import requests

from dynamic.elasticsearch_connection import es_connect
from flask import Blueprint
from flask import Response
from flask import request
from dynamic.queries.update_files import update_users_git_info

hook = Blueprint('githook', __name__)

@hook.route('/git_webhook', methods=['POST'])
def gitTracking():
    git_response = request.get_json()
    if es_connect.test_connection():
        query_body = {
          "query" : {
             "query_string" : {
                "query" : git_response['repository']['url'].lower(),
                "analyzer": "keyword"
             }
          }
        }
        project_search = es_connect.es.search(index='dev_meter', body=query_body)
        if project_search['hits']['total'] > 0:
            project_email = project_search['hits']['hits'][0]['_id']
        else:
            return Response(status_code=500)  # TODO throw exaption

        commit_url = git_response['repository']['commits_url']
        for commit in git_response['commits']:
            sha = commit['id']
            commit_info = requests.get(commit_url.replace('{/sha}', '/' + sha)).json() #TODO: add authentication

            author_email = commit_info['commit']['author']['email']
            additions = commit_info['stats']['additions']
            deletions = commit_info['stats']['deletions']
            update_git_info = update_users_git_info(author_email, additions, deletions)
            es_connect.es.update(index='dev_meter', doc_type='project_registration', id=project_email, body=update_git_info)

    return Response(status=200)