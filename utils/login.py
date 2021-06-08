from email_validator import validate_email, EmailNotValidError
import bcrypt
import uuid

def new_user_template(user_name, email, first_name="", last_name="", interests=[]):
    """returns dictionary representing a user for creating new user document"""
    user = {
        "user_id": str(uuid.uuid1()),
        "user_name": user_name,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "interests": interests,
        "following": [],
        "followers": [],
        "following_count": 0,
        "followers_count": 0,
        "liked_articles": [],
        "reposted_articles": [],
        "likes_count": 0,
    }
    return user

def valid_email(email=""):
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError as e:
        return None

def verify_data(data):
    if data:
        if "username" not in data:
            return {"msg": "username not found"}, 406

        if "email" not in data:
            return {"msg": "email not found"}, 406

        if "password" not in data:
            return {"msg": "password not found"}, 406
    else:
        return {"msg": "missing data"}, 400    
    return {"msg": 1}, 200

def create_user_dataframe(data):
    verification = verify_data(data)
    if 200 not in verification:
        return verification
    
    username = data["username"]
    email = valid_email(data["email"])
    password = data["password"]

    print(email)
    if email is None:
        return {"msg": "invalid email"}, 400

    salt = bcrypt.gensalt()
    pass_hash = bcrypt.hashpw(str.encode(password), salt)
    user = new_user_template(username, email)
    user["pass_hash"] = pass_hash.decode()

    return {"user": user}, 200