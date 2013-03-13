import jinja2
import os
import webapp2
import logging
import time
from google.appengine.api import memcache
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape = True)

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

ALL_BLOGS_CACHE_KEY = 'all_blogs'
LAST_QUERIED_CACHE_KEY = 'last_queried'

class ProblemSet3(webapp2.RequestHandler):
    template = jinja_environment.get_template('ProblemSet3.html')
    def get(self):
        blogs = memcache.get(ALL_BLOGS_CACHE_KEY)
        last_queried = memcache.get(LAST_QUERIED_CACHE_KEY)
        if blogs is None:
            logging.error('DB QUERY')
            blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC')
            blogs = list(blogs)
            memcache.set(ALL_BLOGS_CACHE_KEY, blogs)
            last_queried = time.time()
            memcache.set(LAST_QUERIED_CACHE_KEY, last_queried)
        template_values = {
            'blogs': blogs,
            'time_past': str(int(time.time() - float(last_queried)))
            }
        self.response.out.write(self.template.render(template_values))

class ProblemSet3_NewPost(webapp2.RequestHandler):
    template = jinja_environment.get_template('ProblemSet3_NewPost.html')
    def get(self):
        self.response.out.write(self.template.render())
    def post(self):
        blog_subject = self.request.get('subject')
        blog_content = self.request.get('content')
        if blog_subject and blog_content:
            blog = Blog(subject = blog_subject, content = blog_content)
            blog.put()
            blog_id = str(blog.key().id())
            memcache.set(ALL_BLOGS_CACHE_KEY, None)
            self.redirect('/ps3/' + blog_id)
        else:
            template_values = {
                'subject': blog_subject,
                'content': blog_content,
                'error': 'Both subject and content are required.',
                }
            self.response.out.write(self.template.render(template_values))

class ProblemSet3_Post(webapp2.RequestHandler):
    template = jinja_environment.get_template('ProblemSet3_Post.html')
    def get(self, blog_id):
        blog_cache_key = 'permalink_' + blog_id
        last_queried_cache_key = 'last_queried_' + blog_id
        blog = memcache.get(blog_cache_key)
        if blog is None:
            blog = Blog.get_by_id(int(blog_id))
            memcache.set(blog_cache_key, blog)
            last_queried = time.time()
            memcache.set(last_queried_cache_key, last_queried)
        else:
            last_queried = memcache.get(last_queried_cache_key)
        template_values = {
            'subject': blog.subject,
            'created': blog.created,
            'content': blog.content,
            'time_past': str(int(time.time() - float(last_queried)))
            }
        self.response.out.write(self.template.render(template_values))

