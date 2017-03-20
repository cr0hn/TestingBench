import os.path

from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

DB_LOCATION = os.path.abspath("my_db.db")

app = Flask("myapp")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_LOCATION)

db = SQLAlchemy(app)


class MyEvents(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    event_date = db.Column(db.DateTime, default=datetime.now)
    event_text = db.Column(db.String)

    def __init__(self, event_text):
        self.event_text = event_text


@app.route("/")
def home():
    return jsonify(message="Event tracking system")


@app.route("/event/add")
def add_event():
    event_message = request.args.get("message", None)

    if not event_message:
        return jsonify(error="'message' parameter is needed"), 400

    o = MyEvents(event_message)

    db.session.add(o)
    db.session.commit()

    return jsonify(message="Event added")


@app.route("/event/list")
def list_event():

    all_events = MyEvents.query.all()

    response = []

    for event in all_events:
        response.append(
            {
                "addedDate": event.event_date.strftime("%d-%m-%Y - %H:%M"),
                "eventMessage": event.event_text
            }
        )

    return jsonify(response)

#
# Create database
#
try:
    db.create_all()
except Exception as e:
    print(e)

#
# Launch server
#
app.run("127.0.0.1", port=8000)
