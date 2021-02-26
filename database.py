from pymongo import MongoClient
import pprint
import uuid
import json
import logging

logger = logging.getLogger('root')

class threadDatabase:
    def __init__(self, config):
        database, user, password = config['MongoDB']['URl'], config['MongoDB']['user'], config['MongoDB']['password']
        if database == "YOURURLHERE" or user == "YOURUSERHERE" or password == "YOURPASSWORDHERE":
            logger.critical("user or password has not been changed!")
        self.client = MongoClient(database.format(user, password))
        logger.info("database has been successfully hooked up")

    def get_users(self):
        return self.client.Users.users.find()