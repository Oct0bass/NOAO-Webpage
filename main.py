# main.py - Server backend (python)
import json

import flask
from flask import request

app = flask.Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return app.send_static_file("index.html")
    elif request.method == "POST":
        with open("passwd.txt", "rt") as f:
            if request.form.get("password") == f.read():
                return flask.redirect("/chart")
            else:
                return flask.redirect("/?retry")
    else:
        return "Invalid Request: %s" % request


@app.route("/chart", methods=["GET", "POST"])
def chart():
    # TODO: clean some of this up
    if request.method == "GET":
        with open("chart.json", "rt") as f:
            chart_data = f.read()
        return flask.render_template("chart.html", **json.loads(chart_data))
    elif request.method == "POST":
        req_data = request.get_json()
        json_data = req_data.loads()
        with open("chart.json", "r+t") as f:
            fdata = json.loads(f.read())
            fdata[json_data["row"]["col"]] = json_data["content"]
    else:
        return "Invalid Request: %s" % request


app.run(host="localhost", port=8000)
