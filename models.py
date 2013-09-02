#import Main App
from signup import *


#I have no idea why this needs it's own table but, who gives a shit anyway?
class event_type(db.Model):

    #unique event type id
    event_id = db.Column(db.Integer, primary_key=True)

    #name of event type
    type = db.Column(db.Text)

#Figure it out
class event(db.Model):

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

#Holds the signups
class registration(db.Model):

    #Primary ID - It Better be unique.
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


#Caching the json response (wouldn't wanna hug the auth api to death), holds session data for each user
class user(db.Model):

    #More Id's FTW - unique and fresh, don't mess with it
    id = db.Column(db.Integer, primary_key=True)

    #Pure json response from auth api
    user_data = db.Column(db.Text)