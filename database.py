from pymongo import MongoClient
from bson import json_util
import pprint
import uuid
import json
import logging
import certifi

logger = logging.getLogger('root')

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
        return self.client.Articles.allArticles.find().skip((page-1)*100).limit((page-1)*100 + 100)