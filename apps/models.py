from dependencies.database import db
from flask_ckeditor import CKEditorField
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from dotenv import load_dotenv
import os


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ProjectForm(FlaskForm):
    title = StringField('Main Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    date = DateField('Project Date', validators=[DataRequired()])
    img_url = StringField('Main Image', validators=[URL(), DataRequired()])
    body = CKEditorField('Post Content', validators=[DataRequired()])
    submit = SubmitField('Submit Post')


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    subtitle = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String, nullable=False)


class User(UserMixin):
    load_dotenv()
    USERS = {'admin': os.getenv('ADMIN_PASSWORD')}

    def __init__(self, user_id):

        self.id = user_id
        self.password = self.USERS[user_id]

    @classmethod
    def get(cls, user_id):
        return cls(user_id)
