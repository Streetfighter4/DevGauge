from src.dynamic.web_hooks import jira_webhook, git_webhook

from flask import Flask, request, make_response, jsonify, render_template
app = Flask(__name__)
app.register_blueprint(jira_webhook.hook)
app.register_blueprint(git_webhook.hook)

#from raven.contrib.flask import Sentry
#sentry = Sentry(app, dsn='http://7fe4ca23adb74d4d92f5d17167e66919:8fce1ff465b445ea94c1210d1c5e91d7@sentry.devmeter/2')

if __name__ == "__main__":
    app.run(port=80, host='192.168.0.100')