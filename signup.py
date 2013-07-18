#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy
import os
import datetime
import calendar
from flask import Flask
from flask import request

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ssdigfrrpvgjev:cTzHaJFPU5LekOPl7cUEnkqEP8@ec2-54-225-68-241.compute-1.amazonaws.com:5432/d1a8ndh1lhq25k"
app.config['DEBUG'] = True;
db = SQLAlchemy(app)

""" Event Schema """

class Event(db.Model):

	#Id's FTW - unique and fresh, don't mess with it
    id = db.Column(db.Integer, primary_key=True)

    #Name of event
    title = db.Column(db.Text)

    #Description of event
    description = db.Column(db.Text)

    #Starting Date and Time of Event
    startDateTime = db.Column(db.DateTime)

    #Ending Date and Time of Event
    endDateTime = db.Column(db.DateTime)

    #Attendees - json string
    attendees = db.Column(db.Text)

    #Max Attendees
    maxAttendees = db.Column(db.Integer)

    #Metadata - for kicks... and application specific crap later on
    meta = db.Column(db.Text)

    #Initialize ALL THE COLUMNS!
    def __init__(self, title, description, startDateTime, endDateTime, attendees, maxAttendees, metadata=None):
        self.title = title
        self.description = description
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime
        self.attendees = attendees
        self.maxAttendees = maxAttendees
        self.metadata = metadata

    def __repr__(self):
        return '<Event: %r>' % self.title



""" Main Pages """

@app.route('/search/<theYear>/<theMonth>')
def getMonthEventData(theYear,theMonth):
	year = int(theYear);
	month = int(theMonth);

	num_days = calendar.monthrange(year, month)[1]
	start_date = datetime.date(year, month, 1)
	end_date = datetime.date(year, month, num_days)

	results = db.session.query(Event).filter(and_(Event.startDateTime >= start_date, Event.startDateTime <= end_date)).all()
	return_Str = ""
	for event in results:
		return_Str += event.startDateTime.strftime('%m/%d/%Y')
		return_Str += " - "
		return_Str += event.attendees
		return_Str += "</br>"
	return return_Str

@app.route('/search/<theYear>/<theMonth>/<theDay>')
def getDayEventData(theYear,theMonth,theDay):
	year = int(theYear);
	month = int(theMonth);
	day = int(theDay);
	
	start_date = datetime.datetime(year, month, day, 0,0,0,0,None)
	end_date = datetime.datetime(year, month, day, 23, 59, 59,999999,None)

	results = db.session.query(Event).filter(and_(Event.startDateTime >= start_date, Event.startDateTime <= end_date)).all()
	return_Str = ""
	for event in results:
		return_Str += event.startDateTime.strftime('%m/%d/%Y')
		return_Str += " - "
		return_Str += event.attendees
		return_Str += "</br>"
	return return_Str

@app.route('/event/<id>')
def getEventData(id):
	event = db.session.query(Event).filter(Event.id==id).first()
	return_Str = ""
	return_Str += event.startDateTime.strftime('%m/%d/%Y')
	return_Str += " - "
	return_Str += event.attendees
	return_Str += "</br>"
	return return_Str


@app.route('/events/add')
def addEvent():
	event = Event('ride', datetime.datetime.today(), "me");
	db.session.add(event);
	db.session.commit();
	return "added";

@app.route('/')
def default():
	return "Hi";
