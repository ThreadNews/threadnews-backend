from flask import request, Blueprint
from backend_vars import database_client
from flask_jwt_extended import jwt_required, get_jwt_identity

article_blueprint = Blueprint('article_blueprint', __name__)

@article_blueprint.route('/like', methods=["POST"])
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

@article_blueprint.route('/comment', methods=['POST'])
@jwt_required()
def comment(article_id):
   """ Add comment to user and article """
   data = request.get_json(force=True)
   if data['action']=='add':
      database_client.push_comment(data['user_id'],data['article_id'],data['comment'])

@article_blueprint.route('/threads/<interest>/<n>', methods=["POST"])
def get_interest_thread(interest,n):
   #articles = database_client.get_articles(q={'main_topic': interest}, page=n)
   articles=database_client.client.Articles.allArticles.find()
   print(articles)

   article_ls = []
   for article in articles:
      del article['_id']
      article_ls.append(article)
   return {'articles':article_ls}