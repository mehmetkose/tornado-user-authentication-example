#!/usr/bin/env python
#-*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")
		
class MainHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		self.render('index.html', user=self.current_user)

class LoginHandler(BaseHandler):
	def get(self):
		self.render('login.html')
	def post(self):
		getusername = self.get_argument("username")
		getpassword = self.get_argument("password")
		# TODO : Check data from DB
		if "demo" == getusername and "demo" == getpassword:
		    self.set_secure_cookie("user", self.get_argument("username"))
		    self.redirect(self.reverse_url("main"))
		else:
		    wrong = self.get_secure_cookie("wrong")
		    if not wrong:
		    	wrong = 0
		    self.set_secure_cookie("wrong", str(int(wrong)+1))
		    self.write('Something Wrong With Your Data <a href="/login">Back</a> '+str(wrong))

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", self.reverse_url("main")))

class Application(tornado.web.Application):
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "login_url": "/login",
			'template_path': os.path.join(base_dir, "templates"),
			'static_path': os.path.join(base_dir, "static"),
			'debug':True,
			"xsrf_cookies": True,
		}
		
        tornado.web.Application.__init__(self, [
            tornado.web.url(r"/", MainHandler, name="main"),
            tornado.web.url(r'/login', LoginHandler, name="login"),
            tornado.web.url(r'/logout', LogoutHandler, name="logout"),
        ], **settings)

def main():
    tornado.options.parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

