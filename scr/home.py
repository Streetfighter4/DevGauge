from flask import Flask, request
app = Flask(__name__)

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

import requests
import json

@app.route("/")
def hello():
    print('hey')
    r = requests.get('http://localhost:9200')
    i = 1
    while i < 10:
        r = requests.get('http://swapi.co/api/people/' + str(i))
        es.index(index='sw', doc_type='people', id=i, body=json.loads(r.text))
        i = i + 1

    return 'hey'

if __name__ == "__main__":
    app.run()