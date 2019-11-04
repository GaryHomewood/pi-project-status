import os
import json
import time
import ledshim

from flask import Flask, request

def create_app():
    # pylint: disable=unused-variable
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # setup the instance folder for the db
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    def app_startup():
        # get the currently saved state from the db and set the LEDs
        with app.app_context():
            rows = db.get_db().execute('SELECT * FROM pixel_status').fetchall()
            for row in rows:
                print(row['pixel'], "-", row['status'])
                set_pixel(row['pixel'], row['status'])
    
    @app.route('/api/v1.0')
    def home():
        return '200 OK'

    @app.route('/api/v1.0/status', methods=['POST'])
    def set_status():
        # Note: json loaded like this because request.json is always empty for a post request
        # under nginx/uwsgi/Flask
        req = json.loads(request.data)

        # set the appropriate LED
        pixel = (int(req['metricId']) * int(req['teamMemberCount'])) + int(req['teamMemberId'])
        status = req['status']
        set_pixel(pixel, status)

        # save the LED state to the db
        conn = db.get_db()
        conn.execute(
          'REPLACE INTO pixel_status (pixel, status) VALUES (?, ?)',
          (pixel, status)
        )
        conn.commit()
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

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def set_pixel(pixel, status):
        if status == 'red':
            ledshim.set_pixel(pixel, 255, 0, 0, 0.5)
        elif status == 'amber':
            ledshim.set_pixel(pixel, 255, 140, 0, 0.5)
        elif status == 'green':
            ledshim.set_pixel(pixel, 0, 255, 0, 0.5)
        else:
            ledshim.set_pixel(pixel, 0, 0, 0)
        ledshim.show()
        return

    app_startup()
    return app