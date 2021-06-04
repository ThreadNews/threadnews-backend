class SocialFeatures:
    def follow_user(self, user_id1, user_id2, unfollow=False):
        """user 1 follows or unfollows user 2"""
        op = "$pull" if unfollow else "$push"
        self.client.Users.users.update_one(
            {"user_id": user_id1}, {op: {"following": user_id2}}
        )
        self.client.Users.users.update_one(
            {"user_id": user_id2}, {op: {"followers": user_id1}}
        )

        # incriment of decrement follower count / following count
        i = -1 if unfollow else 1
        self.client.User.users.update_one(
            {"user_id": user_id2}, {"$inc": {"following_count": i}}
        )
        self.client.User.users.update_one(
            {"user_id": user_id2}, {"$inc": {"followers_count": i}}
        )
        return 200

    def fetch_social(
        self, user_id, followers=False, following=False, counts=True, reposted=False
    ):
        """gets user social information"""

        query = {"_id": 0}  # ignores id because causes issues parsing

        if followers:  # fetch followers
            query["followers"] = 1

        if following:  # fetch following
            query["following"] = 1

        if reposted:
            query["reposted"] = 1

        if counts:  # fetch counts
            query["counts"] = 1

        cursor = self.client.Users.users.find({"user_id": user_id}, query)
        for user in cursor:
            print("social info - user:" + user_id, user)
            return {"result": user, "msg": "Success"}
        return {"result": {}, "msg": "unable to fetch"}

    def fetch_reccomended_social(self, user_id, following=False, articles=False, N=10):
        """creates list of reccomentdations for user to follow"""
        socials = self.fetch_social(user_id, following=True, counts=True)["result"]
        followers_following = []

        for user in socials["following"]:
            try:
                following_user_socials = self.fetch_social(
                    user, following=True, counts=True
                )
                for user in following_user_socials["result"]["following"]:
                    followers_following.append(user)

            except Exception as e:
                print("exception", e)
        ctr = collections.Counter(followers_following)
        ctr = dict(ctr)
        ctr_dict = dict(sorted(ctr.items(), key=itemgetter(1), reverse=True)[:N])

        return {"result": list(ctr_dict.keys())}
