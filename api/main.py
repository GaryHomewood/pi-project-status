from flask import Flask, request
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/v1.0/status', methods=['POST'])
def set_status():
    print(request.json)
    pixel = (request.json['userId'] * request.json['metricCount']) + request.json['metricId']
    print('pixel:', pixel)
    return {'status': 'ok'}
