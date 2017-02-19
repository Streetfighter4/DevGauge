from flask import Blueprint
from flask import app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.user import login_required

from dynamic.elasticsearch_connection import es_connect
setiings_blue_print = Blueprint('settings', __name__)

@setiings_blue_print.route('/setup', methods=['GET', 'POST'])
@login_required  # Use of @login_required decorator
def setup_project():
    if request.method == 'GET':
        return render_template('setup_project.html')
    else:
        print('hey')
        if es_connect.test_connection():
            print('hey1.5')
            print(current_user.email)
            print(request.form.get('git_repo'))
            project_info = {
                "email" : current_user.email,
                "git_repo" : request.form['git_repo'],
                "sentry_project" : request.form['sentry_project'],
                "jira_project": request.form['jira_project']
            }
            print(project_info)
            es_connect.es.index(index='dev_meter', doc_type='project_registration', id=current_user.email, body=project_info)
        print('hey2')
        return redirect(url_for('home_page'))