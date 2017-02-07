import requests
from elasticsearch import Elasticsearch
from src.dynamic.config.urls import *

es = Elasticsearch([{'host': HOST_URL, 'port': ELASTICSEARCH_PORT}])

def test_connection():
    r = requests.get('http://' + HOST_URL + ':' + str(ELASTICSEARCH_PORT))
    return r.status_code == 200