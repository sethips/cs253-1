import webapp2
from google.appengine.api import memcache

class Flush(webapp2.RequestHandler):
    def get(self):
        memcache.flush_all()
        self.redirect('/ps3')

