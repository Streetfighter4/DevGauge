import requests
from dynamic.elasticsearch_connection import es_connect
from flask import Blueprint
from flask import request
from flask import Response
from datetime import datetime
from dynamic.queries.update_files import update_issues, get_issue_start_time

hook = Blueprint('jirahook', __name__)


@hook.route('/jira_webhook', methods=['POST'])
def whenIssueUpdate():
    issueUrl = request.get_json()['issue']['self']
    project_name = request.get_json()['issue']['fields']['project']['name']

    if es_connect.test_connection():
        query_body = {
            "query": {
                "term": {
                    "jira_project": project_name.lower()
                }
            }
        }
        project_search = es_connect.es.search(index='dev_meter', body=query_body)

        if project_search['hits']['total'] > 0:
            project_email = project_search['hits']['hits'][0]['_id']
        else:
            return Response(status_code=500)

        jira_response = requests.get(issueUrl).json()
        status = jira_response['fields']['status']['statusCategory']['name']

        issue = {
            "summary" : jira_response['fields']['summary'],
            "status" : status,
            "curr_start_time" : get_issue_start_time(jira_response['fields']['summary']),
            "total_time" : 0
        }

        assignee_email = jira_response['fields']['assignee']['emailAddress']
        if issue['status'] == 'In Progress':
            issue['curr_start_time'] = jira_response['fields']['updated']
        elif issue['curr_start_time'] != None:
            format = '%Y-%m-%dT%H:%M:%S'
            updated_at = datetime.strptime(jira_response['fields']['updated'].rsplit(".", 1)[0], format)
            start_time = datetime.strptime(issue['curr_start_time'].rsplit(".", 1)[0], format)
            issue['total_time'] = (updated_at - start_time).seconds
            issue['curr_start_time'] = None

        update_issue = update_issues(issue, assignee_email)

        es_connect.es.update(index='dev_meter', doc_type='project_registration',
                             id=project_email, body=update_issue)

    return Response(status=200)


@hook.route('/oauth_callback', methods=['GET', 'POST'])
def oauth_callback():
    print (request.get_json())
    return Response(status=200)