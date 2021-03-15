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
# from pymongo import MongoClient
# from db_templates import get_sentiment
import logger
from config import threadConfiguration
from database import threadDatabase
from pymongo import MongoClient
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

import bcrypt

app = Flask(__name__)
CORS(app)
log = logger.setup_logger('root')
configFile = threadConfiguration()
log.debug('initalized logger')
app.config["JWT_SECRET_KEY"] = configFile.get_configuration()['JWT']['secret']

appFeed = NewsAPICalls(configFile.get_configuration())
database_client = threadDatabase(configFile.get_configuration())
jwt = JWTManager(app)

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

@app.route('/threads/<interest>/<n>', methods=["POST"])
def get_interest_thread(interest,n):
   #articles = database_client.get_articles(q={'main_topic': interest}, page=n)
   articles=database_client.client.Articles.allArticles.find()
   print(articles)

   article_ls = []
   for article in articles:
      del article['_id']
      article_ls.append(article)
   return {'articles':article_ls}

@app.route('/login',methods=["POST"])
def try_login():
   if request.method == 'POST':
      data = request.get_json(force=True)
      curr_user = database_client.get_user({"email": data.get("email")})
      if len(curr_user) == 0:
         return {"msg": "no user found"}, 404
      
      curr_user = curr_user[0]
      if not bcrypt.checkpw(str.encode(data['password']), str.encode(curr_user['pass_hash'])):
         return {"msg": "password don't match"}, 400

      # clean up user data for less exposure
      curr_user.pop('pass_hash', None)
      curr_user.pop('_id', None)

      access_token = create_access_token(identity=curr_user)
      return {"access_token": access_token}, 200
   
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return {"logged_in_as": current_user}, 200

@app.route('/newUser', methods=["POST"])
def new_user():
   if request.method == 'POST':
      data = request.get_json(force = True)
      username = None
      email = None
      password = None

      if data:
         if 'username' in data:
            username = data['username']
         else:
            return {'msg': 'username not found'}, 406
         
         if 'email' in data:
            email = data['email']
         else:
            return {'msg': 'email not found'}, 406

         if 'password' in data:
            password = data['password']
         else:
            return {'msg': 'password not found'}, 406

      salt = bcrypt.gensalt()
      pass_hash = bcrypt.hashpw(str.encode(password), salt)
      user = {
         "user_id": str(uuid.uuid1()),
         "user_name": username,
         "first_name": "",
         "last_name": "",
         "email": email,
         "interests": [],
         "pass_hash":pass_hash.decode(),
      }
      log.info("successfully parsed new user information")
      result = database_client.add_user(user)

      if result['result'] == -1:
         return {"msg": result["msg"]}, 404

      # clean up user data for less exposure
      user.pop('_id', None)
      user.pop('pass_hash', None)
      access_token = create_access_token(identity=user)
      return {"msg": "user successfully added", "access_token": access_token}, 200


@app.route('/update_interests', methods=["POST"])
@jwt_required()
def update_user_interests():
   if request.method == 'POST':
      current_user = get_jwt_identity()
      data = request.get_json(force=True) # new interest should be added as {"add": [new interest], "remove": [interest]}
      database_client.update_user_interest(current_user['user_id'], data['add'], data['remove'])
      return {"msg": "success"}, 200
    
@app.route('/like', methods=["POST"])
@jwt_required()
def like_article(articleId):
   """ Add/Delete like to article and user """
   if request.method == 'POST':
      data = request.get_json()
      current_user = get_jwt_identity()
      if data['action']=='add':
         database_client.push_new_like(userId,articleId,articleId)
      if data['action']=='delete':
         database_client.delete_like(data['user_id'],data['article_id'])
      return 200

@app.route('/comment', methods=['POST'])
@jwt_required()
def comment(article_id):
   """ Add comment to user and article """
   data = request.get_json(force=True)
   if data['action']=='add':
      database_client.push_comment(data['user_id'],data['article_id'],data['comment'])

#inprogress
# @app.route('/update_profile')
# @jwt_required()
# def update_bio():
#    """ Add comment to user and article """
#    data = request.get_json(force=True)['bio']
#    user_id = get_jwt_identity()['user_name']
#    database_client.update_bio(user_id,bio)

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
   """ Get headlines from NewsAPI and return itoh yea """
   if request.method == 'GET':
      return appFeed.get_headlines()

@app.route('/users', methods=['GET'])
def get_users():
   """ Get the users of ThreadNews """
   if request.method == 'GET':
      return jsonify(database_client.get_users()), 200

@app.route('/articles', methods=['GET'])
def get_articles():
   if request.method == 'GET':
      pages = request.args.get("pages")
      if pages is None:
         pages = 1
      return database_client.get_articles(int(pages))



      