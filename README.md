cheesy-signups 
============== 
The signup system for FRC - maybe extended later to other signupss 

**Calendar View**

![Screenshot 1](https://raw2.github.com/Team254/cheesy-signups/master/screenshots/1.png?token=1350245__eyJzY29wZSI6IlJhd0Jsb2I6VGVhbTI1NC9jaGVlc3ktc2lnbnVwcy9tYXN0ZXIvc2NyZWVuc2hvdHMvMS5wbmciLCJleHBpcmVzIjoxMzkwMDk0MjIxfQ%3D%3D--704c134f05f60c0cfccfe52b4fddf05f25aa3953) 

**Event and Registration View**

![Screenshot 2](https://raw2.github.com/Team254/cheesy-signups/master/screenshots/2.png?token=1350245__eyJzY29wZSI6IlJhd0Jsb2I6VGVhbTI1NC9jaGVlc3ktc2lnbnVwcy9tYXN0ZXIvc2NyZWVuc2hvdHMvMi5wbmciLCJleHBpcmVzIjoxMzkwMDk0MjkyfQ%3D%3D--0d105bf3239e33698d2e74502f155988dff28f25) 

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
