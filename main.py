from database import database
from flask import Flask

# app blueprint
from app.views import app as app_view


def create_app():
    app = Flask(__name__)
    # setup with configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # setup dependencies
    database.init_app(app)

    # register blueprint
    app.register_blueprint(app_view)

    return app


if __name__ == '__main__':
    create_app().run()
