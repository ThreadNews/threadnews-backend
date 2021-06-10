import pytest
from utils.feed import NewsAPI
from utils.config import threadConfiguration


@pytest.fixture
def newsFeed():
    return NewsAPI(threadConfiguration())


def test_rotate(newsFeed):
    """Test api rotation"""
    if isinstance(newsFeed.api_key, list):
        currentApi = newsFeed.api_key[0]
        assert newsFeed.feed._rotate_api() == currentApi
        assert newsFeed.api_key[0] != currentApi
    else:
        currentApi = newsFeed.api_key
        assert newsFeed.feed._rotate_api() == currentApi


def test_get_headlines(newsFeed):
    result = newsFeed.feed.get_headlines()
    assert result is not None


def test_get_sources(newsFeed):
    result = newsFeed.feed.get_sources()
    assert result is not None


def test_get_bad_request(newsFeed):
    result = newsFeed.feed.get_requests("unknown")
    assert result is None


def test_get_feed(newsFeed):
    result = newsFeed.feed.get_feed(q="Basketball")
    assert result is not None
    result = newsFeed.feed.get_feed(q=None)
    assert 400 in result


# def test_collection(newsFeed):
#     result = newsFeed.begin_collection()
#     assert result is not None
