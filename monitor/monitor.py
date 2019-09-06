import json
import random
import redis
from datetime import timedelta, datetime
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
r = redis.Redis()
random.seed(42)

@app.route('/add_machine', methods=['POST'])
def add():
    req_data = request.get_json()
    data = json.dumps(req_data)
    if r.setex("machine:{}".format(random.getrandbits(32)),
                timedelta(minutes=1),
                value=data):
                return {
                    'status': True,
                    'message': 'add machien info successfully'
                }
    else:
        return {
            'status': False,
            'message': 'Failed to add machine info '
        }



@app.route('/get_machines', methods=['GET'])
def get():
    results = []
    try:
        for key in r.keys():
            results.append(json.loads(r.get(key).decode('utf-8')))
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        for result in results:
            result['timestamp'] = str(datetime.fromtimestamp(result['timestamp']))
        return jsonify(results)
    except:
        return 'Internal server error'


@app.route('/ping')
def ping():
    return 'pong'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
