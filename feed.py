import os, datetime, flask
import requests, json
from rfeed import Item, Feed
from flask import Flask, jsonify, request, Response
# from flask_basicauth import BasicAuth


app = flask.Flask(__name__)

@app.route("/rss", methods=['GET'])
def summary():
    response = requests.get("http://localhost/articles/recent/meta/10")
    data = response.json()
    item = []
    for d in data:
        item1 = Item(
            title = d['title'],
            author = d['author'],
            pubDate = datetime.datetime(2014, 12, 29, 10, 00),
            link = "http://localhost/articles/recent/meta/10"
        )
        item.append(item1)
    feed = Feed(
        title = "A summary feed listing",
        link = "http://localhost/rss",
        description = "a summary feed listing the title, author, date, and link for 10 most recent articles",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = item
    )
    return feed.rss()


#A full feed containing the full text for each article, its tags as RSS categories, and a comment count.

@app.route("/rss/full_feed", methods = ['GET'])
def full_feed():
    response = requests.get("http://localhost/articles/recent/10")
    data = response.json()
    articles = []

    for d in data:
        article_id = d['url'].split('/')[-1]
        item2 = Item(
            title = d['title'],
            pubDate = datetime.datetime(2014, 12, 29, 10, 00),
            link = "http://localhost/article/"+str(d['article_id'])
        )
        a_response = requests.get("http://localhost/article/" + str(d['article_id']))
        a_data = a_response.json()
        item2.title = a_data['title']
        item2.author = a_data['author']
        item2.description = a_data['body']

        c_response = requests.get("http://localhost/article/comments/count/" + str(d['article_id']))
        c_data = c_response.json()
        item2.comments = c_data['count']

        t_response = requests.get("http://localhost/article/tags/" + str(d['article_id']))
        t_data = t_response.json()
        item2.categories = t_data['tags']
        articles.append(item2)

    feed = Feed(
        title = "Full feed",
        link = "http://localhost/rss/full_feed",
        description = "A full feed containing the full text for each article, its tags as RSS categories, and a comment count.",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        item = articles
    )
    return feed.rss()

#A comment feed for each articles
@app.route("/rss/comments", methods = ['GET'])
def comment_feed():
    a_response = requests.get("http://localhost/articles/recent/10")
    a_data = a_response.json()
    comments = []
    for a in a_data:
        article_id = a['url'].split('/')[-1]
        c_response = requests.get("http://localhost/article/comments/" + str(a['article_id']))
        c_data = c_response.json()
        for c in c_data:
            item3 = Item(
                author = c['author'],
                comment = c['comment'],
                pubDate = datetime.datetime(2014, 12, 29, 10, 00),
                link = "http://localhost/article/" + str(c['article_id'])
            )
            comments.append(item3)

    feed = Feed(
        title = "Comment feed",
        link = "http://localhost/rss/comments",
        description = "A comment feed for each articles",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        item = comments
    )
    return feed.rss()
