#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy
#qry = DBSession.query(User).filter(User.birthday.between('1985-01-17', '1988-01-17'))


# *************** #
# General Imports
# *************** #
import os
import datetime
import calendar
import json
import time
import hashlib
import requests
from flask import *


# ********** #
# DB Imports
# ********** #
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import *


# *********** #
# APP Configs
# *********** #
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ssdigfrrpvgjev:cTzHaJFPU5LekOPl7cUEnkqEP8@ec2-54-225-68-241.compute-1.amazonaws.com:5432/d1a8ndh1lhq25k"
app.config['DEBUG'] = True;
db = SQLAlchemy(app)
app.secret_key = '\xe8\xec~G:\xa9iZ{D|^\x1bvc}U\xac\xbc\x1e\xf4\xed\x8c'


# *********** #
# URL Configs
# *********** #
BASE_URL = "http://team254.com:5000"
AUTH_URL = "http://team254.com/auth/"


# ******************************** #
# Application Stuff in other files
# ******************************** #
from models import *


# ******* #
# Logging
# ******* #
import logging
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)


# ********* #
# KVSession
# ********* #
from simplekv.memory import DictStore
from flask.ext.kvsession import KVSessionExtension
    #from simplekv.db.sql import SQLAlchemyStore
    #store = SQLAlchemyStore(db.engine, db.metadata, 'sessions')
store = DictStore()
kvsession = KVSessionExtension(store, app)


# ****************** #
# DB Admin Interface
# ****************** #
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqlamodel import ModelView

class CustomView(ModelView):
    column_display_pk = True
    column_auto_select_related = True

admin = Admin(app, name = "Cheesy-Signups DB Admin")
admin.add_view(CustomView(Event, db.session))
admin.add_view(CustomView(Event_Category, db.session))
admin.add_view(CustomView(Event_Meta, db.session))
admin.add_view(CustomView(Registration, db.session))




# ********************** #
# Main App
# ********************** #

@app.before_request
def gateKeeper():

    if 'user_id' in session:
        return

    else:
        
        wpCookieExists = False
        wpCookieData = "";
        for cookie in request.cookies:
            if 'wordpress_logged_in' in cookie:
                wpCookieExists = True
                wpCookieData = request.cookies[cookie]
                break

        if not wpCookieExists:
            #Handle jsonp requests
            if(request.args.get('callback') != None):
                return 'window.location = '+'"http://www.team254.com/wp-login.php?redirect_to=http://www.team254.com/auth/?sub=www&path=/"'
            else:
                return redirect("http://www.team254.com/wp-login.php?redirect_to=http://www.team254.com/auth/?sub=www&path=/") # <-- cookie monster

        else:

            r = requests.get(AUTH_URL+"?cookie="+wpCookieData)
            
            if r.status_code == 200:

                user_data = r.json()
                user_data['signature'] == ""

                session['user_id'] = user_data['id'];
                session['user_data'] = json.dumps(user_data)

            else:
                pass


"""TESTER VIEWS"""

@app.route('/sess')
def sess():
    return session['user_data']

@app.route('/createEvents')
def createEvents():
    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n)


    year = 2013
    month = 7

    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month+1, 1)

    returnString = ""
    for single_date in daterange(start_date, end_date):
        #returnString += time.strftime("%Y-%m-%d", single_date.timetuple())
        returnString += str(single_date)
        returnString += "<br/>"

    return returnString

@app.route('/reset')
def reset():
    db.drop_all()
    db.create_all()
    return "DONE"



""" Application Views """

#Full Calendar Event Loader
@app.route('/loadView')
def loadView():
    print "loadView";

    start_date = datetime.datetime.fromtimestamp(int(request.args.get('start')))
    end_date = datetime.datetime.fromtimestamp(int(request.args.get('end')))

    startDbTime = int(round(time.time() * 1000))
    results = db.session.query(Event).filter(or_(and_(Event.start_time >= start_date, Event.start_time <= end_date),and_(Event.end_time >= start_date, Event.end_time <= end_date))).all()
    print "Calendar DB Query: " + str(int(round(time.time() * 1000))-startDbTime);

    returnList = []

    for theEvent in results:
        data = {}

        #Full Calendar Required Information
        data['title'] = theEvent.title
        data['allDay'] = True
        data['start'] = str(theEvent.start_time)
        data['end'] = str(theEvent.end_time)

        #Custom MetaData
        category = db.session.query(Event_Category).filter(Event_Category.id==theEvent.et_id).first()

        #Event Category
        data['category'] = str(category.name)

        #Unique Id
        data['id'] = theEvent.id

        #Registrations List
        signupsResults = theEvent.registrations.filter(Registration.has_cancelled==False).all()
        signups = []
        for theRegistration in signupsResults:
            signups.append(theRegistration.username)
        data['registrations'] = signups

        #Is the user already registered?
	    if(theEvent.registrations.filter(and_(Registration.u_id==session['user_id'],Registration.has_cancelled==False)).count()==0):
	    	data['isRegistered'] = False
	    else:
	    	data['isRegistered'] = True

        #Number of Registrations
        data['numberOfRegistrations'] = len(signups)

        #Max Number of registrations
        data['maxRegistrations'] = theEvent.metas.filter(Event_Meta.key=="MAX_REGISTRATION_COUNT").first().value;

        returnList.append(data)

    app.logger.info(json.dumps(returnList));

    #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(returnList) + ")"
    else:
        return json.dumps(returnList)

@app.route('/getEvent/<eventId>')
def getEvent(eventId):
    print "getEvent";

    startDbTime = int(round(time.time() * 1000))
    theEvent = db.session.query(Event).filter(Event.id==int(eventId)).first()
    print "Event DB Query: " + str(int(round(time.time() * 1000))-startDbTime);

    data = {}

    #Full Calendar Required Information
    data['title'] = theEvent.title
    data['allDay'] = True
    data['start'] = str(theEvent.start_time)
    data['end'] = str(theEvent.end_time)

    #Custom MetaData
    category = db.session.query(Event_Category).filter(Event_Category.id==theEvent.et_id).first()

    #Event Category
    data['category'] = str(category.name)

    #Unique Id
    data['id'] = theEvent.id

    #Registrations List
    signupsResults = theEvent.registrations.filter(Registration.has_cancelled==False).all()
    signups = []
    for theRegistration in signupsResults:
        signups.append(theRegistration.username)
    data['registrations'] = signups

    #Is the user already registered?
    if(theEvent.registrations.filter(and_(Registration.u_id==session['user_id'],Registration.has_cancelled==False)).count()==0):
    	data['isRegistered'] = False
    else:
    	data['isRegistered'] = True

    #Number of Registrations
    data['numberOfRegistrations'] = len(signups)

    #Max Number of registrations
    data['maxRegistrations'] = theEvent.metas.filter(Event_Meta.key=="MAX_REGISTRATION_COUNT").first().value;

    app.logger.info(json.dumps(data));

    #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(data) + ")"
    else:
        return json.dumps(data)

#Dashboard feed wide
@app.route('/mySignupsFeed')
def mySignupsFeed():
    print "mySignupsFeed";

    returnList = [];

    startDbTime = int(round(time.time() * 1000))
    mySignups = db.session.query(Event).join(Registration).filter(and_(Registration.u_id==session['user_id'],Registration.has_cancelled==False)).all();
    print "Feed DB Query: " + str(int(round(time.time() * 1000))-startDbTime)

    for signup in mySignups:
        data = {}

        data['title'] = signup.title
        data['start'] = str(signup.start_time)
        data['id'] = signup.id

        returnList.append(data)

        #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(returnList) + ")"
    else:
        return json.dumps(returnList)


#Cancel a registration
@app.route('/cancel/<eventId>')
def cancel(eventId):

    cancelEventId = int(eventId)
    mySignupToCancel = db.session.query(Registration).filter(Registration.u_id==session['user_id'] and Registration.e_id==cancelEventId).first();

    mySignupToCancel.has_cancelled = True;

    db.session.commit();
    app.logger.info("Canceled Event " + str(cancelEventId) + ": Registration - " + str(mySignupToCancel.id));

    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(["Successfully Cancelled"]) + ")"
    else:
        return json.dumps([])


#Add a registration
@app.route('/register/<eventId>',methods=['GET','POST'])
def register(eventId):

    theEvent = db.session.query(Event).filter(Event.id == int(eventId)).first()
    userInfo = json.loads(session['user_data']);

    #Registration(u_id=userInfo['id'], username=userInfo['username'], e_id=theEvent, timestamp=datetime.datetime.now(), remind=False, cancel_time=None, has_cancelled=False, no_show=False, notes=request.args.get("notes"))
    newRegistration = Registration(u_id=userInfo['id'], username=userInfo['username'], e_id=theEvent.id, timestamp=datetime.datetime.now(), remind=False, cancel_time=None, has_cancelled=False, no_show=False, notes=request.args.get("notes",""))

    db.session.add(newRegistration)
    db.session.commit()

    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(["Successfully Registered"]) + ")"
    else:
        return json.dumps([])


@app.route('/')
def dashboard():
    return render_template("main.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")
