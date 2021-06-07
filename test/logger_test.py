import pytest
import utils.logger as logger

def test_logger():
    result = logger.setup_logger("test")
    assert result is not None