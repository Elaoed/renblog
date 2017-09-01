# encoding=utf-8
u"""Made by delphi for himself's blog"""

import os
import binascii
# from lxml import etree

from flask import Flask
from flask import render_template

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


@app.route("/")
def index():

    articles = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/articles")
    data = {
        'articles': articles,
        'create_data': "",
        'tags': ""
    }
    return render_template("home.html", data=data)


# class ErrorHandler(BaseHandler):
#     """"""

#     def get(self):
#         return self.finish("404")


# class AboutHandler(BaseHandler):
#     """Probably it's a resume of myself"""

#     def get(self):
#         return self.render("about.html")

# class SeoHandler(BaseHandler):
#     """Probably it's a resume of myself"""

#     def get(self):
#         return self.render("seo.html")


# class ArticleHandler(BaseHandler):
#     """Article page"""

#     def get(self):
#         article_name = self.get_argument("name", "")
#         if not article_name:
#             self.redirect('/404')
#         file_path = ROOT_PATH + "/articles/" + article_name + ".html"
#         # with open(file_path, 'r') as f:
#         #     article = f.read()
#         # selector = etree.HTML(article)
#         # note = selector.xpath("/html/body/div[@class=\"note-wrapper\"]")
#         # title = selector.xpath("/html/body/div[@class=\"note-wrapper\"]/h1/text()")
#         # title = title[0].encode('utf-8')
#         # content = note[0].xpath('string(.)').encode('utf-8')
#         # data = {
#         #     'title': title,
#         #     'content': content
#         # }
#         return self.render(file_path)


if __name__ == "__main__":

    print("Running on the port 8080......")
    app.run(host='0.0.0.0', port=8081, debug=True)
