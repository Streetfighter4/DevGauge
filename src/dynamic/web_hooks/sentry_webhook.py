import requests
from src.dynamic.elasticsearch_connection import es_connect
from flask import Blueprint
from flask import request
from flask import Response

from src.dynamic.web_hooks import git_webhook

hook = Blueprint('sentryhook', __name__)

@hook.route('/sentry_webhook', methods=['GET','POST'])#TODO: check if can delete get
def sentry_webhook():
    print('aasdasdasda')
    #git_webhook.git_blame()
    return Response(status=200)
