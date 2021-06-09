import pytest
from utils.feed import NewsAPI
from utils.config import threadConfiguration
from utils.database import threadDatabase
import sys, os

"""
Test database functionality
"""

@pytest.fixture
def database():
    return threadDatabase(threadConfiguration().get_configuration())


def test_get_random_article(database):
    result = database.get_random_article()
    assert result is not None


def test_get_article(database):
    result = database.get_articles()
    assert result == 200


def test_get_article_by_id(database):
    result = database.get_article_by_id("54bc318b-71f1-4d68-81d6-d75d6dc7b34e")
    assert result is not None


def test_add_likes_articles(database):
    result = database.add_likes_articles(
        "98200178-781d-11eb-b6dc-acde48001122", "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    )
    assert result == 200


def test_repost_article(database):
    result = database.repost_article(
        "98200178-781d-11eb-b6dc-acde48001122", "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    )
    assert result == 200


def test_push_new_comment(database):
    result = database.push_new_comment(
        "98200178-781d-11eb-b6dc-acde48001122",
        "54bc318b-71f1-4d68-81d6-d75d6dc7b34e",
        "comment one",
    )
    assert result == 200


def test_push_new_like(database):
    result = database.push_new_like(
        "98200178-781d-11eb-b6dc-acde48001122", "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    )
    assert result == 200


def test_push_new_view(database):
    result = database.push_new_view(
        "98200178-781d-11eb-b6dc-acde48001122", "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    )
    assert result[0] == 200


def test_push_new_save(database):
    result = database.push_new_save(
        "98200178-781d-11eb-b6dc-acde48001122", "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    )
    assert result[1] == 200


def test_delete_save(database):
    result = database.delete_save(
        "98200178-781d-11eb-b6dc-acde48001122", "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    )
    assert result == 200


def test_delete_like(database):
    result = database.delete_like(
        "98200178-781d-11eb-b6dc-acde48001122", "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    )
    assert result == 200
