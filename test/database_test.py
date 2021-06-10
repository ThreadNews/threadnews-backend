import pytest
import random
from utils.feed import NewsAPI
from utils.config import threadConfiguration
from utils.database import threadDatabase
import sys, os


@pytest.fixture
def database():
    return threadDatabase(threadConfiguration().get_configuration())


def test_get_random_article(database):
    result = database.get_random_article(random_num=1)
    test_result = "https://www.cbssports.com/college-basketball/news/bracketology-ohio-state-and-illinois-meet-with-the-chance-to-be-the-final-no-1-seed-at-stake/"
    print(result.get("url"))
    assert result.get("url") == test_result
    #assert result is not None


def test_get_articles(database):
    result = database.get_articles()
    assert result[1] == 200


def test_get_article_by_id(database):
    result = database.get_article_by_id("54bc318b-71f1-4d68-81d6-d75d6dc7b34e")
    test_result_url = "https://www.npr.org/2021/03/06/974362036/this-is-the-reality-of-black-girls-inauguration-poet-says-she-was-tailed-by-guar"
    assert result.get("url") == test_result_url
    #assert result is not None


def test_add_likes_articles(database):
    test_user_id = "98200178-781d-11eb-b6dc-acde48001122"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    before_likes = database.get_article_by_id(test_article_id).get("likes")
    result = database.add_likes_articles(
        test_user_id, test_article_id
    )
    after_likes = database.get_article_by_id(test_article_id).get("likes")
    assert before_likes == (after_likes - 1)


def test_repost_article(database):
    test_user_id = "98200178-781d-11eb-b6dc-acde48001122"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    before_reposts = database.get_article_by_id(test_article_id).get("reposts")
    result = database.repost_article(
        test_user_id, test_article_id, add=True 
    )
    after_reposts = database.get_article_by_id(test_article_id).get("reposts")
    assert before_reposts == (after_reposts + 1)


def test_push_new_comment(database):
    test_user_name = "gb"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    comment= "testing" + str(int(random.randint(0, 50)))
    before_comments = database.get_article_by_id(test_article_id).get("comments")
    database.push_new_comment(test_user_name, test_article_id, comment)
    after_comments = database.get_article_by_id(test_article_id).get("comments")
    assert (len(before_comments)) == (len(after_comments)) - 1


def test_push_new_like(database):
    test_user_id = "98200178-781d-11eb-b6dc-acde48001122"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    before_likes = database.get_article_by_id(test_article_id).get("likes")
    result = database.push_new_like(
        test_user_id, test_article_id
    )
    after_likes = database.get_article_by_id(test_article_id).get("likes")
    assert before_likes == (after_likes - 1)


def test_push_new_view_no_change(database):
    # views should not increase after the first view of the article 
    test_user_id = "98200178-781d-11eb-b6dc-acde48001122"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    before_view = database.get_user_by_id(test_user_id).get("viewed_articles")
    result = database.push_new_view(
        test_user_id, test_article_id
    )
    after_view = database.get_user_by_id(test_user_id).get("viewed_articles")
    assert (len(before_view)) == (len(after_view)) - 1



def test_push_new_save(database):
    test_user_id = "98200178-781d-11eb-b6dc-acde48001122"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    before_save = database.get_article_by_id(test_article_id).get("saves")
    result = database.push_new_save(
        test_user_id, test_article_id
    )
    after_save = database.get_article_by_id(test_article_id).get("saves")
    assert before_save == (after_save - 1)

def test_delete_save(database):
    test_user_id = "98200178-781d-11eb-b6dc-acde48001122"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    before_save = database.get_article_by_id(test_article_id).get("saves")
    result = database.delete_save(
        test_user_id, test_article_id
    )
    after_save = database.get_article_by_id(test_article_id).get("saves")
    assert before_save == (after_save + 1)

def test_delete_like(database):
    test_user_id = "98200178-781d-11eb-b6dc-acde48001122"
    test_article_id =  "54bc318b-71f1-4d68-81d6-d75d6dc7b34e"
    before_likes = database.get_article_by_id(test_article_id).get("likes")
    result = database.delete_like(
        test_user_id, test_article_id
    )
    after_likes = database.get_article_by_id(test_article_id).get("likes")
    assert before_likes == (after_likes + 1)
