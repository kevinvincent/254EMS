for COMMIT_MESSAGE in "$@"
do
	pip freeze > requirements.txt
	git add .
	git commit -a -m "$COMMIT_MESSAGE"
	echo "Pushing...."
	git push heroku master
done;