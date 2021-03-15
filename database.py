from pymongo import MongoClient
from bson import json_util
import jsonify
import pprint
import uuid
import json
import logging
import certifi
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

    def get_users(self):
        """ Retrieves users """
        logger.info("getting users")
        return json.loads(json.dumps(list(self.client.Users.users.find()), default=json_util.default))

    def get_user(self, q=""):
        """ Retrieves users """
        logger.info("getting users")
        return json.loads(json.dumps(list(self.client.Users.users.find(q)), default=json_util.default))

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

    def add_likes_articles(self, user_id, article_id):
        self.client.Users.users.update_one({"user_id":user_id},{'$push':{'liked_articles': article_id,}})
        self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'likes':1}})

    def remove_likes_articles(self, user_id, article_id):
        self.client.Users.users.update_one({"user_id":user_id},{'$pull':{'liked_articles': article_id,}})
        self.client.Articles.allArticles.update_one({'id':article_id},{'$dec':{'likes':1}})

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
                self.client.Articles.allArticles.insert_one(article)
                i+=1

    def push_new_comment(self,user_name,article_id,comment):
        #add comment to user document(comment, article_id)
        self.client.Users.users.update_one({"id":article_id},{'$push':{'comments': {'comment':comment,'user_name':user_name}}})
        #add comment to article document(comment,user_name)
        self.client.Articles.allArticles.update_one({"id":article_id},{'$push':{'comments': {'comment':comment,'article_id':article_id}}})
        return 200

    def push_new_like(self,user_id,article_id):
        #add like article doccument
        self.client.Users.users.update_one({"user_id":user_id},{'$push':{'liked_articles': article_id,}})
        #add article id to user document
        self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'likes':1}})
        return 200

    def delete_like(self,user_id,article_id):
            #add like article doccument
            self.client.Users.users.update_one({"user_id":user_id},{'$pull':{'liked_articles': article_id}})
            #add article id to user document
            self.client.Articles.allArticles.update_one({'id':article_id},{'$inc':{'likes':-1}})
            return 200

    def update_bio(self,user_id,bio):
        """ Updates user bio in user document """
        self.client.User.users.update_one({'user_id':user_id},{'$set':{'bio':bio}})
        return 200