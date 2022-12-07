#!/usr/bin/python3
""" API """
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()

if __name__ == '__main__':
    hosts = getenv('HBNB_API_HOST', default='0.0.0.0')
    ports = getenv('HBNB_API_PORT', default='5000')
    app.run(host=hosts, port=ports, threaded=True)
