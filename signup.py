#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy
#qry = DBSession.query(User).filter(User.birthday.between('1985-01-17', '1988-01-17'))

#TODO
# Take old events out of signups feed
# Server side validatation of reservations < maxRegistration
# Admin lockout

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
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://sdrlkkapvrjfbj:DhYDslB1Q-E6bTldFOxILHhTZA@ec2-54-197-246-197.compute-1.amazonaws.com:5432/d1j67bkedrnib1"
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


# ******** #
# Compress
# ******** #
from flask.ext.compress import Compress
Compress(app)

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



# Auth Api
# ********************** #
@app.before_request
def gateKeeper():

    app.logger.info(str(datetime.datetime.now()))
    if 'user_id' in session:
        # if(request.path == '/admin'):
        #     return redirect("http://tweetharder.com/t/634/lol/")
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
                return 'window.location = '+'"http://www.team254.com/wp-login.php?redirect_to=http://signup.team254.com/"'
            else:
                return redirect("http://www.team254.com/wp-login.php?redirect_to=http://www.team254.com/auth/?sub=www&path=") # <-- cookie monster

        else:

            r = requests.get(AUTH_URL+"?cookie="+wpCookieData)
            
            if r.status_code == 200:

                user_data = r.json()
                user_data['signature'] == ""

                session['user_id'] = user_data['id'];
                session['user_data'] = json.dumps(user_data)

            else:
                pass



# Test Endpoints
# ********************** #

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

# @app.route('/reset')
# def reset():
#     db.drop_all()
#     db.create_all()
#     return "DONE"



# Application Endpoints
# ********************** #

#Fullcalendar endpoint
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

        #Description
        data['description'] = theEvent.description;

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

        if(theEvent.start_time < datetime.datetime.now()):
            data['color'] = "#95a5a6"
        elif(float(data['maxRegistrations']) - float(data['numberOfRegistrations']) == 0 ):
            data['color'] = "#e74c3c"
        elif(float(data['numberOfRegistrations']) / float(data['maxRegistrations']) >= .5):
            data['color'] = "#f39c12"
        else:
            data['color'] = "#18bc9c"

        returnList.append(data)

    app.logger.info(json.dumps(returnList));

    #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(returnList) + ")"
    else:
        return json.dumps(returnList)

#Endpoint for search
@app.route('/search/<query>')
def search(query):
    print "Search";

    startDbTime = int(round(time.time() * 1000))
    results = db.session.query(Event).filter(Event.title.ilike("%"+query+"%")).all()
    print "Search DB Query: " + str(int(round(time.time() * 1000))-startDbTime);

    returnList = [];

    for result in results:
        data = {}

        #Full Calendar Required Information
        data['title'] = result.title
        data['allDay'] = True
        data['start'] = str(result.start_time)
        data['end'] = str(result.end_time)

        #Custom MetaData
        category = db.session.query(Event_Category).filter(Event_Category.id==result.et_id).first()

        #Event Category
        data['category'] = str(category.name)

        #Description
        data['description'] = result.description;

        #Unique Id
        data['id'] = result.id

        #TypeaheadJS
        data['value'] = result.title
        data['start_time_pretty'] = str(result.start_time.hour)+":"+str(result.start_time.minute)
        data['start_date_pretty'] = str(result.start_time.month)+"/"+str(result.start_time.day)+"/"+str(result.start_time.year)

        tokens = [data['value'],data['start_date_pretty']]
        data['tokens'] = tokens

        returnList.append(data);

    #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(returnList) + ")"
    else:
        return json.dumps(returnList)


#Returns information for a event
@app.route('/event/<eventId>')
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
    data['start_pretty'] = theEvent.start_time.strftime('%I:%M %p')
    data['end_pretty'] = theEvent.end_time.strftime('%I:%M %p')

    #Custom MetaData
    category = db.session.query(Event_Category).filter(Event_Category.id==theEvent.et_id).first()

    #Event Category
    data['category'] = str(category.name)

    #Description
    data['description'] = theEvent.description;

    #Unique Id
    data['id'] = theEvent.id

    #Registrations List
    signupsResults = theEvent.registrations.filter(Registration.has_cancelled==False).all()
    signups = []
    for theRegistration in signupsResults:
        regdata = {}
        regdata['username'] = theRegistration.username
        regdata['notes'] = theRegistration.notes
        signups.append(regdata)

    data['registrations'] = signups

    #Is the user already registered?
    if(theEvent.registrations.filter(and_(Registration.u_id==session['user_id'],Registration.has_cancelled==False)).count()==0):
    	data['isRegistered'] = False
    else:
    	data['isRegistered'] = True

    #Number of Registrations
    data['numberOfRegistrations'] = len(signups)

    #Max Number of registrations
    maxRegistrations = theEvent.metas.filter(Event_Meta.key=="MAX_REGISTRATION_COUNT").first();
    if(maxRegistrations == None): data['maxRegistrations'] = 15
    else: data['maxRegistrations'] = maxRegistrations.value

    data['open'] = True
    if(theEvent.start_time < datetime.datetime.now()):
        data['open'] = False
    elif(int(data['maxRegistrations']) - int(data['numberOfRegistrations']) < 1):
        app.logger.info("Max Reg")
        data['open'] = False

    app.logger.info(json.dumps(data));

    prevRegistration = theEvent.registrations.filter(and_(Registration.u_id==session['user_id'],Registration.has_cancelled==False)).first();
    try:
        data['needBus'] = prevRegistration.needBus;
    except:
        data['needBus'] = False

    #search
    data['name'] = theEvent.title

    #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(data) + ")"
    else:
        return json.dumps(data)


#Get the list of registered events
@app.route('/mySignupsFeed')
def mySignupsFeed():
    print "mySignupsFeed";

    theFeed = {};

    returnList = [];

    startDbTime = int(round(time.time() * 1000))
    mySignups = db.session.query(Event).join(Registration).filter(and_(Registration.u_id==session['user_id'],Registration.has_cancelled==False)).all();
    print "Feed DB Query: " + str(int(round(time.time() * 1000))-startDbTime)

    for signup in mySignups:

        if(signup.start_time < datetime.datetime.now()):
            continue

        data = {}

        data['title'] = signup.title
        data['start'] = signup.start_time.strftime('%b, %d %Y - %I:%M %p')
        data['id'] = signup.id

        returnList.append(data)

    theFeed['feed'] = returnList;
    #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(theFeed) + ")"
    else:
        return json.dumps(theFeed)


#Cancel a registration
@app.route('/cancel/<eventId>')
def cancel(eventId):

    cancelEventId = int(eventId)
    mySignupToCancel = db.session.query(Registration).filter(and_(Registration.u_id==session['user_id'], Registration.e_id==cancelEventId, Registration.has_cancelled==False)).first();

    mySignupToCancel.has_cancelled = True;

    db.session.commit();
    app.logger.info("Canceled Event " + str(cancelEventId) + ": Registration - " + str(mySignupToCancel.id));

    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(["Successfully Cancelled"]) + ")"
    else:
        return json.dumps([])


#Add a registration
# @app.route('/register/<eventId>',methods=['GET'])
# def register(eventId):

#     theEvent = db.session.query(Event).filter(Event.id == int(eventId)).first()
#     userInfo = json.loads(session['user_data']);

#     #Registration(u_id=userInfo['id'], username=userInfo['username'], e_id=theEvent, timestamp=datetime.datetime.now(), remind=False, cancel_time=None, has_cancelled=False, no_show=False, notes=request.args.get("notes"))
#     newRegistration = Registration(u_id=userInfo['id'], username=userInfo['username'], e_id=theEvent.id, timestamp=datetime.datetime.now(), remind=False, cancel_time=None, has_cancelled=False, no_show=False, notes=request.args.get("notes",""))

#     db.session.add(newRegistration)
#     db.session.commit()

#     if(request.args.get('callback') != None):
#         return request.args.get('callback') + "(" + json.dumps(['success']) + ")"
#     else:
#         return json.dumps(['success'])
    
#Add a FRC registration
@app.route('/registerFRC/<eventId>',methods=['GET'])
def registerFRC(eventId):

    theEvent = db.session.query(Event).filter(Event.id == int(eventId)).first()
    userInfo = json.loads(session['user_data']);

    bus = bool(int(request.args.get("needBus","0")))

    #Get Start and End of Week
    day = theEvent.start_time
    day_of_week = day.weekday()
    to_beginning_of_week = datetime.timedelta(days=day_of_week+1)
    beginning_of_week = day - to_beginning_of_week
    beginning_of_week = beginning_of_week.replace(hour=0, minute=0, second=0)
    to_end_of_week = datetime.timedelta(days=6 - day_of_week-1)
    end_of_week = day + to_end_of_week
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59)
    #app.logger.info("Start: "+str(beginning_of_week)+" End: "+str(end_of_week));

    #Get number of events they have registered for on the week of the event they want to register for
    a = and_(Registration.u_id==session['user_id'],Registration.has_cancelled==False)
    b = or_(Event.start_time >= datetime.datetime.now(), Event.end_time >= datetime.datetime.now())
    count = db.session.query(Registration).join(Event).filter(and_(a,b)).count();

    data = {}
    data['result'] = 'error'
    data['message'] = 'Registration Failed - Server Error'

    cutoff = theEvent.start_time - datetime.timedelta(days=1);

    if(count<=2 or datetime.datetime.now() > cutoff):
        #Go ahead and register for requested event
        newRegistration = Registration(u_id=userInfo['id'], username=userInfo['name'], e_id=theEvent.id, timestamp=datetime.datetime.now(), remind=False, cancel_time=None, has_cancelled=False, no_show=False, notes=request.args.get("notes",""), needBus=bus)
        db.session.add(newRegistration)
        db.session.commit()
        data['result'] = 'success'
        data['message'] = 'Successfully Registered!'

    else:
        #Sorry too many registrations for you
        data['message'] = "Sorry, you have already registered for 3 events this week!"


    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(data) + ")"
    else:
        return json.dumps(data)


#Get user information
@app.route('/user')
def sess():
    return session['user_data']


@app.route('/')
def dashboard():
    return render_template("single_page_old.html")

if __name__ == "__main__":
    app.run()

