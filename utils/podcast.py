import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import logging
import json
from bson import json_util
from utils.data import TOPIC_LIST

# implement threading for the podcast uploading
logger = logging.getLogger("root")
_SIZE = 20


class Podcast:
    def create_a_list_of_all_podcasts(self, limit):
        """
        Description: Creates a list of podcasts under a certain limit 

        Params:
            limit (int) = how many podcasts will be returned

        Returns:
            podcast_list (list of Podcasts) = list of podcasts within user interest range
        """
        all_podcasts = []
        for topic in TOPIC_LIST:
            if limit > len(all_podcasts):
                break
            shows = self.podcast_sp.search(q=topic, type="show")
            shows = shows["shows"]
            items = shows["items"]

            for item in items:
                podcast_list_dict = {
                    "topic": topic,
                    "name": item["name"],
                    "images": item["images"],
                    "publisher": item["publisher"],
                    "uri": item["uri"],
                    "description": item["description"],
                }
                all_podcasts.append(podcast_list_dict)

        return all_podcasts

    def get_a_random_podcast(self, interest_list, limit=20):
        """
        Description: Gives a collection of podcasts that
        fit the user's interests to show in their feed

        Params:
            interest_list (list of string)  =  user interests
            limit (int) = how many podcasts will be returned

        Returns:
            podcast_list (Dict of Podcasts) = dictionary of random podcasts within user interest range
        """
        podcast_list = {}
        num_pods_per_interest = 4
        index_list = self.get_random_indexes(num_pods_per_interest, 9)

        for interest in interest_list:
            shows = self.sp.search(q=interest, type="show")
            shows = shows["shows"]
            items = shows["items"]

            for num in index_list:
                item = items[num]
                name = item["name"]
                podcast_list[name] = {
                    "images": item["images"],
                    "publisher": item["publisher"],
                    "uri": item["uri"],
                    "description": item["description"],
                }

        return podcast_list

    def get_random_indexes(self, count, range):
        """"
        Description: Gets a random indexes within a range 
        to randomize podcast selection from API 

        Params:
            count (int) = how many random ints returned
            range (int) = what is the highest # the random int can be (0 - range)

        Returns:
            index list(list of ints) = returns a list of random integers
        """

        index_list = []
        i = 0
        while i < count:
            r = random.randint(1, range)
            if r not in index_list:
                index_list.append(r)
                i += 1

        return index_list

    def push_new_podcasts(self, limit=700):
        """"
        Description: Puts new podcasts in the database 
        
        Params:
            limit (int) = how many podcasts will pushed 

        Returns:
            Return dict = 200 message for success 
        """
        inserted = 0
        podcasts = self.create_a_list_of_all_podcasts(limit)

        logger.info("trying to insert {} podcasts\n".format(len(podcasts)))

        for podcast in podcasts:
            self.client.Podcasts.allPodcasts.insert_one(podcast)
            inserted += 1

        # logger.info("inserted {} new  podcasts\n".format(inserted))
        return ({"msg": "success"}, 200)

    def get_all_podcasts(self, q={}, page=1, limit=20):
        """"
        Description: Gets podcasts from the database 
        
        Params:
            q (dict) = database query 

        Returns:
            Return dict = response from database 
        """
        logger.info(f"getting podcasts {q}: page number {page}")
        payload = json.loads(
            json.dumps(
                list(
                    self.client.Podcasts.allPodcasts.find(q)
                    .skip((page - 1) * _SIZE)
                    .limit((page - 1) * _SIZE + _SIZE)
                ),
                default=json_util.default,
            )
        )

        if len(payload) == 0:
            return {"message": "no articles possible"}, 404

        else:
            return payload
