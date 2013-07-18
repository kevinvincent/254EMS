#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy
import os
import datetime
import calendar
from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ssdigfrrpvgjev:cTzHaJFPU5LekOPl7cUEnkqEP8@ec2-54-225-68-241.compute-1.amazonaws.com:5432/d1a8ndh1lhq25k"
db = SQLAlchemy(app)

""" Event Schema """

class Event(db.Model):
	#id's FTW - use em
    id = db.Column(db.Integer, primary_key=True)

    #type of event - food / ride
    name = db.Column(db.String(80)) 

    #date of event - python datetime object
    date = Column(db.DateTime)

    #users signed up - json string
    signups = Column(db.Text)

    def __init__(self, name, date, signups):
        self.name = name
        self.date = date
        self.signups = signups

    def __repr__(self):
        return '<Event %r>' % self.name



""" Main Pages """

@app.route('/events/<month>')
def getMonthEvents(month):
	year = 2012
	month = 6

	num_days = calendar.monthrange(year, month)[1]
	start_date = datetime.date(year, month, 1)
	end_date = datetime.date(year, month, num_days)

	results = session.query(Event).filter(and_(Event.date >= start_date, Event.date <= end_date)).all()
    return "getting events for" + month

@app.route('/events/add', methods=['GET', 'POST'])
def addEvent()
	name = request.args.get('name', '')
	
