import pytest
import utils.login as Login


@pytest.fixture
def good_data():
    return {"email": "test@gmail.com", "username": "tester2", "password": "pass"}


def test_valid_email():
    assert Login.valid_email("test@gmail.com") is not None
    assert Login.valid_email("bad@h0tmail.com") is not None
    assert Login.valid_email("someone@yah00.com") is not None


def test_invalid_email():
    assert Login.valid_email("bad@b.com") is None
    assert Login.valid_email("somebody") is None
    assert Login.valid_email("somebody@.com") is None


def test_verify_data(good_data):
    assert 200 in Login.verify_data(good_data)


def test_verify_data_no_email(good_data):
    bad = good_data.copy().pop("email")
    assert 200 not in Login.verify_data(bad)


def test_verify_data_no_username(good_data):
    bad = good_data.copy().pop("username")
    assert 200 not in Login.verify_data(bad)


def test_verify_data_no_password(good_data):
    bad = good_data.copy().pop("password")
    assert 200 not in Login.verify_data(bad)


def test_verify_data_no_data():
    assert 200 not in Login.verify_data({})
    assert 200 not in Login.verify_data(None)


def test_user_dataframe(good_data):
    result = Login.create_user_dataframe(good_data)
    assert 200 in result


def test_user_dataframe_no_password(good_data):
    bad = good_data.copy().pop("password")
    result = Login.create_user_dataframe(bad)
    assert 200 not in result


def test_user_dataframe_no_username(good_data):
    bad = good_data.copy().pop("username")
    result = Login.create_user_dataframe(bad)
    assert 200 not in result


def test_user_dataframe_no_email(good_data):
    bad = good_data.copy().pop("email")
    result = Login.create_user_dataframe(bad)
    assert 200 not in result


def test_template():
    username = "test"
    email = "test@gmail.com"
    result = Login.new_user_template(username, email)

    assert result["user_name"] == username
    assert result["email"] == email
