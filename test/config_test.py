import pytest
from utils.config import threadConfiguration
import os

"""
Tests to check configuration files or environmental variables
"""

@pytest.fixture
def config():
    return threadConfiguration()


def test_get_configuration(config):
    result = config.get_configuration()
    assert result.has_option("NewsAPI", "key")
    assert result.has_option("MongoDB", "URl")
    assert result.has_option("MongoDB", "user")
    assert result.has_option("MongoDB", "password")
    assert result.has_option("JWT", "secret")


def test_get_api_keys(config):
    result = config.get_api_keys()
    assert result is not None


def test_env_vars(config):
    expected = (
        True
        if None
        in [
            os.environ.get("NEWSAPIKEY"),
            os.environ.get("MONGOURL"),
            os.environ.get("MONGOUSER"),
            os.environ.get("MONGOPASS"),
            os.environ.get("JWTSECRET"),
        ]
        else False
    )

    result = config.read_env_vars()
    assert result == expected
