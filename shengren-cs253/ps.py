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

signup_form="""
<h2>Signup</h2>
<form method="post">
  <table>
    <tr>
      <td class="label">
        Username
      </td>
      <td>
        <input type="text" name="username" value="%(username)s">
      </td>
      <td class="error">
        %(error_username)s
      </td>
    </tr>

    <tr>
      <td class="label">
        Password
      </td>
      <td>
        <input type="password" name="password" value="">
      </td>
      <td class="error">
        %(error_password)s
      </td>
    </tr>

    <tr>
      <td class="label">
        Verify Password
      </td>
      <td>
        <input type="password" name="verify" value="">
      </td>
      <td class="error">
        %(error_verify)s
      </td>
    </tr>

    <tr>
      <td class="label">
        Email (optional)
      </td>
      <td>
        <input type="text" name="email" value="%(email)s">
      </td>
      <td class="error">
        %(error_email)s
      </td>
    </tr>
  </table>

  <input type="submit">
</form>
"""

import re
USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE    = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class ProblemSet2_2(webapp2.RequestHandler):
    def validateUsername(self, username):
        return USERNAME_RE.match(username)
    def validatePassword(self, password):
        return PASSWORD_RE.match(password)
    def validateVerify(self, password, verify):
        return password == verify
    def validateEmail(self, email):
        return email == '' or EMAIL_RE.match(email)
    def writeFormWithErrors(self, username, password, verify, email):
        error_username = '' if self.validateUsername(username) else "That's not a valid username."
        error_password = '' if self.validatePassword(password) else "That wasn't a valid password."
        error_verify = ''
        if error_password == '' and not self.validateVerify(password, verify):
            error_verify = "Your passwords didn't match."
        error_email = '' if self.validateEmail(email) else "That's not a valid email."
        self.response.write(signup_form % {"username": username,
                                           "email": email,
                                           "error_username": error_username,
                                           "error_password": error_password,
                                           "error_verify": error_verify,
                                           "error_email": error_email})
    def get(self):
        self.response.write(signup_form % {"username": '',
                                           "email": '',
                                           "error_username": '',
                                           "error_password": '',
                                           "error_verify": '',
                                           "error_email": ''})
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify  = self.request.get('verify')
        email    = self.request.get('email')
        if self.validateUsername(username) and \
           self.validatePassword(password) and \
           self.validateVerify(password, verify) and \
           self.validateEmail(email):
            self.redirect('/ps2_2_welcome?username=%s' % username)
        else:
            self.writeFormWithErrors(username, password, verify, email)

class ProblemSet2_2_Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write('Welcome, %s!' % username)

import GoogleAppEngineTutorial

import ProblemSet3

import ProblemSet4

import ProblemSet5

import ProblemSet6

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/ps1', ProblemSet1),
                               ('/ps2', ProblemSet2),
                               ('/ps2_2', ProblemSet2_2),
                               ('/ps2_2_welcome', ProblemSet2_2_Welcome),
                               ('/gaet', GoogleAppEngineTutorial.GoogleAppEngineTutorial),
                               ('/ps3', ProblemSet3.ProblemSet3),
                               ('/ps3/newpost', ProblemSet3.ProblemSet3_NewPost),
                               (r'/ps3/(\d+)', ProblemSet3.ProblemSet3_Post),
                               ('/ps3/signup', ProblemSet4.ProblemSet4_Signup),
                               ('/ps3/welcome', ProblemSet4.ProblemSet4_Welcome),
                               ('/ps3/login', ProblemSet4.ProblemSet4_Login),
                               ('/ps3/logout', ProblemSet4.ProblemSet4_Logout),
                               ('/ps3/.json', ProblemSet5.AllPosts),
                               (r'/ps3/(\d+).json', ProblemSet5.SinglePost),
                               ('/ps3/flush', ProblemSet6.Flush),
                              ], debug = True)
