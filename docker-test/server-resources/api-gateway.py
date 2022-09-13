"""
Simple echo server for testing.
"""

import json

from flask import Flask

app = Flask(__name__)


# @app.route('/', methods=['POST'])
# @app.route('/', methods=['DELETE'])
# @app.route('/', methods=['PUT'])
@app.route('/')
def index():
    return json.dumps({'name': 'mnist model',
                       'result': 1})

app.run(host='0.0.0.0', port=9999)