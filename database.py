from pymongo import MongoClient
from bson import json_util
import uuid
import json
import logging
import certifi
import time
import collections
from operator import itemgetter
from feed import NewsAPICalls
logger = logging.getLogger('root')
_SIZE=20
class threadDatabase:
    def __init__(self, config):
        database, user, password = config['MongoDB']['URl'], config['MongoDB']['user'], config['MongoDB']['password']
        if database == "YOURURLHERE" or user == "YOURUSERHERE" or password == "YOURPASSWORDHERE":
            logger.critical("user or password has not been changed!")
        else:
            logger.info("database has been successfully hooked up")


        self.client = MongoClient(database.format(user, password), tlsCAFile=certifi.where())
        
        # self.client = MongoClient(database.format(user, password), tlsCAFile=certifi.where())
        #self.client = MongoClient("mongodb+srv://thread-admin:dontThr3adOnM3@cluster0.n4ur2.mongodb.net")

    def get_article_by_id(self,article_id):
        articles = self.client.Articles.allArticles.find(
            {'id':article_id})
        for article in articles:
            return article
        
    def get_users(self):
        """ Retrieves users """
        logger.info("getting users")
        return json.loads(json.dumps(list(self.client.Users.users.find()), default=json_util.default))

    def get_user(self, q=""):
        """ Retrieves users """
        logger.info("getting users")
        return json.loads(json.dumps(list(self.client.Users.users.find(q)), default=json_util.default))


    def get_user_interests(self, q='',interests=True):
        user = self.get_user(q)[0]
        print("USER:",user)
        if user['interests'] is not None and interests:
            return {'interests':user['interests']}
        return {'msg':'error'}


    def add_user(self, new_user=None):
        logger.info("trying to add new user")

        if len(self.get_user(q={'email': new_user['email']})) != 0:
            return {"result": -1, "msg": "email exists"}

        if len(self.get_user(q={'user_name': new_user['user_name']})) != 0:
            return {"result": -1, "msg": "username exists"}

        if self.client.Users.users.insert_one(new_user).inserted_id:
            return {"result": 1, "msg": "successfully inserted"}
        else:
            return {"result": -1, "msg": "failed to inserted"}

    def get_user_count(self):
        return self.client.Users.users.count

    def get_articles(self, q={}, page=1):
        """ Retrieves articles """
        logger.info(f"getting articles {q}: page number {page}")
        payload = json.loads(json.dumps(list(self.client.Articles.allArticles.find(q).skip((page-1)*_SIZE).limit((page-1)*_SIZE + _SIZE)), default=json_util.default))
        if len(payload) == 0:
            return {"message": "no articles possible"}, 404

    def push_new_user(self, payload=None):
        """ Should be dealt with the login authentication """
        if payload is not None:
            if self.Client.Users.users.find({"user_name": payload["user_name"]}) is not None:
                logger.info("username already in use")
            elif self.Client.Users.users.find({"email": payload["email"]}) is not None:
                logger.info("email already in use")
            else:
                logger.info("adding new user")
                self.Client.Users.users.insert_one(payload)
                return 201
            return 409
        else:
            logger.info("not possible to add user")
            return 500

    def update_user_interest(self, user_id, add=None, remove=None):
        if add:
            self.client.Users.users.update_one({"user_id":user_id},
                    {'$push':
                        {'interests':
                            { '$each': add }
                        }
                    })
        
        print(remove)
        if remove:
            self.client.Users.users.update_one({"user_id":user_id},
                    {'$pull':
                        { 'interests': 
                            { '$in': remove }
                        }
                    })

    def push_new_headlines(self,max=50):
        feed = NewsAPICalls(self.config)
        headlines = feed.get_headlines()
        print(headlines.keys())
        i=0
        for article in headlines['articles']:
            # print(article.get_json())
            if i<max:
                article['id'] = str(uuid.uuid4()).strip('-')
                article['global_score'] = 50
                article["main_topic"] = ""
                article['tags'] = {}
                # self.client.Articles.allArticles.insert_one(article)
                i+=1
        {'msg':'success'}
        
    def add_likes_articles(self, user_id, article_id):
        self.client.Users.users.update_one({"user_id":user_id},{'$push':{'liked_articles': article_id,}})
        self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'likes':1}})

    def remove_likes_articles(self, user_id, article_id):
        self.client.Users.users.update_one({"user_id":user_id},{'$pull':{'liked_articles': article_id,}})
        self.client.Articles.allArticles.update_one({'id':article_id},{'$dec':{'likes':1}})

    def push_new_comment(self,user_name,article_id,comment):
        #add comment to user document(comment, article_id)
        self.client.Users.users.update_one({"id":article_id},{'$push':{'comments': {'comment':comment,'user_name':user_name}}})
        #add comment to article document(comment,user_name)
        self.client.Articles.allArticles.update_one({"id":article_id},{'$push':{'comments': {'comment':comment,'article_id':article_id}}})
        return 200

    def push_new_articles(self, articles):
        inserted = 0
        logger.info("trying to insert {} articles".format(len(articles)))
        for article in articles:
            if self.client.Articles.allArticles.find({"id": article["id"]}).count() == 0:
                self.client.Articles.allArticles.insert_one(article)
                inserted += 1
                
        logger.info("inserted {} new articles".format(inserted))
        return {"msg": "success"}, 200

    def push_new_like(self,user_id,article_id):
        #add like article document
        self.client.Users.users.update_one({"user_id":user_id},{'$push':{'liked_articles': article_id,}})
        #add article id to user document
        self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'likes':1}})
        return 200


    def push_new_view(self,user_id,article_id):
        #stores article id, headline, sentiment in user object
        article_data = self.get_article_by_id(article_id)
        article_data['date'] = time.time()
        self.client.Users.users.update_one({'user_id':user_id},{'$push':{'viewed_articles':article_data}})
        return 200,"success"


    def push_new_save(self,user_id,article_id):
        #add save to user doccument
        self.client.Users.users.update_one({"user_id":user_id},{'$push':{'saved_articles': article_id,}})
        #add save count to article document
        self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'saves':1}})
        return 'success',200

    def delete_save(self,user_id,article_id):
        #add save to user doccument
        self.client.Users.users.update_one({"user_id":user_id},{'$pull':{'saved_articles': article_id,}})
        #add save count to article document
        self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'saves':-1}})


    def delete_like(self,user_id,article_id):
        #add like article document
        self.client.Users.users.update_one({"user_id":user_id},{'$pull':{'liked_articles': article_id}})
        #add article id to user document
        self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'likes':-1}})
        return 200



    def update_interests(self, user_id, interests, remove=False):
        op = '$push' if not remove else '$pull'
        for interest in interests:
            self.client.Users.users.update_one({'user_id':user_id,},{op:{'interests':interest}})
        return 200


    def update_bio(self,user_id,bio):
        """ Updates user bio in user document """
        self.client.User.users.update_one({'user_id':user_id},{'$set':{'bio':bio}})
        return 200

    def follow_user(self,user_id1,user_id2,unfollow=False):
        """user 1 follows or unfollows user 2"""
        op = '$pull' if unfollow else '$addToSet'
        self.client.Users.users.update_one({'user_id':user_id1},{op:{'following':user_id2}})
        self.client.Users.users.update_one({'user_id':user_id2},{op:{'followers':user_id1}})

        #incriment of decrement follower count / following count
        i = -1 if unfollow else 1
        self.client.User.users.update_one({'user_id':user_id2},{'$inc':{'following_count':i}})
        self.client.User.users.update_one({'user_id':user_id2},{'$inc':{'followers_count':i}})
        return 200

    
    def fetch_social(self,user_id,followers=False,following=False,counts=True):
        """gets user social information"""

        query = {'_id':0} #ignores id because causes issues parsing
        
        if followers: #fetch followers
            query['followers']=1

        if following: #fetch following
            query['following'] = 1

        if counts: #fetch counts
            query['counts']=1

        cursor = self.client.Users.users.find({'user_id':user_id},query)
        for user in cursor:    
            print("social info - user:"+ user_id, user)
            
            return {'result':user,'msg':'Success'}
        return {'result':{},'msg':'unable to fetch'}
                

    def fetch_reccomended_social(self,user_id, following = False, articles=False, N=10):
        """creates list of reccomentdations for user to follow"""
        socials = self.fetch_social(user_id,following=True, counts = True)['result']
        followers_following = []
        for user in socials['following']:
            following_user_socials = self.fetch_social(user,following=True, counts = True)

            followers_following.append(following_user_socials['result']['following'])
        print("Original List : ",followers_following)
        ctr = collections.Counter(followers_following)
        ctr= dict(ctr)
        ctr_dict = dict(sorted(ctr.items(), key = itemgetter(1), reverse = True)[:N])
        return {'result':ctr_dict.keys()}


