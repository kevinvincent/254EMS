#http://stackoverflow.com/questions/16433338/inserting-new-records-with-one-to-many-relationship-in-flask-sqlalchemy

#import Main App
from signup import *



#Figure it out
class Event(db.Model):
    __tablename__ = 'Event'

    #Id's FTW - unique and fresh, don't mess with it
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text)

    description = db.Column(db.Text)

    #--> event_Category.
    et_id = db.Column(db.Integer, db.ForeignKey('Event_Category.id'))

    #Starting Date and Time of Event
    start_time = db.Column(db.DateTime)

    #Ending Date and Time of Event
    end_time = db.Column(db.DateTime)

    #Is it open?
    available = db.Column(db.Boolean)

    #Has it been cancelled?
    cancelled = db.Column(db.Boolean)

    #The registrations with the current event
    registrations = db.relationship('Registration', backref='Event',
                                lazy='dynamic')

    #The metas with the current event
    metas = db.relationship('Event_Meta', backref='Event',
                                lazy='dynamic')

    def __repr__(self):
        return str(self.title)


    #Amount slots open
    #num_slots = db.Column(db.Integer)

    #specific info?
    #notes = db.Column(db.Text)
    

#I have no idea why this needs it's own table but, who gives a shit anyway?
class Event_Category(db.Model):
    __tablename__ = 'Event_Category'

    #unique event Category id
    id = db.Column(db.Integer, primary_key=True)

    #name of event Category
    name = db.Column(db.Text)

    #The events with the current event Category
    events = db.relationship('Event', backref='Event_Category',
                                lazy='dynamic')

    def __repr__(self):
        return str(self.name)


class Event_Meta(db.Model):
    __tablename__ = 'Event_Meta'

    id = db.Column(db.Integer, primary_key=True)

    e_id = db.Column(db.Integer, db.ForeignKey('Event.id'))
    
    key = db.Column(db.Text)

    value = db.Column(db.Text)

    def __repr__(self):
        return str(self.key + ": " + self.value)

#Holds the signups
class Registration(db.Model):
    __tablename__ = 'Registration'

    #Primary ID - It Better be unique.
    id = db.Column(db.Integer, primary_key=True)

    #users.id "what user?"
    u_id = db.Column(db.Integer)

    #username
    username = db.Column(db.Text)

    #events.id "wat event"
    e_id = db.Column(db.Integer, db.ForeignKey('Event.id'))

    #timestamp of registration
    timestamp = db.Column(db.DateTime)

    #would u like a reminder oh forgetful one?
    remind = db.Column(db.Boolean)

    #why u cancel?
    cancel_time = db.Column(db.DateTime, default=None)

    #Is it cancelled?
    has_cancelled = db.Column(db.Boolean, default=False)

    #why u no show up?
    no_show = db.Column(db.Boolean, default=False)

    #Do you need a bus
    needBus = db.Column(db.Boolean, default=False)

    #anything else?
    notes = db.Column(db.Text)

    def __repr__(self):
        return str(self.u_id)
