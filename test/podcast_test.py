import pytest
from utils.feed import NewsAPI
from utils.config import threadConfiguration
from utils.database import threadDatabase
import sys, os
import logging


@pytest.fixture
def database():
    return threadDatabase(threadConfiguration().get_configuration())


def test_push_new_podcasts(database):
    result = database.push_new_podcasts(limit=3)
    assert result[1] == 200


# def get_new_podcasts(self):
#     spot = SpotifyPodcasts()
#     return spot.create_a_list_of_all_podcasts()

# def push_new_podcasts(self):
#     inserted = 0
#     podcasts = self.get_new_podcasts()
#     logger.info("trying to insert {} podcasts".format(len(podcasts)))
#     for podcast in podcasts:
#         self.client.Podcasts.allPodcasts.insert_one(podcast)
#         inserted += 1

#     logger.info("inserted {} new  podcasts".format(inserted))
#     return {"msg": "success"}, 200
