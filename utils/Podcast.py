import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

class SpotifyPodcasts:

    def __init__(self):
        self.scope =  'user-read-currently-playing user-modify-playback-state user-library-modify playlist-modify-public playlist-read-collaborative playlist-read-private playlist-modify-private'
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope, client_secret="6ee1722e4bf14ae499a1ceda45c81e92", client_id="0e57bf8a5bc0404aa228a4ad5374683b",redirect_uri='http://localhost:8000'))

    
    def create_a_list_of_all_podcasts(self, all_topics):
        all_podcasts = []
        for topic in all_topics:
            shows = self.sp.search(q=topic, type="show")
            shows = shows['shows']
            items = shows['items']

            for item in items:
                podcast_list_dict= {"topic": topic, "name": item['name'], "images": item['images'], "publisher": item["publisher"], "uri": item["uri"],
                                      "description": item["description"]}
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
        index_list = self.get_random_indexes(num_pods_per_interest,9)

        for interest in interest_list:
            shows = self.sp.search(q=interest, type="show")
            shows = shows['shows']
            items = shows['items']

            for num in index_list:
                item = items[num]
                name = item['name']
                podcast_list[name] = {"images": item['images'], "publisher": item["publisher"], "uri": item["uri"],
                                      "description": item["description"]}

        return podcast_list


    def get_random_indexes(self, count, range):
        """"
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


interest_list = ["technology", "fashion", "politics", "beauty", "pop culture"]
spot = SpotifyPodcasts()
random_pods = spot.get_a_random_podcast(interest_list)
print(random_pods)
