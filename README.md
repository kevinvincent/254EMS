cheesy-signups 
============== 
The signup system for FRC - maybe extended later to other signupss 

![]() 

Stack Infomration 
-----------------
- Flask microframework for python
- SQL Alchemy for ORM
- Postgresql DB on Heroku
- KVSession Flask extension for Server Side sessions
- DB and App run on Heroku for now 


Files and Directories
--------------------------- 
- (dir) templates: html for frontend
- (dir) static: static css and js files
- (dir) dev: contains old code and a heroku deploy script
- (file) Procfile: Heroku config file
- (file) requirements.txt: Heroku requirements file (all these resources are necessary and can be installed via pip)
- (file) models.py: Holds all table schemas
- (file) signup.py: Main app with controllers


Status Updates: 
---------------
- DB models are done - 8/29/13
- Auth implemented. But I dont know if it works - 8/29/13
- Auth implemented and working! - 9/25/13
- Server can now handle jsonp requests (cross domain ajax for client) - 9/26/13
- Most stuff is done working on ui - 11/25/13
- MVP Released and Live - 1/30/14
