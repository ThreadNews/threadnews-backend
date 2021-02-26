from pymongo import MongoClient
import pprint
import uuid
import json
import logging

logger = logging.getLogger('root')
database_url="mongodb+srv://{}:{}@cluster0.n4ur2.mongodb.net"

class threadDatabase:
    def __init__(self, config):
        user, password = config['MongoDB']['user'], config['MongoDB']['password'])
        if user == "YOURUSERHERE" or password == "YOURPASSWORDHERE":
            logger.critical("user or password has not been changed!")
        self.client = MongoClient(database_url.format(user, password))
        print(self.client)

    def get_users(self):
        return self.client.Users.users.find()