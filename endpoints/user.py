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


@user_blueprint.route("/edit_profile", methods=["POST"])
@jwt_required()
def update_user_bio():
    if request.method == "POST":
        data = request.get_json(force=True)
        current_user = get_jwt_identity()

    # get the info from each field store it so its attached to the user
    # shows up everytime

    # NEW (?) fields for user data base
    # first name **
    # last name **
    # profile pic
    # bio
    # password **
    # email **
