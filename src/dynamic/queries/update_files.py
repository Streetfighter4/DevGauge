from dynamic.elasticsearch_connection.es_connect import es

def update_files_with_query(filename):
    return {
          "script": {
            "lang": "painless",
            "inline": "def updated = false; for (int i=0;i<ctx._source.files.size();i++) { if (ctx._source.files[i]['filename'] == params.file.filename){ctx._source.files[i].error_count += 1; updated=true;break}}if(!updated){ctx._source.files.add(params.file)}",
            "params": {
              "file" : {
                "filename" : filename,
                "error_count": 1
              }
            }
          }
        }

user = {
    "email" : "",
    "additions" : 0,
    "deletions" : 0,
    "jira_issues": [],
    "error_count": 0
}

def update_users_error_with_query(email):
    query_user = user
    query_user['email'] = email
    query_user['error_count'] = 1
    return {
          "script": {
            "lang": "painless",
            "inline": "def updated = false;"
                      "for (int i=0;i<ctx._source.users.size();i++) { if (ctx._source.users[i]['email'] == params.user.email){ctx._source.users[i].error_count += 1; updated=true;break}}if(!updated){ctx._source.users.add(params.user)}",
            "params": {
              "user" : query_user
            }
          }
        }

def update_users_git_info(email, additions, deletions):
    query_user = user
    query_user['email'] = email
    query_user['additions'] = additions
    query_user['deletions'] = deletions
    return {
          "script": {
            "lang": "painless",
            "inline": "def updated = false;"
                      "for (int i=0;i<ctx._source.users.size();i++) { if (ctx._source.users[i]['email'] == params.user.email){ctx._source.users[i].additions += params.user.additions; ctx._source.users[i].deletions += params.user.deletions; updated=true;break}}if(!updated){ctx._source.users.add(params.user)}",
            "params": {
              "user" : query_user
            }
          }
        }

def update_issues(issue, assignee_email):
    query_user = user
    query_user['email'] = assignee_email
    return {
      "script": {
        "lang": "painless",
        "inline": "def updated = false; int user_index = -1; for (int i=0;i<ctx._source.users.size();i++) { if (ctx._source.users[i]['email'] == params.user.email){ user_index = i; for(int j=0;j<ctx._source.users[i].jira_issues.size();j++) {def issue = ctx._source.users[i].jira_issues[j]; if (issue.summary == params.issue.summary) {issue.status = params.issue.status; issue.curr_start_time = params.issue.curr_start_time; issue.total_time += params.issue.total_time; ctx._source.users[i].jira_issues[j] = issue; updated=true; break } } break } } if(!updated){if (user_index == -1) {def user_copy = params.user; user_copy.jira_issues.add(params.issue); ctx._source.users.add(user_copy) } else {ctx._source.users[user_index].jira_issues.add(params.issue) } }",
        "params": {
          "issue" : issue,
          "user": query_user
        }
      }
    }

def get_issue_start_time(summary):
    query_body = {
        "query":{
            "nested":{
                "path" : "users.jira_issues",
                "query":{
                    "match":{
                        "users.jira_issues.summary": summary,
                    }
                },
                "inner_hits":{}
            }
        }
    }
    search_result = es.search(index='dev_meter', doc_type='project_registration', body=query_body)
    if search_result['hits']['total'] > 0:
        return search_result['hits']['hits'][0]['inner_hits']['users.jira_issues']['hits']['hits'][0]['_source']['curr_start_time']
    else:
        return None