# encoding=utf-8
u"""Made by delphi for himself's blog"""

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import binascii
# from lxml import etree

from tornado.options import define, options
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


class BaseHandler(tornado.web.RequestHandler):
    TOKEN_LIST = {}

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def new_token(self):
        while True:
            _token = binascii.hexlify(os.urandom(16)).decode('utf-8')
            if _token not in self.TOKEN_LIST:
                return _token

    def on_login_success(self, new_token, user_id):
        # 和@tornado.web.authenticated对应 如果验证成功才可继续 验证不成功就跳转到指定url
        self.set_cookie('_token', new_token)
        self.TOKEN_LIST[new_token] = user_id

    def get_current_user(self):
        # 通过token获取已登录的用户的id
        token = self.get_cookie('_token')
        if token and token in self.TOKEN_LIST:
            user_id = self.TOKEN_LIST[token]
            return user_id
        return None


class IndexHandler(BaseHandler):
    """Home page"""

    def get(self):
        page = self.get_argument("page", "1")
        try:
            page = int(page)
        except ValueError:
            page = 1

        articles = os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/articles")
        displays = [x.split(".")[0] for x in articles[(page - 1) * 10:10 * page]]
        page_numbers = len(articles) // 10
        if len(articles) % 10 > 0:
            page_numbers += 1
        data = {
            'articles': displays,
            'total_page': page_numbers,
            'current_page': page,
            'create_data': "",
            'tags': ""
        }
        return self.render("home.html", data=data)


class ErrorHandler(BaseHandler):
    """"""

    def get(self):
        return self.finish("404")


class AboutHandler(BaseHandler):
    """Probably it's a resume of myself"""

    def get(self):
        return self.render("about.html")

class SeoHandler(BaseHandler):
    """Probably it's a resume of myself"""

    def get(self):
        return self.render("seo.html")


class ArticleHandler(BaseHandler):
    """Article page"""

    def get(self):
        article_name = self.get_argument("name", "")
        if not article_name:
            self.redirect('/404')
        file_path = ROOT_PATH + "/articles/" + article_name + ".html"
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
        return self.render(file_path)


def create_app():
    define("port", default=8081, help="run on the given port")

    settings = dict(
        template_path=os.path.join(ROOT_PATH, "templates"),
        static_path=os.path.join(ROOT_PATH, "static"),
        debug=True,
        # xsrf_cookies=True,
        # cookie_secret=CONFIG['COOKIE_SECRET'],
        gzip=True,
        login_url='/'
    )
    app = tornado.web.Application(handlers=[(r"/", IndexHandler),
                                            (r"/articles", ArticleHandler),
                                            (r"/404", ErrorHandler),
                                            (r"/about", AboutHandler),
                                            (r"/seoDataScrapy", SeoHandler),
                                            ], **settings)
    return app


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(create_app())
    http_server.listen(options.port)
    print("Running on the port " + str(options.port) + " ......")
    tornado.ioloop.IOLoop.instance().start()
