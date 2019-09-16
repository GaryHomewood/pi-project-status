from flask import Flask, request
app = Flask(__name__)

import json
import ledshim
import time

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/v1.0')
def home():
    return '200 OK'

@app.route('/api/v1.0/status', methods=['POST'])
def set_status():
    # Note: json loaded like this because request.json is always empty for a post request
    # under nginx/uwsgi/Flask
    req = json.loads(request.data)

    pixel = (int(req['metricId']) * int(req['teamMemberCount'])) + int(req['teamMemberId'])
    status = req['status']

    if status == 'red':
        ledshim.set_pixel(pixel, 255, 0, 0, 0.5)
    elif status == 'amber':
        ledshim.set_pixel(pixel, 255, 140, 0, 0.5)
    elif status == 'green':
        ledshim.set_pixel(pixel, 0, 255, 0, 0.5)
    else:
        ledshim.set_pixel(pixel, 0, 0, 0)

    ledshim.show()
    return '200 OK'

@app.route('/api/v1.0/reset', methods=['POST'])
def reset():
    pixelCount = (request.json['pixelCount'])
    delay = 0.1
    for pixel in range(pixelCount - 1, -1, -1):
        ledshim.set_pixel(pixel, 0, 0, 0)
        ledshim.show()
        time.sleep(delay)
    return '200 OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0')