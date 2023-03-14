from dependencies import database, login_manager, ckeditor
from flask import Flask
from flask_bootstrap import Bootstrap

# apps blueprint
from apps.views import app_view


def create_app():
    app = Flask(__name__)
    # setup with configuration provided
    app.config.from_object('config.DevelopmentConfig')

    # setup dependencies
    db = database.init_app(app)

    login_manager.init_app(app)
    ckeditor.init_app(app)
    Bootstrap(app)

    # register blueprint
    app.register_blueprint(app_view)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':

    create_app().run()
