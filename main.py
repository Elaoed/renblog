# encoding=utf-8
"""Made by delphi for himself's blog"""

import os
# import binascii
from lxml import etree

from flask import Flask
from flask import render_template

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


@app.route("/")
def index():

    excludes = [".DS_Store"]
    articles = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/templates/articles")
    articles = [a for a in articles if a not in excludes]
    data = {
        'articles': articles,
    }
    return render_template("home.html", data=data)


@app.route("/404")
def get(self):
    """404 page"""
    return render_template("404.html")

@app.route("/about")
def about():
    """ Resume of myself"""
    return render_template("about.html")

@app.route("/articles/<name>")
def article(name=""):

    # file_path = ROOT_PATH + "/articles/" + name
    # if not os.path.exists(file_path):
    #     return "404"
    file_path = "articles/" + "Phrase.html"

    # with open(file_path, 'r') as f:
    #     article = f.read()
    # selector = etree.HTML(article)
    # note = selector.xpath("/html/body/div[@class=\"note-wrapper\"]")
    # title = selector.xpath("/html/body/div[@class=\"note-wrapper\"]/h1/text()")
    # title = title[0].encode('utf-8')
    # content = note[0].xpath('string(.)').encode('utf-8')
    # data = {
    #     'title': title,
    #     'content': content
    # }
    return render_template(file_path)


if __name__ == "__main__":

    print("Running on the port 8080......")
    app.run(host='0.0.0.0', port=8081, debug=False)
