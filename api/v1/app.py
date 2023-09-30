#!/usr/bin/python3
"""Proceeds to import Flask and run host plus port"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import environ
from werkzeug.exceptions import NotFound
app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(NotFound)
def handle_404(error):
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == '__main__':
    hst = environ.get("HBNB_API_HOST") if environ.get(
            "HBNB_API_HOST") else "0.0.0.0"
    prt = environ.get("HBNB_API_PORT") if environ.get(
            "HBNB_API_PORT") else 5000
    app.run(host=hst, port=prt, threaded=True)