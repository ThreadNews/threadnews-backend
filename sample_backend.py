from flask import Flask,Response
from flask import request
from flask import jsonify
from flask_cors import CORS
import os
import json
import jsonify
import uuid
from feed import NewsAPICalls
from pymongo import MongoClient
from db_templates import get_sentiment
app = Flask(__name__)
CORS(app)


sentiment_queue = []

client = MongoClient("mongodb+srv://thread-admin:dontThr3adOnM3@cluster0.n4ur2.mongodb.net")

@app.route('/categoryBubbleData',methods = ['GET',"POST"])
def get_categoy_bubble_data():
   if request.method == 'GET':
      #return json object that is used used to construct bubbles
      print(os.listdir())
      with open("topic_bubble_data.json") as f:
         data = json.load(f)
      print(type(data))
      print("DATA:", data)
      return Response(response= data)
      #return data
   elif request.method== "POST":
      #update data in db - not implemented yet
      return Response(response={},status=404)

@app.route('/threads/<interest>/<n>', methods=["GET"])
def get_interest_thread(interest,n):
   articles = client.Articles.allArticles.find({'main_topic':interest})
   print(articles)
   article_ls = []
   for article in articles:
      del article['_id']
      article_ls.append(article)
   return {'articles':article_ls}
# @app.route('/users/<id>/<job>',methods = ['GET'])
# def get_users_with_job(id,job):


@app.route('/newUser/<username>/<email>/<password>', methods=["POST"])
def new_user(username,email,password):
   user = {
      "user_id": str(uuid.uuid1()),
      "username": username,
      "first_name": "John",
      "last_name": "Doe",
      "email": email,
      "interests": [],
   }
   result = client.Users.users.insert_one(user)
   #do error check
   return json.dumps(user)


@app.route('/update_interests', methods=["POST"])
def update_user_interests():
   data = request.get_json(force=True)
   print(type(data))
   client.Users.users.update_one({"user_id":data['user_id']},{'$set':{'interests':data['new_interests']}})
   return {}

@app.route('/liked_article/<userId>/<articleId>', methods=["POST"])
def add_liked_article(userId,articleId):
   print('user id:',userId)
   #add article id to user object
   u = client.Users.users.update_one({"user_id":userId},{'$push':{'liked_articles': articleId,}})
   print(type(u),u)
   a = client.Articles.allArticles.update_one({'id':articleId},{'$inc':{'likes':1}})

   return {}






