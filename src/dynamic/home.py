import requests

from src.dynamic.web_hooks import jira_webhook, git_webhook, sentry_webhook
from flask import Flask

app = Flask(__name__)
app.register_blueprint(jira_webhook.hook)
app.register_blueprint(git_webhook.hook)
app.register_blueprint(sentry_webhook.hook)

if __name__ == "__main__":
    app.run(port=80, host='192.168.0.100')



