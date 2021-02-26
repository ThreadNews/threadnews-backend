from flask import jsonify
import requests
import configparser
import os
import logging 
import sys

HEADLINES = "https://newsapi.org/v2/top-headlines"
SOURCES = "https://newsapi.org/v2/sources"
FEED = "https://newsapi.org/v2/everything"

DEFAULT_LANG="en"
DEFAULT_SORT="popularity"
DEFAULT_SIZE=50
STARTING_PAGE=1

logger = logging.getLogger('root')

class NewsAPICalls:
    """ Wrapper class for NewsAPI calls """

    def __init__(self, configFile):
        self.api_key = configFile['NewsAPI']['key'].strip("\'")
        if self.api_key == "YOURKEYHERE":
            logger.critical("missing api key, please add key to .config/api.conf")
        else:
            logger.info("api key successfully identified in .config/api.conf")

    def get_requests(self, url: str, data=None):
        """ helper function, send a get request to a specified url and any parameters """
        logger.info("{} {}".format(url, data))
        if data is None:
            data = {'apiKey': self.api_key}
        else:
            data['apiKey'] = self.api_key
        return requests.get(url, params=data)

    def get_headlines(self, country="us"):
        """ get headlines from a specified country (default is US) """
        r = self.get_requests(HEADLINES, data={'country': country})

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 500
        return r.json()

    def get_sources(self):
        """ retrieves the current sources gathered from NewsAPI """
        r = self.get_requests(SOURCES)

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 500
        return r.json()

    def get_feed(self, q: str, q_in_title=None, sources=None, domains=None, exclude_domains=None, date_from=None, date_to=None, lang="en", sort_by="publishedAt", page_size=100, page=1):
        """ retrieves a feed from a queried item plus any other parameters """
        if q is None or q == "":
            return jsonify({"error": "empty query"}), 400

        data = {'q': q}

        data['lang'] = DEFAULT_LANG if lang is None else lang
        data['sortBy'] = DEFAULT_SORT if sort_by is None else sort_by
        data['pageSize'] = DEFAULT_SIZE if page_size is None else page_size   
        data['page'] = STARTING_PAGE if page is None else page

        if q_in_title is not None:
            data['qInTitle'] = q_in_title
        if sources is not None:
            data['sources'] = sources
        if domains is not None:
            data['domains'] = domains
        if exclude_domains is not None:
            data['excludeDomains'] = exclude_domains
        if date_from is not None:
            data['from'] = date_from
        if date_to is not None:
            data['to'] = date_to

        r = self.get_requests(FEED, data=data)
        if r.status_code != 200:
            return jsonify({"error": "internal error"}), 500
        return r.json()
