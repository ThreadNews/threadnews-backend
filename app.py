from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend_vars import configFile
from endpoints.login import login_blueprint

def create_app():
    app = Flask(__name__)

    CORS(app)
    app.config["JWT_SECRET_KEY"] = configFile.get_configuration()['JWT']['secret']
    app.register_blueprint(login_blueprint)
    jwt = JWTManager()
    jwt.init_app(app)

    return app