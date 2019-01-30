#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
# import time
import time

import jinja2
import webapp2
from models import Movie

reload(sys)
sys.setdefaultencoding('utf8')


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)



class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        movieList = Movie.query(Movie.movieDeleted == False).fetch()
        movieDeleted = Movie.query(Movie.movieDeleted == True).fetch()

        params = {"movieList": movieList, "movieDeleted": movieDeleted}
        return self.render_template("index.html", params=params)


class AddMovieHandler(BaseHandler):
    def get(self):
        movieList = Movie.query(Movie.movieDeleted == False).fetch()
        movieDeleted = Movie.query(Movie.movieDeleted == True).fetch()
        task = ""

        params = {"movieList": movieList, "movieDeleted": movieDeleted, "task": task}

        return self.render_template("add.html", params=params)

    def post(self):
        movieTitle = self.request.get("movieTitle")
        movieExcerpt = self.request.get("movieExcerpt")
        movieRating = int(self.request.get("movieRating"))
        movieThumb = self.request.get("movieThumb")


        newMovie = Movie(movieTitle=movieTitle, movieExcerpt=movieExcerpt, movieRating=movieRating, movieThumb=movieThumb)

        newMovie.put()

        time.sleep(1)

        movieList = Movie.query(Movie.movieDeleted == False).fetch()
        movieDeleted = Movie.query(Movie.movieDeleted == True).fetch()

        params = {"movieList": movieList, "movieDeleted": movieDeleted}

        return self.render_template("index.html", params=params)
#
#
# class EditHandler(BaseHandler):
#     def get(self, task_id):
#         edit = Todo.get_by_id(int(task_id))
#
#         params = {"task": edit}
#
#         return self.render_template("add.html", params=params)
#
#     def post(self, task_id):
#         status = self.request.get("status")
#         task = self.request.get("task")
#
#         edit = Todo.get_by_id(int(task_id))
#
#         if status == "True":
#             status = True
#         else:
#             status = False
#
#         edit.task = task
#         edit.status = status
#
#         edit.put()
#
#         params = fetchReload() ## from function
#
#         return self.render_template("index.html", params=params)
#
#
# class DeleteHandler(BaseHandler):
#     def get(self, task_id):
#         edit = Todo.get_by_id(int(task_id))
#         params = {"task": edit}
#
#         return self.render_template("delete.html", params=params)
#
#     def post(self, task_id):
#         edit = Todo.get_by_id(int(task_id))
#
#         edit.deleted = True
#
#         edit.put()
#
#         params=fetchReload() ## from function
#
#         return self.render_template("index.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/add', AddMovieHandler),
    # webapp2.Route('/edit/<task_id:\d+>', EditHandler),
    # webapp2.Route('/delete/<task_id:\d+>', DeleteHandler),
], debug=True)
