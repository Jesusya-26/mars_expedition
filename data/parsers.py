from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('surname', required=True)
user_parser.add_argument('name', required=True)
user_parser.add_argument('age', required=True, type=int)
user_parser.add_argument('position', required=True)
user_parser.add_argument('speciality', required=True)
user_parser.add_argument('address', required=True)
user_parser.add_argument('city_from', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('password', required=True)

jobs_parser = reqparse.RequestParser()
jobs_parser.add_argument('job', required=True)
jobs_parser.add_argument('team_leader', required=True, type=int)
jobs_parser.add_argument('work_size', required=True, type=int)
jobs_parser.add_argument('collaborators', required=True)
jobs_parser.add_argument('category', required=True, type=int)
jobs_parser.add_argument('is_finished', required=True, type=bool)