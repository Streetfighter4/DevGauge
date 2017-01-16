import traceback

from flask import Flask, request, make_response, jsonify, render_template
app = Flask(__name__)

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], timeout=30)
es.cluster.health(wait_for_status='yellow', request_timeout=5)

import requests
import json

@app.route('/webhook', methods=['GET','POST'])
def tracking():
    print('hey')
    print (request.get_json())
    print('hey2')
    jsonDict = request.get_json()
    print(jsonDict)
    issueUrl = jsonDict['issue']['self']
    print(issueUrl)


    r = requests.get('http://localhost:9200')
    i = 1
    if r.status_code == 200:
        r = requests.get(issueUrl , auth=('yasen.alexiev@abv.bg', 'Streetfighter4'))
        #print(r.json()['fields']['summary'])


        es.index(index='dev_gauge', doc_type='jira_issues', id=r.json()['id'], body=r.json())
        res = es.get(index='dev_gauge', doc_type='jira_issues', id=r.json()['id'])
        print(res)
        print(res['_source'])
        res = es.search(index='dev_gauge', body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            print("%(summary)s" % hit["_source"]['fields'])

    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=80, host='192.168.0.100')