from flask import Blueprint
from flask import Response
from flask import request

from dynamic.common import git_common
from dynamic.elasticsearch_connection import es_connect
from dynamic.queries import update_files

hook = Blueprint('sentryhook', __name__)


@hook.route('/sentry_webhook', methods=['POST'])
def sentry_webhook():
    sentry_response = request.get_json()
    if es_connect.test_connection():
        query_body = {
            "query" : {
                "term" : {
                    "sentry_project": sentry_response['project']
                }
            }
        }
        git_repo = ""
        project_search = es_connect.es.search(index='dev_meter', body = query_body)
        if project_search['hits']['total'] > 0:
            git_repo = project_search['hits']['hits'][0]['_source']['git_repo']
        else:
            return "fuck u"
        print(git_repo)
        values = sentry_response['event']['sentry.interfaces.Exception']['values']
        print(sentry_response)
        for value in values:
            frames = value['stacktrace']['frames']
            for frame in frames:
                good_path = frame['filename'].replace("\\", "/")
                print(good_path)
                git_repo_name = git_repo.split("/")[-1]
                if git_repo_name in good_path:
                    good_path = good_path.split(git_repo_name)[-1]

                username = git_common.git_blame(git_repo, frame['filename'], frame['line'])
                email = project_search['hits']['hits'][0]['_id']
                update = update_files.update_files_with_query(good_path)
                es_connect.es.update(index='dev_meter', doc_type='project_registration', id=email, body=update)


    return Response(status=200)