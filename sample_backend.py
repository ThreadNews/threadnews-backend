
from flask import request
from flask import jsonify

import os
import json
import jsonify
import uuid
import hashlib

# from pymongo import MongoClient
# from db_templates import get_sentiment


from pymongo import MongoClient
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

import bcrypt

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


   
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return {"logged_in_as": current_user}, 200




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



      