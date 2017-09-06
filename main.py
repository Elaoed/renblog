# encoding=utf-8
"""Made by delphi for himself's blog"""

import os

from flask import Flask
from flask import render_template

from kits import initialize
from config.conf import conf

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
def index():
    return render_template("home.html", articles=conf['articles'])

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

@app.route("/archive")
def archive():

    years = [article['year'] for article in conf['articles']]
    years = set(years)
    years = sorted(years, key=lambda x: x, reverse=True)
    return render_template("archive.html", articles=conf['articles'], years=years)


if __name__ == "__main__":
    initialize()
    conf['logger'].info("Running on the port %d......", conf['env']['port'])
    app.run(host='0.0.0.0', port=conf['env']['port'], debug=conf['env']['debug'])
