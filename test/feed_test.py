import pytest
from utils.feed import NewsAPI
from utils.config import threadConfiguration


@pytest.fixture
def newsFeed():
    return NewsAPI(threadConfiguration())


def test_rotate(newsFeed):
    if isinstance(newsFeed.api_key, list):
        currentApi = newsFeed.api_key[0]
        assert newsFeed.feed._rotate_api() == currentApi
        assert newsFeed.api_key[0] != currentApi
    else:
        currentApi = newsFeed.api_key
        assert newsFeed.feed._rotate_api() == currentApi
