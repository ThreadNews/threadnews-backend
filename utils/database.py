from pymongo import MongoClient
import logging
import certifi
from utils.user import User
from utils.social_features import SocialFeatures
from utils.article import Article
from utils.podcast import Podcast
import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger("root")


class threadDatabase(User, Article, Podcast, SocialFeatures):
    """class uses multiple inheritince to seperate database functionality into
    user, article, podcast and social feature interactions"""

    # class wide var for spotify database
    def __init__(self, config):
        self.scope = "user-read-currently-playing user-modify-playback-state user-library-modify playlist-modify-public playlist-read-collaborative playlist-read-private playlist-modify-private"
        self.podcast_sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=self.scope,
                client_secret="6ee1722e4bf14ae499a1ceda45c81e92",
                client_id="0e57bf8a5bc0404aa228a4ad5374683b",
                redirect_uri="http://localhost:8000",
            )
        )

        database, user, password = (
            config["MongoDB"]["URl"],
            config["MongoDB"]["user"],
            config["MongoDB"]["password"],
        )
        if (
            database == "YOURURLHERE"
            or user == "YOURUSERHERE"
            or password == "YOURPASSWORDHERE"
        ):
            logger.critical("user or password has not been changed!")
        else:
            logger.info("database has been successfully hooked up")
        self.client = MongoClient(
            database.format(user, password), tlsCAFile=certifi.where()
        )
        # self.client = MongoClient(
        #     "mongodb+srv://thread-admin:dontThr3adOnM3@cluster0.n4ur2.mongodb.net"
        # )
