from flask import jsonify, request
from flask_restful import abort, Resource
from . import db_session
from .jobs import Jobs
from .category import Category
from .parsers import jobs_parser


class JobsResource(Resource):

    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify(
            {
                'job':
                    job.to_dict(
                        only=(
                        'job', 'team_leader', 'work_size', 'collaborators', 'category', 'is_finished'))
            }
        )

    def post(self, job_id):
        abort_if_job_not_found(job_id)
        args = jobs_parser.parse_args()
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        if not session.query(Category).get(request.json['category']):
            category = Category()
            category.name = f'Category №{request.json["category"]}'
        else:
            category = session.query(Category).get(request.json['category'])
        job.job = request.json['job']
        job.team_leader = request.json['team_leader']
        job.work_size = request.json['work_size']
        job.collaborators = request.json['collaborators']
        job.category = request.json['category']
        job.is_finished = request.json['is_finished']
        job.categories.clear()
        job.categories.append(category)
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        job.categories.clear()
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):

    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {
                'jobs':
                    [item.to_dict(
                        only=(
                            'job', 'team_leader', 'work_size', 'collaborators', 'category', 'is_finished'))
                        for item in jobs]
            }
        )

    def post(self):
        args = jobs_parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=request.json['job'],
            team_leader=request.json['team_leader'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            category=request.json['category'],
            is_finished=request.json['is_finished']
        )
        if not session.query(Category).get(request.json['category']):
            category = Category()
            category.name = f'Category №{request.json["category"]}'
        else:
            category = session.query(Category).get(request.json['category'])
        job.categories.append(category)
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")