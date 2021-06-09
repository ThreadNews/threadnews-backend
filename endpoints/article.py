from flask import request, Blueprint
from backend_vars import database_client
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger('root')
article_blueprint = Blueprint("article_blueprint", __name__)


@article_blueprint.route("/articles", methods=["POST"])
def article_list():
    if request.method == "POST":
        data = request.get_json()
        articles = database_client.get_article_list(data["ids"])

        return {"result": articles}, 200
    return 404


@article_blueprint.route("/like", methods=["POST"])
@jwt_required()
def like_article():
    """Add/Delete like to article and user"""
    # if request.method == "POST":
    data = request.get_json(force=True)
    current_user = get_jwt_identity()
    if data["action"] == "add":
        database_client.push_new_like(current_user["user_id"], data["id"])
    if data["action"] == "delete":
        database_client.delete_like(current_user["user_id"], data["id"])
    return {"msg": "success"}, 200


@article_blueprint.route("/comment", methods=["POST"])
@jwt_required()
def comment():
    """Add comment to user and article"""
    data = request.get_json(force=True)
    user = get_jwt_identity()

    database_client.push_new_comment(
        user["user_name"], data["article_id"], data["comment"]
    )
    return {"msg": "comment added"}, 200


@article_blueprint.route("/repost", methods=["POST"])
@jwt_required()
def repost():
    """Add comment to user and article"""
    data = request.get_json(force=True)
    user = get_jwt_identity()
    if data["action"] == "add":
        database_client.repost_article(user["user_name"], data["id"])
        return {"msg": "liked article"}, 200
    elif data["action"] == "remove":
        database_client.repost_article(user["user_name"], data["id"], add=False)
        return {"msg": "removed article"}, 200
    return {""}


@article_blueprint.route("/save", methods=["POST"])
@jwt_required()
def save_article():
    """Save article to user and article"""
    data = request.get_json(force=True)
    user = get_jwt_identity()
    if data["action"] == "add":
        database_client.push_new_save(user["user_name"], data["id"])
        return {"msg": "liked article"}, 200
    elif data["action"] == "remove":
        database_client.delete_save(user["user_name"], data["id"])
        return {"msg": "removed liked article"}, 200
    return {""}


@article_blueprint.route("/threads", methods=["POST"])
def get_interest_thread():
    # articles = database_client.get_articles(q={'main_topic': interest}, page=int(n))
    data = request.get_json(force=True)

    if data["topic"] == "":
        articles = database_client.client.Articles.allArticles.find()
    else:
        articles = database_client.client.Articles.allArticles.find(
            {"main_topic": data["topic"]}
        ).limit(data["n"])

    article_ls = []
    for article in list(articles)[: data["n"]]:
        del article["_id"]
        article_ls.append(article)
    return {"articles": article_ls}
