import flask
import os
from flask import send_from_directory
import push

helloWorld = "HELLO WORLD"

app = flask.Flask(__name__)

@app.route('/')
@app.route('/<int:startDay>/<int:endDay>/<string:key>')
def home(startDay, endDay, key):
    push.sendNotifs(startDay, endDay, key)
    return f"{startDay} {endDay} {key}"


if(__name__ == "__main__"):
    app.secret_key = 'Secret'
    app.debug = True
    app.run()

