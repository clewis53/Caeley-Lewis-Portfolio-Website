from apps.models import LoginForm, Project, ProjectForm, User
from dependencies.database import db
from dependencies.login_manager import login_manager
from dependencies.ckeditor import ckeditor
from flask import Blueprint, redirect, request, url_for, render_template, flash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.exc import IntegrityError

# Register blueprint
app_view = Blueprint('apps', __name__, template_folder='templates')


def authenticated():
    return current_user.is_authenticated


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app_view.route('/about-me')
def about_me():
    return render_template('about-me.html',
                           logged_in=authenticated())


@app_view.route('/edit-project/<int:project_id>')
def edit_project(project_id):
    project = Project.query.get(project_id)
    project_form = ProjectForm(title=project.title,
                               subtitle=project.subtitle,
                               date=project.date,
                               body=project.body,
                               img_url=project.img_url)

    if project_form.validate_on_submit():
        title = project_form.title.data
        subtitle = project_form.subtitle.data
        date = project_form.date.data,
        body = project_form.body.data,
        img_url = project_form.img_url.data


@app_view.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    project_form = ProjectForm()

    if project_form.validate_on_submit():
        new_project = Project(title=project_form.title.data,
                              subtitle=project_form.subtitle.data,
                              date=project_form.date.data,
                              body=project_form.body.data,
                              img_url=project_form.img_url.data)
        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect(url_for('apps.show_project', project_id=new_project.id))

        except IntegrityError:
            flash('That project title has already been used.')

    return render_template('create-project.html', project_form=project_form)


@app_view.route('/')
def home():
    return render_template('index.html',
                           logged_in=authenticated())


@app_view.route('/admin', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.get('admin')

        if login_form.password.data == user.password:
            login_user(user)
            return redirect(url_for('apps.home'))

        flash('Incorrect Password')

    return render_template('login.html', login_form=login_form)


@app_view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('apps.home'))


@app_view.route('/cv')
def show_cv():
    return render_template('cv.html',
                           logged_in=authenticated())


@app_view.route('/portfolio')
def show_portfolio():
    portfolio = Project.query.all()
    return render_template('portfolio.html',
                           portfolio=portfolio,
                           logged_in=authenticated())


@app_view.route('/project/<int:project_id>')
def show_project(project_id):
    project = Project.query.get(project_id)
    return render_template('project.html',
                           project=project,
                           logged_in=authenticated())


@app_view.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', logged_in=authenticated()), 404
