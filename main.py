import datetime
from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def create_team(db_sess):
    team_lead = User()
    team_lead.surname = 'Scott'
    team_lead.name = 'Ridley'
    team_lead.age = 21
    team_lead.position = 'captain'
    team_lead.speciality = 'research engineer'
    team_lead.address = 'module_1'
    team_lead.email = 'scott_chief@mars.org'
    db_sess.add(team_lead)
    db_sess.commit()
    for i in range(1, 4):
        colonist = User()
        colonist.surname = f'Surname of Colonist {i}'
        colonist.name = f'Name of Colonist {i}'
        colonist.age = 20 + i
        colonist.position = f'Colonist {i}'
        colonist.speciality = f'Student {i}'
        colonist.address = f'Mars street {i}'
        colonist.email = f'colonist{i}@mars.org'
        db_sess.add(colonist)
        db_sess.commit()
        work = Jobs()
        work.team_leader = 1
        work.job = 'deployment of residential modules 1 and 2'
        work.work_size = 15
        work.collaborators = '2, 3'
        db_sess.add(work)
        db_sess.commit()


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(port=8080, host='127.0.0.1')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    create_team(db_sess)
    return render_template("index.html", jobs=db_sess.query(User).first().jobs)


if __name__ == '__main__':
    main()