from flask import request, Blueprint, Response
import json
import os
from utils.Podcast import SpotifyPodcast

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
        # return json object that is used used to construct bubbles
        
        # return data
    if request.method == "POST":
        data = request.get_json(force=True)
        interest_list = data['interest_list']
        spot = SpotifyPodcasts()
        random_pods = spot.get_a_random_podcast(interest_list)  
        # update data in db - not implemented yet
        return {"result": random_pods}, 200

