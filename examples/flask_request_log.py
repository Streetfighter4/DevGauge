import pprint

from flask import Flask, request
app = Flask(__name__)

@app.before_request
def log_request():
    pprint.pprint({
        'url': request.url,
        'method': request.method,
        'headers': request.headers,
        'data': request.data
    })


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def catch_all(path):
    return 'You want path: %s' % path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
