from requests import get, post, delete

# print(get('http://localhost:8080/api/v2/users').json())
#
# print(get('http://localhost:8080/api/v2/users/1').json())
#
# print(get('http://localhost:8080/api/v2/users/999').json())
#
# print(get('http://localhost:8080/api/v2/users/q').json())
#
# print(delete('http://localhost:8080/api/v2/users/3').json())
#
# print(post('http://localhost:8080/api/v2/users',
#            json={'surname': 'New',
#                  'name': 'Man',
#                  'age': 1,
#                  'position': '',
#                  'speciality': '',
#                  'address': '',
#                  'city_from': 'Paris'}).json())
#
# print(post('http://localhost:8080/api/v2/users').json())
#
# print(post('http://localhost:8080/api/v2/users',
#            json={'surname': 'New',
#                  'name': 'Man',
#                  'age': 1,
#                  'position': '',
#                  'speciality': '',
#                  'address': '',
#                  'city_from': 'Paris',
#                  'email': 'babaev@yandex.ru',
#                  'password': '111'}).json())
#
# print(get('http://localhost:8080/api/v2/users').json())
#
# print(post('http://localhost:8080/api/v2/users/3',
#            json={'surname': 'NewNew',
#                  'name': 'ManMan',
#                  'age': 2,
#                  'position': '',
#                  'speciality': '',
#                  'address': '',
#                  'city_from': 'Paris'}).json())
#
# print(post('http://localhost:8080/api/v2/users/3',
#            json={'surname': 'NewNew',
#                  'name': 'ManMan',
#                  'age': 2,
#                  'position': '',
#                  'speciality': '',
#                  'address': '',
#                  'city_from': 'Paris',
#                  'email': 'babaev@yandex.ru',
#                  'password': '222'}).json())
#
# print(get('http://localhost:8080/api/v2/users').json())

print(get('http://localhost:8080/api/v2/jobs').json())

print(get('http://localhost:8080/api/v2/jobs/1').json())

print(get('http://localhost:8080/api/v2/jobs/999').json())

print(get('http://localhost:8080/api/v2/jobs/q').json())

print(delete('http://localhost:8080/api/v2/jobs').json())

print(delete('http://localhost:8080/api/v2/jobs/3100').json())

print(delete('http://localhost:8080/api/v2/jobs/q').json())

print(delete('http://localhost:8080/api/v2/jobs/3').json())

print(post('http://localhost:8080/api/v2/jobs').json())

print(post('http://localhost:8080/api/v2/jobs',
           json={'job': 'New Job',
                 'team_leader': 1,
                 'work_size': 1,
                 'collaborators': '',
                 'category': 1}).json())

print(post('http://localhost:8080/api/v2/jobs',
           json={'job': 'New Job',
                 'team_leader': 'ok',
                 'work_size': 1,
                 'collaborators': '',
                 'category': 1,
                 'is_finished': False}).json())

print(post('http://localhost:8080/api/v2/jobs',
           json={'job': 'New Job',
                 'team_leader': 1,
                 'work_size': 1,
                 'collaborators': '',
                 'category': 1,
                 'is_finished': False}).json())

print(get('http://localhost:8080/api/v2/jobs').json())

print(post('http://localhost:8080/api/v2/jobs/3').json())

print(post('http://localhost:8080/api/v2/jobs/3',
           json={'job': 'New Job',
                 'team_leader': 1,
                 'work_size': 1,
                 'collaborators': '',
                 'category': 1}).json())

print(post('http://localhost:8080/api/v2/jobs/3',
           json={'job': 'Fix New Job',
                 'team_leader': 'ok',
                 'work_size': 1,
                 'collaborators': '',
                 'category': 1,
                 'is_finished': True}).json())

print(post('http://localhost:8080/api/v2/jobs/3',
           json={'job': 'Fix New Job',
                 'team_leader': 1,
                 'work_size': 1,
                 'collaborators': '',
                 'category': 1,
                 'is_finished': True}).json())

print(get('http://localhost:8080/api/v2/jobs').json())