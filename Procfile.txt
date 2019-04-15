users: FLASK_APP=users.py flask run -p $PORT
articles: FLASK_APP=articles.py flask run -p $PORT
comments: FLASK_APP=comments.py flask run -p $PORT
tags: FLASK_APP=tags.py flask run -p $PORT
feed: FLASK_APP=feed.py flask run -p $PORT
EOM