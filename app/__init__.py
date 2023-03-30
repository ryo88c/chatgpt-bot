import os
import json
from flask import Flask, request
from pprint import pprint
from redis import Redis

app = Flask(__name__)

client = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])

@app.route('/', methods=['POST'])
def index():
    body = json.loads(request.data.decode('utf-8'))
    if 'challenge' in body:
        return body['challenge']
    if 'event' in body and 'text' in body['event']:
        client.rpush('messages', json.dumps(body))
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
