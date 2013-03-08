import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Udacity cs253 Web Application - My problem set solutions')

class ProblemSet1(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Udacity!')

import cgi

form="""
<h2>Enter some text to ROT13:</h2>
<form method="post">
  <textarea name="text" style="height: 100px; width: 400px;">%(t)s</textarea>
  <br>
  <input type="submit">
</form>
"""

class ProblemSet2(webapp2.RequestHandler):
    def rot13(self, t):
        cs = list(t)
        for i in range(len(cs)):
            if cs[i].isalpha():
                if cs[i].islower():
                    cs[i] = chr((ord(cs[i]) - ord('a') + 13) % 26 + ord('a'))
                else:
                    cs[i] = chr((ord(cs[i]) - ord('A') + 13) % 26 + ord('A'))
        return "".join(cs)
    def writeForm(self, t = ''):
        self.response.write(form % {"t": t})
    def get(self):
        self.writeForm()
    def post(self):
        t = self.request.get('text')
        t = self.rot13(t)
        t = cgi.escape(t, quote = True)
        self.writeForm(t)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/ps1', ProblemSet1),
                               ('/ps2', ProblemSet2)
                              ], debug = True)
