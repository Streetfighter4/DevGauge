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
            "inline": "def updated = false; for (int i=0;i<ctx._source.users.size();i++) { if (ctx._source.users[i]['email'] == params.user.email){ctx._source.users[i].error_count += 1; updated=true;break}}if(!updated){ctx._source.users.add(params.user)}",
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
            "inline": "def updated = false; for (int i=0;i<ctx._source.users.size();i++) { if (ctx._source.users[i]['email'] == params.user.email){ctx._source.users[i].additions += params.user.additions; ctx._source.users[i].deletions += params.user.deletions; updated=true;break}}if(!updated){ctx._source.users.add(params.user)}",
            "params": {
              "user" : query_user
            }
          }
        }

