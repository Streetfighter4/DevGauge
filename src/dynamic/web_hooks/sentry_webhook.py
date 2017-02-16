import requests

from src.dynamic.common import git_common
from src.dynamic.elasticsearch_connection import es_connect
from flask import Blueprint
from flask import request
from flask import Response

hook = Blueprint('sentryhook', __name__)


@hook.route('/sentry_webhook', methods=['POST'])
def sentry_webhook():
    print ('in sentry')
    print (request.get_json())
    sentry_response = request.get_json()
    if es_connect.test_connection():
        id = sentry_response['id']
        values = sentry_response['event']['sentry.interfaces.Exception']['values']
        print(values)
        error_info = {}
        #found = es_connect.es.exists(index='dev_meter', doc_type='jira_issues', id=id)
        for value in values:
            frames = value['stacktrace']['frames']
            for frame in frames:
                error_info = {
                    "line" : frame['lineno'],
                    "function" : frame['function'],
                    "filename" : frame['filename'],
                    "author" : git_common.git_blame(frame['filename'], frame['line'])
                }
        print(error_info)

    print('aasdasdasda')

    return Response(status=200)