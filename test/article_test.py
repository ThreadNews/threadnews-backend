import pytest
from utils.feed import NewsAPI
from utils.config import threadConfiguration
from utils.database import threadDatabase
import sys, os


@pytest.fixture
def database(): 
    return threadDatabase(threadConfiguration().get_configuration())

def test_get_random_article(database):
    result = database.get_random_article()
    assert result is not None 

