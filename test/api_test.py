import pytest
from utils.config import threadConfiguration

"""
Test if API keys are working and gathered
"""

@pytest.fixture
def config():
    return threadConfiguration()


def test_collected_NewsAPI(config):
    assert config.get_api_keys() != None


def test_has_env_vars(config):
    assert config.read_env_vars() != None
