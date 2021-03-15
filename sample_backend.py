from flask import Flask,Response
from flask import request
from flask import jsonify
from flask_cors import CORS
import os
import json
import jsonify
import uuid
import hashlib
from feed import NewsAPICalls
from pymongo import MongoClient
from db_templates import get_sentiment
import logger
from config import threadConfiguration
from database import threadDatabase
import multiprocessing
import atexit

app = Flask(__name__)
CORS(app)
log = logger.setup_logger('root')
configFile = threadConfiguration()
log.debug('initalized logger')

database_client = threadDatabase(configFile.get_configuration())

def feed_worker():
    # this is where the feed updator will be
    appFeed = NewsAPICalls(configFile.get_configuration())
    print("I'm the feed")
    return

feed_process = multiprocessing.Process(target=feed_worker)
# sentiment_process = multiprocessing.Process(target=sentiment_worker, args=(database_client,))
feed_process.start()

def exit_handler():
   feed_process.terminate()

atexit.register(exit_handler)

sentiment_queue = []
salt = open('salt.txt').readline()
print("CURRENT SALT: ", salt)
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

@app.route('/login',methods=["POST"])
def try_login():
   status = {"status":"success"}
   data = request.get_json(force=True)
   print("type data :", type(data))
   print("data: ", data, data.keys())

   #pass_hash = hashlib.sha512((data['password']+salt).encode('utf-8')).hexdigest()
   pass_hash = "00e2a7f276ac9aa5c1ecbbab43059328479a3f5c9aac3d8811229b94fe7552d67179d497c41a497d844dfae069c2200a877b1f863d7580f5238eccd8e66e750a"
   # user_objects_in_table = client.Users.users.find({'user_name':data.get("user_name")})
   #print("username", data.get("username"))
   user = client.Users.users.find_one({'email':data.get("email")})
   print("user", type(user),user)
   print('user keys:', user.keys())

   count = client.Users.users.count 
   print("count", count)
   print("user fetched:", user)
   if len(user.keys()) > 0: 
      del user['_id']
      if(pass_hash == user['pass_hash']):
            status["user_name"] = data.get("user_name")
            status["user"] = user
            return status
      else:
            return {"status":"failure"}

   status["user_name"] = data.get("user_name")
   
   #          del user['_id']
   #          status["user"] = user
   #          return status

   # # if user_objects_in_table.count > 0: 
   #    for user in user_objects_in_table:
   #       if(pass_hash == user_objects_in_table['pass_hash']):
   #          status["user_name"] = data.get("user_name")
   #          del user['_id']
   #          status["user"] = user
   #          return status
   #          #return Response(response=status) 
   #       else: 
   #          return {"status":"failure"}
      




   



   # if found 
     # send another message to front end success logging in 

   # if not found 
      # send message back to front end 
      # increment count how many times user has tried to login 


   


@app.route('/newUser/<username>/<email>/<password>', methods=["POST"])
def new_user(username,email,password):
   pass_hash = hashlib.sha512((password+salt).encode('utf-8')).hexdigest()
   print("HASHED PASS:", pass_hash[:10], type(pass_hash))
   user = {
      "user_id": str(uuid.uuid1()),
      "user_name": username,
      "first_name": "John",
      "last_name": "Doe",
      "email": email,
      "interests": [],
      "pass_hash":pass_hash,
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