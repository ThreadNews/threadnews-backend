from flask import jsonify
import requests
import configparser

headlines = "https://newsapi.org/v2/top-headlines"
sources = "https://newsapi.org/v2/sources"
feed = "https://newsapi.org/v2/everything"

class NewsAPICalls:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('.config/api.conf')
        self.api_key = config['NewsAPI']['key'].strip("\'")

    def get_requests(self, url: str, data=None):
        if data is None:
            data = {'apiKey': self.api_key}
        else:
            data['apiKey'] = self.api_key
        return requests.get(url, params=data)

    def get_headlines(self, country="us"):
        r = self.get_requests(headlines, data={'country': country})

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 404
        return r.json()

    def get_sources(self):
        r = requests.get(sources)

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 404
        return r.json()

    def get_feed(self, q: str, q_in_title=None, sources=None, domains=None, exclude_domains=None, date_from=None, date_to=None, lang="en", sort_by="publishedAt", page_size=100, page=1):
        if q is None or q == "":
            return jsonify({"error": "empty query"}), 404

        data = {'q': q}
        
        if lang is None:
            data['lang'] = "en"
        else: 
            data['lang'] = lang

        if sort_by is None:
            data['sortBy'] = "popularity"
        else:
            data['sortBy'] = sort_by

        if page_size is None:
            data['pageSize'] = 50
        else:
            data['pageSize'] = page_size
            
        data['page'] = 1 if page is None else page

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
