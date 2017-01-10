import traceback

from flask import Flask, request, make_response, jsonify, render_template
app = Flask(__name__)

#from elasticsearch import Elasticsearch
#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

import requests
import json

@app.route('/webhook', methods=['GET','POST'])
def tracking():
    print('hey')
    print (request.get_json())
    print('hey2')
    jsonDict = request.get_json()
    issueUrl = jsonDict['issue']['self']
    print (issueUrl)

    r = requests.get(issueUrl, auth=('yasen.alexiev@abv.bg', 'Streetfighter4'))
    print(r.json()['fields']['summary'])

    #     data = request.data
    #     try:
    #         jdata = json.load(data)
    #
    #         if jdata['webhookEvent'] == 'jira::issue_created':
    #
    #
    #     except:
    #         print
    #         traceback.format_exc()
    #         msg = 'Incorrect data! Can not parse to json format'
    #         print
    #         msg
    #         return make_response(msg, 500)



   # r = requests.get('http://localhost:9200')
    i = 1
    # while i < 10:
    #     es.index(index='devgauge', doc_type='jiraData', id=i, body=json.loads(r.text))
    #     i = i + 1
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=80, host='192.168.0.100')