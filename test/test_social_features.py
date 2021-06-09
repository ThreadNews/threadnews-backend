import pytest
from utils.database import threadDatabase
from utils.config import threadConfiguration
import collections

TEST_USER_ID1 = "0e7bf4b8-7c28-11eb-95d3-acde48001122"
TEST_USER_ID2 = "98200178-781d-11eb-b6dc-acde48001122"
TEST_USER_ID3 = "3296fe3a-7c53-11eb-95d3-acde48001122"
TEST_USER_ID4 = "e269cc10-a34b-11eb-92dd-acde48001122"
EMPTY_USER_ID = "a49387e4-7c51-11eb-95d3-acde48001122"


@pytest.fixture
def db():
    """creates global variable to be use in multiple tests"""
    config = threadConfiguration()
    return threadDatabase(config.get_configuration())


def test_follow_user(db):
    result = db.follow_user(TEST_USER_ID1, TEST_USER_ID2)
    assert result == 200

    # check if user2 has user1 as a follower
    result = db.fetch_social(TEST_USER_ID2, followers=True)
    assert "followers" in result["result"].keys()
    assert TEST_USER_ID1 in result["result"]["followers"]

    # check if user1 is following user 2
    result = db.fetch_social(TEST_USER_ID1, following=True)
    assert "following" in result["result"].keys()
    assert TEST_USER_ID2 in result["result"]["following"]


def test_unfollow_user(db):
    result = db.follow_user(TEST_USER_ID1, TEST_USER_ID2, unfollow=True)
    assert result == 200

    # confirm user 2 is not being followed by user 1
    result = db.fetch_social(TEST_USER_ID2, followers=True)
    assert TEST_USER_ID1 not in result["result"]["followers"]

    # confirm if user1  not is following user 2
    result = db.fetch_social(TEST_USER_ID1, following=True)
    assert TEST_USER_ID2 not in result["result"]["following"]
