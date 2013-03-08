import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Udacity cs253 Web Application - My problem set solutions')

class ProblemSet1(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Udacity!')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/ps1', ProblemSet1)
                              ], debug = True)
