from flask import request, Blueprint
from backend_vars import database_client
from flask_jwt_extended import jwt_required, get_jwt_identity

article_blueprint = Blueprint("article_blueprint", __name__)

@article_blueprint.route("/articles", methods=["POST"])
def article_list():
    if request.method=="POST":
        data = request.get_json()
        articles = database_client.get_article_list(data['article_ids'])
        
        return {'result':articles},200
    return 404


@article_blueprint.route("/like", methods=["POST"])
@jwt_required()
def like_article():
    """ Add/Delete like to article and user """
    # if request.method == "POST":
    data = request.get_json(force =True)
    current_user = get_jwt_identity()
    if data["action"] == "add":
        database_client.push_new_like(current_user['user_id'], data['article_id'])
    if data["action"] == "delete":
        database_client.delete_like(data["user_id"], data["article_id"])
    return 200


@article_blueprint.route("/comment", methods=["POST"])
@jwt_required()
def comment():
    """ Add comment to user and article """
    data = request.get_json(force=True)
    user = get_jwt_identity()
    if data['action']=='add':
        print("got to comment in article.py", data['article_id'])
        database_client.push_new_comment(user['user_name'],data['article_id'],data['comment'])
        return {'msg':'liked article'}, 200
    elif data['action']=='remove':
        database_client.push_new_comment(user['user_name'],data['article_id'],data['comment'],add=False)
        return {'msg':'liked article'}, 200
    return {''}



@article_blueprint.route("/repost", methods=["POST"])
@jwt_required()
def repost():
    """ Add comment to user and article """
    data = request.get_json(force=True)
    user = get_jwt_identity()
    if data['action']=='add':
        database_client.repost_article(user['user_name'],data['article_id'])
        return {'msg':'liked article'}, 200
    elif data['action']=='remove':
        database_client.repost_article(user['user_name'],data['article_id'],add=True)
        return {'msg':'liked article'}, 200
    return {''}



@article_blueprint.route("/threads", methods=["POST"])
# @jwt_required()

def get_interest_thread():
    # articles = database_client.get_articles(q={'main_topic': interest}, page=int(n))
    data = request.get_json(force=True)

    if data['topic']=='':
        articles = database_client.client.Articles.allArticles.find()
    else:
        articles = database_client.client.Articles.allArticles.find({'main_topic':data['topic']}).limit(data['n'])
    
    article_ls = []
    for article in list(articles)[:data['n']]:
        del article["_id"]
        article_ls.append(article)
    return {"articles": article_ls}
