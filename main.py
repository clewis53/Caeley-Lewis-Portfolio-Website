from flaskr import ckeditor, database, login_manager
from flask import Flask
from flask_bootstrap import Bootstrap

# apps blueprint
from flaskr.views import app_view


def create_app():
    app = Flask(__name__)
    # setup with configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # setup dependencies
    database.init_app(app)

    login_manager.init_app(app)
    ckeditor.init_app(app)
    Bootstrap(app)

    # register blueprint
    app.register_blueprint(app_view)

    return app


if __name__ == '__main__':

    create_app().run()
