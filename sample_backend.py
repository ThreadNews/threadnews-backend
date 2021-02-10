from flask import Flask,Response
from flask import request
from flask import jsonify
from flask_cors import CORS
import os
import json
from feed import NewsAPICalls

app = Flask(__name__)
CORS(app)
appFeed = NewsAPICalls()

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
   """ Get headlines from NewsAPI and return it """
   if request.method == 'GET':
      return appFeed.get_headlines() # TODO currently returning headlines and not a feed

@app.route('/sources', methods=['GET'])
def get_app_sources():
   """ Get sources from NewsAPI and return it """
   if request.method == 'GET':
      return appFeed.get_sources()

@app.route('/headlines', methods=['GET'])
def get_app_feed():
   """ Get headlines from NewsAPI and return it """
   if request.method == 'GET':
      return appFeed.get_headlines()