import json
from bson import json_util
import logging

logger = logging.getLogger("root")


class User:
    def get_user_list(self, user_ls):
        """gets a user information from ids"""
        if type(user_ls) == dict:
            user_ls = list(user_ls.values())
        return self.get_user(q={"user_id": {"$in": user_ls}})

    def get_substring_search_results(self, search_string):
        """searching users by substring"""
        list_of_users_to_display = []
        print("starting ...")
        users = self.client.Users.users.find()
        for user in users:
            del user["_id"]

            if "user_name" in user.keys():
                if search_string in user["user_name"]:
                    list_of_users_to_display.append(user)

        return list_of_users_to_display

    def get_users(self):
        """Retrieves users"""
        return json.loads(
            json.dumps(list(self.client.Users.users.find()), default=json_util.default)
        )

    def get_user(self, q=""):
        """Retrieves users"""
        return json.loads(
            json.dumps(list(self.client.Users.users.find(q)), default=json_util.default)
        )

    def search_user(self, search_string):
        """searches for a user"""
        q = {"username": "/.*" + search_string + ".*/"}
        return self.get_substring_search_results(search_string)

    def add_user(self, new_user=None):
        """adds new user to database"""
        logger.info("trying to add new user")

        if len(self.get_user(q={"email": new_user["email"]})) != 0:
            return {"result": -1, "msg": "email exists"}

        if len(self.get_user(q={"user_name": new_user["user_name"]})) != 0:
            return {"result": -1, "msg": "username exists"}

        if self.client.Users.users.insert_one(new_user).inserted_id:
            return {"result": 1, "msg": "successfully inserted"}
        else:
            return {"result": -1, "msg": "failed to inserted"}

    def get_user_count(self):
        return self.client.Users.users.count()

    def get_user_interests(self, q="", interests=True):
        """get users interest"""
        user = self.get_user(q)[0]
        if user["interests"] is not None and interests:
            return {"interests": user["interests"]}
        return {"msg": "error"}

    def update_user_interest(self, user_id, add=None, remove=None):
        msg = "user not added or removed"
        if add:
            self.client.Users.users.update_one(
                {"user_id": user_id}, {"$set": {"interests": {"$each": add}}}
            )
            msg = "user added"
        if remove:
            self.client.Users.users.update_one(
                {"user_id": user_id}, {"$pull": {"interests": {"$in": remove}}}
            )
            msg = "user removed"
        return 200, {"msg": msg}

    def update_user(
        self,
        user_id,
        bio="",
        first_name="",
        last_name="",
        profile_pic="",
        new_password="",
        new_email="",
    ):
        """Updates user bio in user document"""
        new_info = {}
        if bio:
            new_info["bio"] = bio
        if first_name:
            new_info["first_name"] = first_name
        if last_name:
            new_info["last_name"] = last_name
        if profile_pic:
            new_info["profile_pic"] = profile_pic
        if new_password:
            new_info["new_password"] = new_password
        if new_email:
            new_info["new_email"] = new_email

        self.client.Users.users.update_one(
            {"user_id": user_id}, {"$set": new_info}, upsert=True
        )
        return new_info

    def update_interests(self, user_id, interests, remove=False):
        """updates a users interests"""
        op = "$push" if not remove else "$pull"
        for interest in interests:
            self.client.Users.users.update_one(
                {
                    "user_id": user_id,
                },
                {op: {"interests": interest}},
            )
        return 200


    def get_user_list(self, user_ls):
        if type(user_ls) == dict:
            user_ls = list(user_ls.values())
        return self.get_user(q={"user_id": {"$in": user_ls}})

   