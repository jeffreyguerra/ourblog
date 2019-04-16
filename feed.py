import os, datetime
import requests, json
from rfeed import Item, Feed
from flask import Flask, jsonify, request, Response
# from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config["DEBUG"] = True

# def parse(url):
#     return rfeed.parse(url)

@app.route("/rss", methods=['GET'])
def summary():
    response = requests.get("http://localhost:5000/articles/recent/meta/10")
    data = response.json()
    for d in data:
        item1 = Item(
            title = d['title'],
            author = d['author'],
            pubDate = datetime.datetime(2014, 12, 29, 10, 00),
            link = "http://localhost:5000/articles/recent/10"
        )
    feed = Feed(
        title = "A summary feed listing",
        link = "http://localhost/rss",
        description = "a summary feed listing the title, author, date, and link for 10 most recent articles",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = [item1]
    )
    return feed.rss()


#A full feed containing the full text for each article, its tags as RSS categories, and a comment count.

@app.route("/rss/full_feed", methods = ['GET'])
def full_feed():
    a_response = requests.get("http://localhost/articles/recent/10")
    t_response = requests.get("http://localhost/article/get?url=/tags")
    c_response = requests.get("http://localhost/article/get?id=/comments/count")
    a_data = a_response.json()
    t_data = t_response.json()
    c_data = c_response.json()
    for a in a_data:
        title = a['title']
        author = a['author']
        description = a['body']

    for t in t_data:
        category = t['tag']

    for c in c_data:
        count = c['count']

    item2 = Item(
        title = title,
        author = author,
        description = description,
        category = category,
        comment = count,
        pubDate = datetime.datetime(2014, 12, 29, 10, 00)
    )

    feed = Feed(
        title = "Full feed",
        link = "http://localhost/rss/full_feed",
        description = "A full feed containing the full text for each article, its tags as RSS categories, and a comment count.",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        item = [item2]
    )
    return feed.rss()

#A comment feed for each articles
@app.route("/rss/comments", methods = ['GET'])
def comment_feed():
    c_response = requests.get("http://localhost/article/get?url=/comments")
    c_data = c_response.json()
    for c in c_data:
        item3 = Item(
            title = c['title'],
            author = c['author'],
            comment = c['comment'],
            pubDate = datetime.datetime(2014, 12, 29, 10, 00),
            link = c['url']
        )

    feed = Feed(
        title = "Comment feed",
        link = "http://localhost/rss/comments",
        description = "A comment feed for each articles",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        item = [item3]
    )
    return feed.rss()

if __name__ == '__main__':
    app.run()
