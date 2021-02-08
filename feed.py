from flask import jsonify
import requests
import configparser

headlines = "https://newsapi.org/v2/top-headlines?country=us&apiKey={}"
sources = "https://newsapi.org/v2/sources?apiKey={}"

class NewsAPICalls:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config/api.conf')
        self.api_key = config['NewsAPI']['key'].strip("\'")

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
