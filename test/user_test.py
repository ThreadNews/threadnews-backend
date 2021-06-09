import pytest
from utils.user import User 
from utils.database import threadDatabase
from utils.config import threadConfiguration
import sys, os


@pytest.fixture
def database():
    return threadDatabase(threadConfiguration().get_configuration())


def test_get_users(database): 
    length_of_users = len(database.get_users())
    assert length_of_users > 1 

def test_substring_search_results(database): 
    search_string = "gb"
    test_user = database.get_substring_search_results(search_string)
    assert test_user[0].get("user_id") == '9ece6032-9ba4-11eb-a5a0-acde48001122'

def test_get_user_list(database):
    user_list = database.get_user_list({'user_id': '9ece6032-9ba4-11eb-a5a0-acde48001122', 'user_name': 'gb', 'first_name': 'dfsf', 'last_name': 'asfs', 'email': 'gb@gmail.com'})
    test_user_in_list = user_list[0]
    assert test_user_in_list['_id'] == {'$oid': '6074689a6eda1bc92400f6b4'}

def test(database): 
    user_count = database.get_user_count()
    assert user_count == 98 


def test_get_user_interests(database): 
    user_interests = database.get_user_interests({'user_id': '9ece6032-9ba4-11eb-a5a0-acde48001122'})
    interests = set(user_interests.get("interests"))
    assert interests == {'Skincare', 'Healthy Living', 'Crypto', 'Cleansing', 'Cars', 'DIY', 'Health', 'Big Tech'}

def test_update_user_interests_none(database): 
    msg = database.update_user_interest('9ece6032-9ba4-11eb-a5a0-acde48001122')
    assert msg[0] == 200


