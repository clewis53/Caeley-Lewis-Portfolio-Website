from flask import Blueprint, request, url_for, render_template, flash
from app.models import LoginForm, PostForm, ProjectPost

# Register blueprint
app = Blueprint('app', __name__, template_folder='templates')


@app.route('/')
def home():
    return render_template('index.html')


@app.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
