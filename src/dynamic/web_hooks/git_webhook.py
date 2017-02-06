import requests
from src.dynamic.elasticsearch_connection import es_connect
from flask import Blueprint
from flask import Response
from flask import request

hook = Blueprint('githook', __name__)

@hook.route('/git_webhook', methods=['GET','POST'])
def gitTracking():
    print('In gitTracking()')
    if es_connect.test_connection():
        git_response = request.get_json()
        commit_url = git_response['repository']['commits_url'].rsplit("{",1)[0] + '/'
        for commit in git_response['commits']:
            sha = commit['id']

            commit_info = requests.get(commit_url + sha).json() #TODO: add authentication
            commit_body = {
                "user_id" : commit_info['author']['id'],
                "author_email" : commit_info['commit']['author']['email'],
                "additions" : commit_info['stats']['additions'],
                "deletions" : commit_info['stats']['deletions']
            }
            found = es_connect.es.exists(index='dev_meter', doc_type='git_users', id=commit_body['user_id'])
            if found:
                es_res = es_connect.es.get(index='dev_meter', doc_type='git_users', id=commit_body['user_id'])
                old_commit_info = es_res['_source']
                commit_body['additions'] += old_commit_info['additions']
                commit_body['deletions'] += old_commit_info['deletions']

            es_connect.es.index(index='dev_meter', doc_type='git_users', id=commit_body['user_id'], body=commit_body)

    return Response(status=200)
