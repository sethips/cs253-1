import jinja2
import os
import webapp2
import re
import hashlib

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape = True)

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE    = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class ProblemSet4_Signup(webapp2.RequestHandler):
    template = jinja_environment.get_template('ProblemSet4_Signup.html')
    def validateUsername(self, username):
        return USERNAME_RE.match(username)
    def validatePassword(self, password):
        return PASSWORD_RE.match(password)
    def validateVerify(self, password, verify):
        return password == verify
    def validateEmail(self, email):
        return email == '' or EMAIL_RE.match(email)
    def get(self):
        self.response.out.write(self.template.render())
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify   = self.request.get('verify')
        email    = self.request.get('email')
        error_username = error_password = error_verify = error_email = ''
        is_valid = True
        if not self.validateUsername(username):
            is_valid = False
            error_username = "That's not a valid username."
        if not self.validatePassword(password):
            is_valid = False
            error_password = "That wasn't a valid password."
        elif not self.validateVerify(password, verify):
            is_valid = False
            error_verify = "Your passwords didn't match."
        if not self.validateEmail(email):
            is_valid = False
            error_email = "That's not a valid email."
        if is_valid:
            h = hashlib.sha256(password).hexdigest()
            self.response.headers.add_header('Set-Cookie', \
                                             'account=%s|%s' % (str(username), h))
            self.redirect('/ps3/welcome') # Changed to ps3 for PS5 submission
        else:
            template_values = {
                'username': username,
                'email': email,
                'error_username': error_username,
                'error_password': error_password,
                'error_verify': error_verify,
                'error_email': error_email,
                }
            self.response.out.write(self.template.render(template_values))

class ProblemSet4_Welcome(webapp2.RequestHandler):
    template = jinja_environment.get_template('ProblemSet4_Welcome.html')
    def get(self):
        account = self.request.cookies.get('account')
        username = account.split('|')[0]
        template_values = {
            'username': username,
            }
        self.response.out.write(self.template.render(template_values))

class ProblemSet4_Login(webapp2.RequestHandler):
    template = jinja_environment.get_template('ProblemSet4_Login.html')
    def get(self):
        self.response.out.write(self.template.render())
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        account = self.request.cookies.get('account')
        if account and username == account.split('|')[0]:
            h = hashlib.sha256(password).hexdigest()
            if h == account.split('|')[1]:
                self.redirect('/ps3/welcome') # Changed to ps3 for PS5 submission
                return
        error = 'Invalid login'
        template_values = {
            'error': error,
            }
        self.response.out.write(self.template.render(template_values))

class ProblemSet4_Logout(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'account=;Path=/')
        self.redirect('/ps3/signup') # Changed to ps3 for PS5 submission

