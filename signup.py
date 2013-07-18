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
	#id's FTW - use em
    id = db.Column(db.Integer, primary_key=True)

    #type of event - food / ride
    name = db.Column(db.Text) 

    #Date time objects
    date = db.Column(db.Date)

    #users signed up - json string
    signups = db.Column(db.Text)

    def __init__(self, name, date, signups):
        self.name = name
        self.date = date
        self.signups = signups

    def __repr__(self):
        return '<Event %r>' % self.name



""" Main Pages """

@app.route('/events/<theYear>/<theMonth>')
def getMonthEventData(theYear,theMonth):
	year = int(theYear);
	month = int(theMonth);

	num_days = calendar.monthrange(year, month)[1]
	start_date = datetime.date(year, month, 1)
	end_date = datetime.date(year, month, num_days)

	results = db.session.query(Event).filter(and_(Event.date >= start_date, Event.date <= end_date)).all()
	return_Str = ""
	for event in results:
		return_Str += event.date.strftime('%m/%d/%Y')
		return_Str += " - "
		return_Str += event.signups
		return_Str += "</br>"
	return return_Str

@app.route('/events/<theYear>/<theMonth>/<theDay>')
def getDayEventData(theYear,theMonth,theDay):
	year = int(theYear);
	month = int(theMonth);
	day = int(theDay);
	
	searchDate = datetime.date(year, month, day)

	results = db.session.query(Event).filter(Event.date.date()==searchDate).all()
	#return_Str = ""
	#for event in results:
		#return_Str += event.date.strftime('%m/%d/%Y')
		#return_Str += " - "
		#return_Str += event.signups
		#return_Str += "</br>"
	return searchDate.strftime('%m/%d/%Y')

@app.route('/events/add')
def addEvent():
	event = Event('ride', datetime.datetime.today(), "me");
	db.session.add(event);
	db.session.commit();
	return "added";

@app.route('/')
def default():
	return "Hi";
