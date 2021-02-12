from flask import jsonify
import requests
import configparser

headlines = "https://newsapi.org/v2/top-headlines"
sources = "https://newsapi.org/v2/sources"
feed = "https://newsapi.org/v2/everything"

DEFAULT_LANG="en"
DEFAULT_SORT="popularity"
DEFAULT_SIZE=50
STARTING_PAGE=1

class NewsAPICalls:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('.config/api.conf')
        self.api_key = config['NewsAPI']['key'].strip("\'")

    def get_requests(self, url: str, data=None):
        """ helper function, send a get request to a specified url and any parameters """
        if data is None:
            data = {'apiKey': self.api_key}
        else:
            data['apiKey'] = self.api_key
        return requests.get(url, params=data)

    def get_headlines(self, country="us"):
        """ get headlines from a specified country (default is US) """
        r = self.get_requests(headlines, data={'country': country})

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 404
        return r.json()

    def get_sources(self):
        """ retrieves the current sources gathered from NewsAPI """
        r = requests.get(sources)

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 404
        return r.json()

    def get_feed(self, q: str, q_in_title=None, sources=None, domains=None, exclude_domains=None, date_from=None, date_to=None, lang="en", sort_by="publishedAt", page_size=100, page=1):
        """ retrieves a feed from a queried item plus any other parameters """
        if q is None or q == "":
            return jsonify({"error": "empty query"}), 404

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

        r = self.get_requests(feed, data=data)
        if r.status_code != 200:
            return jsonify({"error": "internal error"}), 404
        return r.json()
