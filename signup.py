#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy


#Python libs
import os
import datetime
import calendar
import json
import hashlib
import requests

from flask import *


#DB stuff that no one cares about
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_


#Config, Config, Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ssdigfrrpvgjev:cTzHaJFPU5LekOPl7cUEnkqEP8@ec2-54-225-68-241.compute-1.amazonaws.com:5432/d1a8ndh1lhq25k"
app.config['DEBUG'] = False;
db = SQLAlchemy(app)

#Super Super Super duper secret key - cookie signing
app.secret_key = '\xe8\xec~G:\xa9iZ{D|^\x1bvc}U\xac\xbc\x1e\xf4\xed\x8c'
BASE_URL = "http://team254.com:5000" #no trailing slash
AUTH_URL = "http://team254.com/auth/"

#Application Stuff in other files
from models import *

#Logging
import logging
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

#KVSession
from simplekv.memory import DictStore
#from simplekv.db.sql import SQLAlchemyStore
from flask.ext.kvsession import KVSessionExtension

#store = SQLAlchemyStore(db.engine, db.metadata, 'sessions')
store = DictStore()
kvsession = KVSessionExtension(store, app)




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
        app.logger.info("WP_COOKIE_CHECK")

        if not wpCookieExists:
            return redirect("http://www.team254.com/wp-login.php?redirect_to=http://www.team254.com/auth/?sub="+"www"+"&path="+"/") # <-- cookie monster

        else:

            r = requests.get(AUTH_URL+"?cookie="+wpCookieData)
            
            if r.status_code == 200:

                user_data = r.json()
                user_data['signature'] == ""

                session['user_id'] = user_data['id'];
                session['user_data'] = json.dumps(user_data)

            else:
                pass


@app.route('/')
def login():
    return "MAIN PAGE"

@app.route('/sess')
def sess():
    return session['user_data']

@app.route('/loadView')
def loadView():
    data = {}
    data['title'] = "Test Event"
    data['allDay'] = True
    data['start'] = "2013-06-06 06:00:00"
    data['end'] = "2013-06-06 14:00:00"

    l = []
    l.append(data)

    #Handle Jsonp cross domain requests
    # - Basically allow this to be accesed from any domain through ajax
    if(request.args.get('callback') != None):
        return request.args.get('callback') + "(" + json.dumps(l) + ")"
    else:
        return json.dumps(l)    



