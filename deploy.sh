git add .
git commit -m $1
pip freeze > requirements.txt
git push heroku master