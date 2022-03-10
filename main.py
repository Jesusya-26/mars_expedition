import os.path
import requests
from flask import Flask, render_template, redirect, request, abort, make_response, jsonify, url_for
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_restful import Api
from data import db_session, jobs_api, users_api, users_resource
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from data.category import Category
from forms.user import RegisterForm, LoginForm
from forms.job import JobForm
from forms.department import DepartmentForm


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(users_resource.UsersListResource, '/api/v2/users')
api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:user_id>')


def main():
    db_session.global_init('db/mars_explorer.db')
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def work_log():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('work_log.html', title='Work log', jobs=jobs)


@app.route('/departments')
def list_departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Departments).all()
    return render_template('list_departments.html', title='List of Departments', departments=departments)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message='There is already such a user')
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            city_from=form.city_from.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        if not db_sess.query(Category).filter(Category.id == form.category.data).first():
            category = Category()
            category.name = f'Category №{form.category.data}'
        else:
            category = db_sess.query(Category).filter(Category.id == form.category.data).first()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.category = form.category.data
        job.is_finished = form.is_finished.data
        current_user.jobs.append(job)
        job.categories.append(category)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("/")
    return render_template('jobs.html', title='Adding a Job',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.user == current_user) | (
                                                 current_user == db_sess.query(User).first()))
                                         ).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.category.data = job.category
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((Jobs.user == current_user) | (
                                                 current_user == db_sess.query(User).first()))
                                         ).first()
        if job:
            if not db_sess.query(Category).get(form.category.data):
                category = Category()
                category.name = f'Category №{form.category.data}'
            else:
                category = db_sess.query(Category).get(form.category.data)
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.category = form.category.data
            job.is_finished = form.is_finished.data
            job.categories.clear()
            job.categories.append(category)
            db_sess.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Edit Job',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id,
                                     ((Jobs.user == current_user) | (
                                             current_user == db_sess.query(User).first()))
                                     ).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")


@app.route('/department',  methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Departments()
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        current_user.departments.append(department)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('departments.html', title='Adding a Departments',
                           form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        department = db_sess.query(Departments).filter(Departments.id == id,
                                                       ((Departments.user == current_user) | (
                                                              current_user == db_sess.query(User).first()))
                                                       ).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = db_sess.query(Departments).filter(Departments.id == id,
                                                       ((Departments.user == current_user) | (
                                                              current_user == db_sess.query(User).first()))
                                                       ).first()
        if department:
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('departments.html',
                           title='Edit Department',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    department = db_sess.query(Departments).filter(Departments.id == id,
                                                   ((Departments.user == current_user) | (
                                                          current_user == db_sess.query(User).first()))
                                                   ).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/users_show/<int:user_id>', methods=['GET'])
def show_hometown(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": user.city_from,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        return render_template('nostalgy.html', title='Hometown', user=user, image=None)

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta = "0.050"
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "sat"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    map_file = f"static/img/map_{user.city_from}.png"
    if os.path.isfile(map_file):
        img = url_for('static', filename=f'img/map_{user.city_from}.png')
        return render_template('nostalgy.html', title='Hometown', user=user, image=img)
    else:
        with open(map_file, "wb") as file:
            file.write(response.content)
        img = url_for('static', filename=f'img/map_{user.city_from}.png')
        return render_template('nostalgy.html', title='Hometown', user=user, image=img)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
