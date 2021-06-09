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

