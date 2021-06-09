from flask import request, Blueprint
import bcrypt
from flask_jwt_extended import create_access_token
from backend_vars import database_client, log
import utils.login as Login

login_blueprint = Blueprint("login_blueprint", __name__)


@login_blueprint.route("/login", methods=["POST"])
def try_login():
    """ login to application, returns a jwt token """
    if request.method == "POST":
        log.info("trying to login")
        data = request.get_json(force=True)
        curr_user = database_client.get_user({"email": data.get("email")})
        if len(curr_user) == 0:
            return {"msg": "no user found"}, 404

        curr_user = curr_user[0]
        if not bcrypt.checkpw(
            str.encode(data["password"]), str.encode(curr_user["pass_hash"])
        ):
            return {"msg": "password don't match"}, 400

        # clean up user data for less exposure
        curr_user.pop("pass_hash", None)
        curr_user.pop("_id", None)

        access_token = create_access_token(identity=curr_user)
        return {"access_token": access_token, "user": curr_user}, 200


@login_blueprint.route("/newUser", methods=["POST"])
def new_user():
    """ new users route, tries to add new users """
    if request.method == "POST":
        log.info("new user")
        data = request.get_json(force=True)

        result = Login.create_user_dataframe(data)
        if 200 not in result:
            return result

        user = result[0]["user"]
        log.info("successfully parsed new user information")

        result = database_client.add_user(user)
        if result["result"] == -1:
            return {"msg": result["msg"]}, 404

        log.info("successfully added new user")
        # clean up user data for less exposure
        user.pop("_id", None)
        user.pop("pass_hash", None)
        access_token = create_access_token(identity=user)
        return {
            "msg": "user successfully added",
            "access_token": access_token,
            "user": user,
        }, 200
