import pytest
import utils.logger as logger


"""
Test if logger is being created
"""


def test_logger():
    result = logger.setup_logger("test")
    assert result is not None
