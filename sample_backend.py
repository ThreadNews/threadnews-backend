from flask import Flask,Response
from flask import request
from flask import jsonify
from flask_cors import CORS
import os
import json
from feed import NewsAPICalls
import logger
from config import threadConfiguration
from database import threadDatabase

app = Flask(__name__)
CORS(app)
log = logger.setup_logger('root')
configFile = threadConfiguration()
log.debug('initalized logger')
appFeed = NewsAPICalls(configFile.get_configuration())
database_client = threadDatabase(configFile.get_configuration())

@app.route('/categoryBubbleData',methods = ['GET',"POST"])
def get_categoy_bubble_data():
   if request.method == 'GET':
      #return json object that is used used to construct bubbles
      print(os.listdir())
      with open("topic_bubble_data.json") as f:
         data = json.load(f)
         ddata = json.dumps(data)
      print(type(data))
      print("DATA:", data)
      return Response(response= data)
      #return data
   elif request.method== "POST":
      #update data in db - not implemented yet
      return Response(response={},status=404)

# @app.route('/users/<id>/<job>',methods = ['GET'])
# def get_users_with_job(id,job):
@app.route('/feed', methods=['GET'])
def get_app_feed():
   """ Get custom feed from NewsAPI and return it """
   if request.method == 'GET':
      q = request.args.get("q")
      q_in_title = request.args.get("qInTitle")
      sources = request.args.get("sources")
      domains = request.args.get("domains")
      exclude_domains = request.args.get("excludeDomains")
      date_from = request.args.get("dateFrom")
      date_to = request.args.get("dateTo")
      lang = request.args.get("lang")
      sort_by = request.args.get("sortBy")
      page_size = request.args.get("pageSize")
      page = request.args.get("page")
      return appFeed.get_feed(q=q, q_in_title=q_in_title, sources=sources, domains=domains, exclude_domains=exclude_domains, date_from=date_from, date_to=date_to, lang=lang, sort_by=sort_by, page_size=page_size, page=page)

@app.route('/sources', methods=['GET'])
def get_app_sources():
   """ Get sources from NewsAPI and return it """
   if request.method == 'GET':
      return appFeed.get_sources()

@app.route('/headlines', methods=['GET'])
def get_app_headlines():
   """ Get headlines from NewsAPI and return it """
   if request.method == 'GET':
      return appFeed.get_headlines()

@app.route('/users', methods=['GET'])
def get_users():
   """ Get the users of ThreadNews"""
   if request.method == 'GET':
      return jsonify(database_client.get_users()), 200

@app.route('/articles', methods=['GET'])
def get_articles():
   if request.method == 'GET':
      pages = request.args.get("pages")
      if pages is None:
         pages = 1
      return database_client.get_articles(int(pages))