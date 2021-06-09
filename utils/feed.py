import requests
import logging
from .article import Article
from utils.data import TOPIC_LIST
from random import choice

HEADLINES = "https://newsapi.org/v2/top-headlines"
SOURCES = "https://newsapi.org/v2/sources"
FEED = "https://newsapi.org/v2/everything"

DEFAULT_LANG = "en"
DEFAULT_SORT = "popularity"
DEFAULT_SIZE = 50
STARTING_PAGE = 1


logger = logging.getLogger("root")


class NewsAPICalls:
    """Wrapper class for NewsAPI calls"""

    def __init__(self, api_key):
        self.api_key = api_key
        if self.api_key == "YOURKEYHERE":
            logger.critical("missing api key, please add key to .config/api.conf")
        else:
            logger.info("api key successfully identified in .config/api.conf")

    def _rotate_api(self):
        if isinstance(self.api_key, list):
            current = self.api_key.pop(0)
            self.api_key.append(current)
            return current
        return self.api_key

    def get_requests(self, url: str, data=None):
        """helper function, send a get request to a specified url and any parameters"""
        logger.info("{} {}".format(url, data))
        if data is None:
            data = {"apiKey": self._rotate_api()}
        else:
            data["apiKey"] = self._rotate_api()

        try:
            return requests.get(url, params=data)
        except:
            return None

    def get_headlines(self, country="us"):
        """get headlines from a specified country (default is US)"""
        r = self.get_requests(HEADLINES, data={"country": country})

        if r.status_code != 200:
            return {"error": "internal errorr"}, 500
        return r.json(), 200

    def get_sources(self):
        """retrieves the current sources gathered from NewsAPI"""
        r = self.get_requests(SOURCES)

        if r.status_code != 200:
            return {"error": "internal errorr"}, 500
        return r.json(), 200

    def get_feed(
        self,
        q: str,
        q_in_title=None,
        sources=None,
        domains=None,
        exclude_domains=None,
        date_from=None,
        date_to=None,
        lang="en",
        sort_by="publishedAt",
        page_size=100,
        page=1,
    ):
        """retrieves a feed from a queried item plus any other parameters"""
        if q is None or q == "":
            return {"error": "empty query"}, 400

        data = {"q": q}

        data["lang"] = DEFAULT_LANG if lang is None else lang
        data["sortBy"] = DEFAULT_SORT if sort_by is None else sort_by
        data["pageSize"] = DEFAULT_SIZE if page_size is None else page_size
        data["page"] = STARTING_PAGE if page is None else page

        if q_in_title is not None:
            data["qInTitle"] = q_in_title
        if sources is not None:
            data["sources"] = sources
        if domains is not None:
            data["domains"] = domains
        if exclude_domains is not None:
            data["excludeDomains"] = exclude_domains
        if date_from is not None:
            data["from"] = date_from
        if date_to is not None:
            data["to"] = date_to

        r = self.get_requests(FEED, data=data)
        if r.status_code != 200:
            return {"error": "internal error"}, 500
        return r.json(), 200


class NewsAPI:
    def __init__(self, config):
        self.api_key = config.get_api_keys()
        self.feed = NewsAPICalls(self.api_key)

    def begin_collection(self):
        """current implementation makes use of hourly pull"""
        # todo: add more items to add articles to the database
        rand_topic = choice(TOPIC_LIST)
        feed = self.feed.get_feed(q=rand_topic)
        if 200 not in feed:
            return None

        headlines = self.feed.get_headlines()
        if 200 not in headlines:
            return None

        formatted_articles = Article.convert_to_dataframe(
            feed[0]["articles"], topic=rand_topic
        )
        formatted_articles += Article.convert_to_dataframe(headlines[0]["articles"])

        return formatted_articles
