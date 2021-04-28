from flask import request, Blueprint, jsonify
from backend_vars import database_client, appFeed, log
from flask_jwt_extended import jwt_required, get_jwt_identity

test_blueprint = Blueprint('test_blueprint', __name__)

@test_blueprint.route('/feed', methods=['GET'])
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
        return appFeed.feed.get_feed(q=q, q_in_title=q_in_title, sources=sources, domains=domains, exclude_domains=exclude_domains, date_from=date_from, date_to=date_to, lang=lang, sort_by=sort_by, page_size=page_size, page=page)

@test_blueprint.route('/sources', methods=['GET'])
def get_app_sources():
    """ Get sources from NewsAPI and return it """
    log.info("trying to retrieve sources")
    if request.method == 'GET':
        return appFeed.feed.get_sources()

@test_blueprint.route('/headlines', methods=['GET'])
def get_app_headlines():
    """ Get headlines from NewsAPI and return itoh yea """
    if request.method == 'GET':
        return appFeed.feed.get_headlines()

@test_blueprint.route('/users', methods=['GET'])
def get_users():
    """ Get the users of ThreadNews """
    if request.method == 'GET':
        return jsonify(database_client.get_users()), 200

@test_blueprint.route('/articles', methods=['GET'])
def get_articles():
    if request.method == 'GET':
        pages = request.args.get("pages")
        if pages is None:
            pages = 1
        return database_client.get_articles(int(pages))

@test_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return {"logged_in_as": current_user}, 200