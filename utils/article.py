import uuid
import random
import logging
import json
from bson import json_util
import time


logger = logging.getLogger("root")
_SIZE = 20


class Article:
    @staticmethod
    def convertToDataFrame(article_data):
        def convertor(article):
            unique_bytes = ""
            if article["author"]:
                unique_bytes += article["author"]
            if article["title"]:
                unique_bytes += article["title"]
            if article["url"]:
                unique_bytes += article["url"]
            article["id"] = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_bytes))
            article["global_score"] = 50
            article["main_topic"] = ""
            article["tags"] = {}
            return article

        if isinstance(article_data, list):
            return [convertor(article) for article in article_data]
        return [convertor(article_data)]

    def get_random_article(self):
        """Gets random article (used for test users)"""
        article = dict(
            self.client.Articles.allArticles.find()
            .limit(-1)
            .skip(int(random.randint(0, 50)))
            .next()
        )
        del article["_id"]

        return article

    def get_articles(self, q={}, page=1):
        """Retrieves articles"""
        logger.info(f"getting articles {q}: page number {page}")
        payload = json.loads(
            json.dumps(
                list(
                    self.client.Articles.allArticles.find(q)
                    .skip((page - 1) * _SIZE)
                    .limit((page - 1) * _SIZE + _SIZE)
                ),
                default=json_util.default,
            )
        )
        if len(payload) == 0:
            return {"message": "no articles possible"}, 404

        return 200

    def get_article_by_id(self, article_id):
        articles = self.client.Articles.allArticles.find({"id": article_id})
        for article in articles:
            return article

    def push_new_headlines(self, max=50):
        feed = NewsAPICalls(self.config)
        headlines = feed.get_headlines()
        print(headlines.keys())
        i = 0
        for article in headlines["articles"]:
            # print(article.get_json())
            if i < max:
                article["id"] = str(uuid.uuid4()).strip("-")
                article["global_score"] = 50
                article["main_topic"] = ""
                article["tags"] = {}
                # self.client.Articles.allArticles.insert_one(article)
                i += 1
        {"msg": "success"}

    def add_likes_articles(self, user_id, article_id):
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    "liked_articles": article_id,
                }
            },
        )
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"likes": 1}}
        )
        return 200

    def repost_article(self, user_id, article_id, add=True):
        op = "$push" if not add else "$pull"
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                op: {
                    "reposted_articles": article_id,
                }
            },
        )
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"reposts": 1}}
        )
        return 200

    def remove_likes_articles(self, user_id, article_id):
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                "$pull": {
                    "liked_articles": article_id,
                }
            },
        )
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$dec": {"likes": 1}}
        )
        return 200

    def push_new_comment(self, user_name, article_id, comment, add=True):
        # add comment to user document(comment, article_id)
        op = "$push" if add else "$pull"
        # self.client.Users.users.update_one({"user_id":user_id},{op:{'comments': {'comment':comment,'article_id':article_id}}})
        # add comment to article document(comment,user_name)
        self.client.Articles.allArticles.update_one(
            {"id": article_id},
            {op: {"comments": {"comment": comment, "user_name": user_name}}},
        )
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    "liked_articles": article_id,
                }
            },
        )
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"likes": 1}}
        )
        return 200

    def remove_likes_articles(self, user_id, article_id):
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                "$pull": {
                    "liked_articles": article_id,
                }
            },
        )
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$dec": {"likes": 1}}
        )
        return 200

    def push_new_comment(self, user_name, article_id, comment):
        # add comment to user document(comment, article_id)
        self.client.Users.users.update_one(
            {"id": article_id},
            {"$push": {"comments": {"comment": comment, "user_name": user_name}}},
        )
        # add comment to article document(comment,user_name)
        self.client.Articles.allArticles.update_one(
            {"id": article_id},
            {"$push": {"comments": {"comment": comment, "article_id": article_id}}},
        )
        return 200

    def push_new_articles(self, articles):
        inserted = 0
        logger.info("trying to insert {} articles".format(len(articles)))
        for article in articles:
            if (
                self.client.Articles.allArticles.find({"id": article["id"]}).count()
                == 0
            ):
                self.client.Articles.allArticles.insert_one(article)
                inserted += 1

        logger.info("inserted {} new articles".format(inserted))
        return ({"msg": "success"}, 200)

    def push_new_like(self, user_id, article_id):
        # add like article document
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    "liked_articles": article_id,
                }
            },
        )
        # add article id to user document
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"likes": 1}}
        )
        return 200

    def push_new_view(self, user_id, article_id):
        # stores article id, headline, sentiment in user object
        article_data = self.get_article_by_id(article_id)
        article_data["date"] = time.time()
        self.client.Users.users.update_one(
            {"user_id": user_id}, {"$push": {"viewed_articles": article_data}}
        )
        return 200, "success"

    def push_new_save(self, user_id, article_id):
        # add save to user doccument
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                "$push": {
                    "saved_articles": article_id,
                }
            },
        )
        # add save count to article document
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"saves": 1}}
        )
        return "success", 200

    def delete_save(self, user_id, article_id):
        # add save to user doccument
        self.client.Users.users.update_one(
            {"user_id": user_id},
            {
                "$pull": {
                    "saved_articles": article_id,
                }
            },
        )
        # add save count to article document
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"saves": -1}}
        )
        return 200

    def delete_like(self, user_id, article_id):
        # add like article document
        # add like article doccument
        self.client.Users.users.update_one(
            {"user_id": user_id}, {"$pull": {"liked_articles": article_id}}
        )
        # add article id to user document
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"likes": -1}}
        )
        return 200

    def get_article_list(self, article_ids, n=10):
        article_ls = []
        cur = self.client.Articles.allArticles.find(
            {"id": {"$in": list(article_ids)}}
        ).limit(n)
        for article in cur:
            del article["_id"]
            article_ls.append(article)

        return article_ls

    def delete_like(self, user_id, article_id):
        # add like article document
        self.client.Users.users.update_one(
            {"user_id": user_id}, {"$pull": {"liked_articles": article_id}}
        )
        # add article id to user document
        self.client.Articles.allArticles.update_one(
            {"id": article_id}, {"$inc": {"likes": -1}}
        )
        return 200
