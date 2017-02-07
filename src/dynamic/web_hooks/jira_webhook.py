import requests
from src.dynamic.elasticsearch_connection import es_connect
from flask import Blueprint
from flask import request
from flask import Response
from datetime import datetime

hook = Blueprint('jirahook', __name__)


@hook.route('/jira_webhook', methods=['GET','POST'])
def tracking():
    issueUrl = request.get_json()['issue']['self']

    if es_connect.test_connection():
        jira_response = requests.get(issueUrl , auth=('groznika123@gmail.com', 'Streetfighter4')).json()
        id = jira_response['id']
        status = jira_response['fields']['status']['statusCategory']['name']
        issue = {}
        found = es_connect.es.exists(index='dev_meter', doc_type='jira_issues', id=id)
        if found:
            es_res = es_connect.es.get(index='dev_meter', doc_type='jira_issues', id=id)
            issue = es_res['_source']
            issue['status'] = status
        else:
            issue = {
                "summary" : jira_response['fields']['summary'],
                "status" : status,
                "assignee_email" : jira_response['fields']['assignee']['emailAddress'],
                "curr_start_time" : None,
                "total_time" : 0
            }
            #TODO: reformat as git webhook

        if issue['status'] == 'In Progress':
            issue['curr_start_time'] = jira_response['fields']['updated']
        elif issue['curr_start_time'] != None:
            format = '%Y-%m-%dT%H:%M:%S'
            updated_at = datetime.strptime(jira_response['fields']['updated'].rsplit(".", 1)[0], format)
            start_time = datetime.strptime(issue['curr_start_time'].rsplit(".", 1)[0], format)
            issue['total_time'] += (updated_at - start_time).seconds

        es_connect.es.index(index='dev_meter', doc_type='jira_issues', id=id, body=issue)

    return Response(status=200)
