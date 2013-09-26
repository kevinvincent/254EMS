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
from simplekv.db.sql import SQLAlchemyStore
from flask.ext.kvsession import KVSessionExtension
store = SQLAlchemyStore(db.engine, db.metadata, 'sessions')
kvsession = KVSessionExtension(store, app)



@app.before_request
def gateKeeper():

    start = datetime.datetime.now()
    if 'user_id' in session:
        delta = datetime.datetime.now() - start
        app.logger.info(delta.microseconds)
        return

    #Na = off you go to be authenticated then
    else:
        app.logger.info("WP_COOKIE_CHECK")
        #Check if the wp cookie exists. It BETTER be chocolate chip.
        wpCookieExists = False
        wpCookieData = "";
        for cookie in request.cookies:
            if 'wordpress_logged_in' in cookie:
                wpCookieExists = True
                wpCookieData = request.cookies[cookie]
                break
        app.logger.info("WP_COOKIE_CHECK")

        #If it doesn't, send them to go get a cookie from the cookie monster (wp login page) and come back to gatekeeper caller
        if not wpCookieExists:
            return redirect("http://www.team254.com/wp-login.php?redirect_to=http://www.team254.com/auth/?sub="+"www"+"&path="+"/") # <-- cookie monster

        #If it does, go get their user data from wp and make em a sandwich (affecionately known as a session)
        else:
            app.logger.info("API")
            r = requests.get(AUTH_URL+"?cookie="+wpCookieData)
            app.logger.info("API")

            #check if good
            if r.status_code == 200:

                app.logger.info("SET_SESSIONS")
                #get json response and remove stupid unicode signature
                user_data = r.json()
                user_data['signature'] == ""

                #set session cookie with id
                session['user_id'] = user_data['id'];
                session['user_data'] = json.dumps(user_data)
                app.logger.info("SET_SESSIONS")

            else:
                pass

@app.route('/')
def login():
    return "MAIN PAGE"

@app.route('/sess')
def sess():
    return session['user_data']






