import os, datetime
import requests
from rfeed import Item, Feed
from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)
app.config["DEBUG"] = True

# def parse(url):
#     return rfeed.parse(url)

@app.route("/rss", methods=['GET'])
def summary():
    res = requests.get("http://localhost:5001/articles/recent/meta/10")
    if res.status_code is 200:
        data = json.dumps(res)
        for articles in data:
            item = Item(
                    title = articles['title'],
                    author = articles['author'],
                    pubDate = datetime.datetime(2014, 12, 29, 10, 00),
                    link = articles['url']
                )
        feed = Feed(
            title = "A summary feed listing",
            link = "http://127.0.0.1:5400/rss",
            description = "a summary feed listing the title, author, date, and link for 10 most recent articles",
            language = "en-US",
            lastBuildDate = datetime.datetime.now(),
            items = [item]
        )
        return feed.rss()
    else:
        return jsonify({'Error': 'Not found'}), 404


#A full feed containing the full text for each article, its tags as RSS categories, and a comment count.

@app.route("/rss/full_feed", methods = ['GET'])
def full_feed():
    a_response = requests.get("http://127.0.0.1:5000/articles/recent/10")
    t_response = requests.get("http://127.0.0.1:5300/article/get?url=/tags")
    c_response = requests.get("http://127.0.0.1:5200/article/get?id=/comments/count")

    if a_response.status_code is 200:
        a_data = a_response.json()
        t_data = t_response.json()
        c_data = c_response.json()
        for a in a_data:
            item1 = Item(
                title = a_data['title'],
                author = a_data['author'],
                description = a_data['body'],
                categories = t_data['tag'],
                comments = c_data['count'],
                pubDate = datetime.datetime(2014, 12, 29, 10, 00),
                link = a_data['url']
            )
    feed = Feed(
        title = "Full feed",
        link = "http://127.0.0.1:5401/rss/full_feed",
        description = "A full feed containing the full text for each article, its tags as RSS categories, and a comment count.",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        item = [item1]
    )
    return feed.rss()

#A comment feed for each articles
@app.route("/rss/comments", methods = ['GET'])
def comment_feed():
    a_response = requests.get("http://127.0.0.1:5001/articles/recent/meta/10")
    a_data = a_response.json()
    comments = []

    for a in a_data:
        c_response = requests.get("http://127.0.0.1:5200/article/get?id=/comments/count")
        c_data = c_response.json()

        for c in c_data:
            comments.append(
                Item(
                    title = c['title'],
                    author = c['author'],
                    description = c['body'],
                    pubDate = datetime.datetime(2014, 12, 29, 10, 00),
                    link = c['url']
                )
            )
    feed = Feed(
        title = "Comment feed",
        link = "http://127.0.0.1:5402/rss/comments",
        description = "A comment feed for each articles",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        item = comments
    )
    print(feed.rss())



if __name__ == '__main__':
    app.run()
