from app.models import LoginForm, Project, ProjectForm, User
from database.database import db
from flask import Blueprint, redirect, request, url_for, render_template, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.exc import IntegrityError

# Register blueprint
app = Blueprint('app', __name__, template_folder='templates')

# setup dependencies
Bootstrap(app)

ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/about-me')
def about_me():
    return render_template('about-me.html',
                           logged_in=current_user.is_authenticated)


@app.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    project_form = ProjectForm()

    if project_form.validate_on_submit():
        new_project = Project(title=project_form.title,
                              subtitle=project_form.subtitle,
                              date=project_form.date,
                              body=project_form.body,
                              img_url=project_form.img_url)
        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('show_project', project_id=new_project.id))

        except IntegrityError:
            flash('That project title has already been used.')

    return render_template('create-project.html', project_form=project_form)


@app.route('/')
def home():
    return render_template('index.html',
                           logged_in=current_user.is_authenticated)


@app.route('/admin', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.get('admin')

        if login_form.password == user.password:
            login_user(user)
            return redirect(url_for('home'))

        flash('Incorrect Password')

    return render_template('login.html', login_form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/cv')
def show_cv():
    return render_template('cv.html',
                           logged_in=current_user.is_authenticated)


@app.route('/portfolio')
def show_portfolio():
    portfolio = Project.query.all()
    return render_template('portfolio.html',
                           portfolio=portfolio,
                           logged_in=current_user.is_authenticated)


@app.route('/project/<int:project_id>')
def show_project(project_id):
    project = Project.query.get(project_id)
    return render_template('project.html',
                           project=project,
                           logged_in=current_user.is_authenticated)


@app.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
