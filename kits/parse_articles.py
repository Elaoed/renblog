# -*- coding: utf-8 -*-

import re
import os
from io import StringIO
from bs4 import BeautifulSoup

from config.conf import conf

def parse_articles():
    excludes = [".DS_Store"]
    article_path = os.path.dirname(os.path.realpath(__file__))
    article_path = os.path.dirname(article_path) + "/templates/articles"

    articles = os.listdir(article_path)
    articles = [a for a in articles if a not in excludes]

    article_infos = []
    for article in articles[:1]:
        file_path = article_path + "/" + article
        with open(file_path, 'r') as f:
            content = f.read()

        content = content.replace("class=“desc”", "class='desc'")
        content = content.replace("<i>", "_")
        content = content.replace("</i>", "_")
        if "<!DOCTYPE html>" in content:
            format_new_article(content, file_path)

        soup = BeautifulSoup(content, 'lxml')
        tags = soup.find("meta", attrs={'name': "tags"})['content']
        created = soup.find("meta", attrs={'name': "created"})['content']
        title = soup.find("title").contents[0]
        desc = soup.find("div", attrs={'class': "desc"}).__str__()
        year = created[:4]
        date = created[5:10]
        info = {
            'filename': article,
            'created': created,
            'tags': tags,
            'title': title,
            'desc': desc,
            'year': year,
            'date': date
        }
        article_infos.append(info)
    conf['articles'] = article_infos


def format_new_article(content, file_path):
    soup = BeautifulSoup(content, 'lxml')
    note = soup.find("div", attrs={'class': "note-wrapper"}).__str__()
    title = soup.find("title").contents[0]
    tags = soup.find("meta", attrs={'name': "tags"})['content']

    created = soup.find("meta", attrs={'name': "created"})['content']
    res = re.match(r"^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})", created)
    created = " ".join([res.group(1), res.group(2)])

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
