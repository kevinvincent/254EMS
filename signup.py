#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy
"""
NOTE TO YOU: 
- Please excuse the language present in this codebase.
- Extensive coding sessions cause mental breakdowns. Source: http://en.wikipedia.org/wiki/Defenstration
- If you want a more censored version, open an issue. I may or may not get back to you.


APPLICATION INFORMATION:

TODO: Copious amounts of logging. 
Log. Every. Freaking. Thing.

TODO: Even more logging. Get the point yet?

"""

#Python libs
import os
import datetime
import calendar
import json
import hashlib
import requests

#Flask shit
from flask import Flask
from flask import *

#DB stuff that no one cares about
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_


#Config, Config, Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ssdigfrrpvgjev:cTzHaJFPU5LekOPl7cUEnkqEP8@ec2-54-225-68-241.compute-1.amazonaws.com:5432/d1a8ndh1lhq25k"
app.config['DEBUG'] = True;
db = SQLAlchemy(app)

#Super Super Super duper secret key - cookie signing
app.secret_key = '\xe8\xec~G:\xa9iZ{D|^\x1bvc}U\xac\xbc\x1e\xf4\xed\x8c'
BASE_URL = "http://localhost:5000" #no trailing slash

#Application Stuff in other files
from models import *

import logging
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

@app.before_request
def gateKeeper():

    #DEBUG
    if request.endpoint == "wp_login" or request.endpoint == "wp_logout":
        return


    #Are you authenticated with this app bro?
    if 'user_id' in session:
        return #Ya = return   

    #Na = off you go to be authenticated then
    else:
        #Check if the wp cookie exists. It BETTER be chocolate chip.
        wpCookieExists = False
        wpCookieData = "";
        for cookie in request.cookies:
            if 'wordpress_logged_in' in cookie:
                wpCookieExists = True
                wpCookieData = cookie;
                break

        #If it doesn't, send them to go get a cookie from the cookie monster (wp login page) and come back to gatekeeper caller
        if not wpCookieExists:
            return redirect("http://www.team254.com/wp-login.php?redirect_to="+request.url) # <-- cookie monster

        #If it does, go get their user data from wp and make em a sandwich (affecionately known as a session)
        else:

            # hit the auth api, HARD
            payload = {'cookie':"#"+wpCookieData, 'trollololol':'u mad bro?'} # <-- Whoever checks the logs next is gonna get trolled, HARD
            r = requests.get("http://www.team254.com/auth/", params = payload)

            #check if good
            if r.status_code == 200:

                #get json response and remove stupid unicode signature
                user_data = r.json()
                user_data['signature'] == ""

                #set session cookie with id
                session['user_id'] = user_data['id'];

                #cache response to db
                the_user = user(int(user_data[id]), json.dumps(user_data));
                db.session.add(the_user);
                db.session.commit();

            else:
                #TODO: What do if da cookie expire?
                pass





@app.route('/')
def login():
    return "MAIN PAGE"



@app.route('/wp_login')
def wp_login():
    resp = make_response();
    resp.set_cookie('wordpress_logged_in')
    return resp


@app.route('/wp_logout')
def wp_logout():
    resp = make_response()
    resp.set_cookie('wordpress_logged_in', expires=0)
    return resp













