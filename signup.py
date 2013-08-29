#http://stackoverflow.com/questions/11616260/how-to-get-all-objects-with-a-date-that-fall-in-a-specific-month-sqlalchemy
"""
NOTE TO READER: Please excuse the language present in this codebase. 
If you want a more censored version, open an issue. I may or may not get back to you.

 DO WHAT THE f*** YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE f*** YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE f*** YOU WANT TO.

"""

import os
import datetime
import calendar
import json
import hashlib

from flask import Flask
from flask import request

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ssdigfrrpvgjev:cTzHaJFPU5LekOPl7cUEnkqEP8@ec2-54-225-68-241.compute-1.amazonaws.com:5432/d1a8ndh1lhq25k"
app.config['DEBUG'] = True;
db = SQLAlchemy(app)
