from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import atexit

from endpoints import tasks

from backend_vars import configFile, scheduler, log
from endpoints.login import login_blueprint
from endpoints.frontend import front_blueprint
from endpoints.article import article_blueprint
from endpoints.tests import test_blueprint
from endpoints.user import user_blueprint

POLL_INTERVAL = 1800


def create_app():
    app = Flask(__name__)

    CORS(app)
    app.config["JWT_SECRET_KEY"] = configFile.get_configuration()["JWT"]["secret"]
    app.register_blueprint(login_blueprint)
    app.register_blueprint(front_blueprint)
    app.register_blueprint(article_blueprint)
    app.register_blueprint(test_blueprint)  # for testing
    app.register_blueprint(user_blueprint)
    jwt = JWTManager(app)
    from endpoints import tasks

    scheduler.api_enabled = True
    # scheduler.init_app(app)

    scheduler.add_job(func=tasks.feed_worker, trigger="interval", seconds=POLL_INTERVAL)
    scheduler.start()
    log.info("scheduler started")

    atexit.register(lambda: scheduler.shutdown())

    return app
