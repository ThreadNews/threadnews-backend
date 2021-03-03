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
        logger.info("getting users")
        return json.loads(json.dumps(list(self.client.Users.users.find()), default=json_util.default))

    def get_articles(self, page=1):
        logger.info(f"getting articles: page number {page}")
        payload = json.loads(json.dumps(list(self.client.Articles.allArticles.find().skip((page-1)*_SIZE).limit((page-1)*_SIZE + _SIZE)), default=json_util.default))
        if len(payload) == 0:
            return {"message": "no articles possible"}, 404
        return {"articles": payload, "page": page}, 200

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
