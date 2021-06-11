from flask import request, Blueprint, Response
import json
import os
from utils.podcast import Podcast
from backend_vars import database_client

front_blueprint = Blueprint("front_blueprint", __name__)


@front_blueprint.route("/categoryBubbleData", methods=["GET", "POST"])
def get_categoy_bubble_data():
    if request.method == "GET":
        # return json object that is used used to construct bubbles
        print(os.listdir())
        with open("topic_bubble_data.json") as f:
            data = json.load(f)
        print(type(data))
        print("DATA:", data)
        return Response(response=data)
        # return data
    elif request.method == "POST":
        # update data in db - not implemented yet
        return Response(response={}, status=404)


@front_blueprint.route("/podcasts", methods=["POST"])
def get_podcasts():
    if request.method == "POST":
        data = request.get_json(force=True)
        interest_list = data["interest_list"]
        spot = Podcast()
        if "topic" in data.keys():
            random_pods = database_client.get_all_podcasts(q={"topic": data["topic"]})
        else:
            random_pods = database_client.get_all_podcasts()

        return {"podcasts": random_pods}, 200
