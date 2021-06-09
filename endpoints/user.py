from flask import request, Blueprint
from backend_vars import database_client
from flask_jwt_extended import jwt_required, get_jwt_identity


user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/update_interests", methods=["POST"])
@jwt_required()
def update_user_interests():
    if request.method == "POST":
        current_user = get_jwt_identity()
        data = request.get_json(
            force=True
        )  # new interest should be added as {"add": [new interest], "remove": [interest]}
        database_client.update_user_interest(
            current_user["user_id"], data["add"], data["remove"]
        )
        return {"msg": "success"}, 200


@user_blueprint.route("/users", methods=["GET", "POST"])
@jwt_required()
def get_users():
    """Get the users of ThreadNews"""
    if request.method == "GET":
        return jsonify(database_client.get_users()), 200
    if request.method == "POST":
        current_user = get_jwt_identity()
        data = request.get_json(force=True)
        try:
            users = database_client.get_user_list(data["user_ids"])
            print("USERS:", users)
            return {"result": users}, 200
        except:
            return {"result": []}


@user_blueprint.route("/follow_user", methods=["POST"])
@jwt_required()
def follow_user():
    """User that is signed in will follow/unfollow other user"""
    current_user = get_jwt_identity()
    data = request.get_json(force=True)
    unfollow = False if data["action"] == "follow" else True
    status = database_client.follow_user(
        current_user["user_id"], data["user_id"], unfollow
    )
    if status == 200:
        return {"result": "success"}, 200
    return {"result": "err"}, 430


@user_blueprint.route("/reccomended_follows", methods=["POST"])
@jwt_required()
def get_recommended_follows():
    """returns a list of users the user may like to follow"""
    current_user = get_jwt_identity()
    print(current_user)
    data = request.get_json(force=True)
    users = database_client.get_user_list(current_user["suggested_follows"])
    return {"result": users}


@user_blueprint.route("/edit_profile", methods=["POST"])
@jwt_required()
def update_():
    if request.method == "POST":
        data = request.get_json(force=True)
        current_user = get_jwt_identity()
        user = database_client.update_user(
            user_id=current_user["user_id"],
            bio=data["bio"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            profile_pic=data["profile_pic"],
        )
        return {"result": user}


@user_blueprint.route("/search_user", methods=["POST"])
def search_user():
    if request.method == "POST":
        data = request.get_json(force=True)
        print("DATA:", data)
        users = database_client.search_user(data["user_name"])
        return {"msg": "success", "users": users}, 200


@user_blueprint.route("/edit_profile", methods=["POST"])
@jwt_required()
def update_user_bio():
    if request.method == "POST":
        data = request.get_json(force=True)
        current_user = get_jwt_identity()

