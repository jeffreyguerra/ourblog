import os, datetime
import requests
from rfeed import Item, Feed
from flask import Flask, jsonify, request as flask_request

app = Flask(__name__)

@app.route("/rss/summary", methods=['GET'])
def summary():
    response = requests.get("http://127.0.0.1:5000/articles/recent/meta/10")
    data = response.get_json()
    article_sum = []
    for d in data:
        article_sum.append(
            Item(
                title = d['title'],
                author = d['author'],
                pubDate = datetime.datetime(2014, 12, 29, 10, 00),
                link = d['url']
            )
        )
    feed = Feed(
        title = "A summary feed listing",
        link = "http://127.0.0.1:5000/rss/summary",
        description = "a summary feed listing the title, author, date, and link for 10 most recent articles",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = article_sum
    )
    print(feed.rss())
#
# @app.route("/rss/full_feed", methods = ['GET'])
# def full_feed():
#     a_response = requests.get("http://127.0.0.1:5000/articles/recent/10")
#     data = a_response.get_json()
#     t_response = requests.get("http://127.0.0.1:5000/article/tags") ###
#     data = t_response.get_json()
#     article = []
#     tag = []
#









if __name__ == '__main__':
    app.run()
