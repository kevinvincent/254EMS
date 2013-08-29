#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy
import os
import datetime
import calendar
import json
import hashlib

from flask import Flask
from flask import request

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ssdigfrrpvgjev:cTzHaJFPU5LekOPl7cUEnkqEP8@ec2-54-225-68-241.compute-1.amazonaws.com:5432/d1a8ndh1lhq25k"
app.config['DEBUG'] = True;
db = SQLAlchemy(app)


#Define all the Schemas!
class event_type(db.Model):

    #unique event type id
    event_id = db.Column(db.Integer, primary_key=True)

    #name of event type
    type = db.Column(db.Text)

class events(db.Model):

    #Id's FTW - unique and fresh, don't mess with it
    id = db.Column(db.Integer, primary_key=True)

    #--> event_type.eid
    event_type_id = db.Column(db.Integer)

    #Starting Date and Time of Event
    start_time = db.Column(db.DateTime)

    #Ending Date and Time of Event
    end_time = db.Column(db.DateTime)

    #Is it open?
    available = db.Column(db.Boolean)

    #Amount slots open
    num_slotes = db.Column(db.Integer)

    #Has it been cancelled?
    cancelled = db.Column(db.Boolean)

    #specific info?
    notes = db.Column(db.Text)

class registrations(db.Model):

    #Id's FTW - unique and fresh, don't mess with it
    id = db.Column(db.Integer, primary_key=True)

    #users.id "what user?"
    user_id = db.Column(db.Integer)

    #events.id "wat event"
    event_id = db.Column(db.Integer)

    #timestamp of registration
    timestamp = db.Column(db.DateTime)

    #would u like a reminder oh forgetful one?
    remind = db.Column(db.Boolean)

    #why u cancel?
    cancel_time = db.Column(db.DateTime, default=None)

    #why u no show up?
    no_show = db.Column(db.Boolean, default=False)

    #anything else?
    notes = db.Column(db.Text)

class users(db.Model):

    #More Id's FTW - unique and fresh, don't mess with it
    id = db.Column(db.Integer, primary_key=True)

    #email address
    email = db.Column(db.Text)

    #user full name
    name = db.Column(db.Text)

    # 'normal', 'eligible', 'leader', 'mentor'
    status = db.Column(db.Text)


