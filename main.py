# encoding=utf-8
"""Made by delphi for himself's blog"""

import re
import os
from io import StringIO
from bs4 import BeautifulSoup
from lxml import etree

from flask import Flask
from flask import render_template

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def format_new_article(content, file_path):
    soup = BeautifulSoup(content, 'lxml')
    note = soup.find("div", attrs={'class': "note-wrapper"}).__str__()
    title = soup.find("title").contents[0]
    created = soup.find("meta", attrs={'name': "created"})['content']
    tags = soup.find("meta", attrs={'name': "tags"})['content']

    article = StringIO()
    article.write("{% extends 'layout.html' %}\n")
    article.write("<title>%s</title>\n" % title)
    article.write("""
{% block link %}
<link rel="stylesheet" style="text/css" href={{ url_for("static", filename="bear.css") }}>
<link rel="stylesheet" style="text/css" href={{ url_for("static", filename="style.css") }}>
{% endblock %}
    {% block header %}
              """)
    article.write("""
<meta name="created" content="%s">
<meta name="tags" content="%s">
                  """ % (created, tags))

    article.write("""
{% endblock %}
{% block body %}
                  """)
    article.write(note)
    article.write("\n{% endblock %}")

    with open(file_path, 'w') as f:
        f.write(article.getvalue())

@app.route("/")
def index():

    excludes = [".DS_Store"]
    article_path = os.path.dirname(os.path.realpath(__file__)) + "/templates/articles"
    articles = os.listdir(article_path)
    articles = [a for a in articles if a not in excludes]

    article_infos = []
    for article in articles[:1]:
        file_path = article_path + "/" + article
        with open(file_path, 'r') as f:
            content = f.read()

        content = content.replace("class=“desc”", "class='desc'")
        if "<!DOCTYPE html>" in content:
            format_new_article(content, file_path)

        soup = BeautifulSoup(content, 'lxml')
        tags = soup.find("meta", attrs={'name': "tags"})['content']
        created = soup.find("meta", attrs={'name': "created"})['content']
        title = soup.find("title").contents[0]
        desc = soup.find("div", attrs={'class': "desc"}).__str__()

        info = {
            'create_time': created,
            'tags': tags,
            'title': title,
            'desc': desc
        }
        article_infos.append(info)
    return render_template("home.html", articles=article_infos)


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

    file_path = ROOT_PATH + "/templates/articles/" + name
    print(file_path)
    if not os.path.exists(file_path):
        return render_template("404.html")
    file_path = "articles/" + name
    return render_template(file_path)


if __name__ == "__main__":

    print("Running on the port 8080......")
    app.run(host='0.0.0.0', port=8081, debug=True)
