from flask import json, jsonify
import requests
import configparser

headlines = "https://newsapi.org/v2/top-headlines?country=us&apiKey={}"
sources = "https://newsapi.org/v2/sources?apiKey={}"

class NewsAPICalls:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config/api.conf')
        self.api_key = config['NewsAPI']['key'].strip("\'")

    def get_requests(self, url: str):
        return requests.get(url)

    def get_headlines(self):
        r = requests.get(headlines.format(self.api_key))

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 404
        return r.json()

    def get_sources(self):
        r = requests.get(sources.format(self.api_key))

        if r.status_code != 200:
            return jsonify({"error": "internal errorr"}), 404
        return r.json()

    def get_feed(self, q: str, q_in_title=None, sources=None, domains=None, exclude_domain=None, date_from=None, date_to=None, lang="en", sort_by="publishedAt", pageSize=100, page=1):
        return jsonify({"error": "not yet implemented"}), 404
