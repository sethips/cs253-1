import webapp2
import re
import jinja2
import os
import logging
import hashlib
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    )
    #autoescape = True)

class User(db.Model):
    username = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

class Page(db.Model):
    entry = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    timestamp = db.DateTimeProperty(auto_now_add = True)

class MyHandler(webapp2.RequestHandler):
    def render(self, template, template_values = {}):
        self.response.out.write(template.render(template_values))

RE_USERNAME = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
RE_PASSWORD = re.compile(r'^.{3,20}$')
RE_EMAIL = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

class Signup(MyHandler):
    template = jinja_environment.get_template('Signup.html')
    def validateUsername(self, username):
        return RE_USERNAME.match(username)
    def validatePassword(self, password):
        return RE_PASSWORD.match(password)
    def validateVerify(self, password, verify):
        return password == verify
    def validateEmail(self, email):
        return not email or RE_EMAIL.match(email)
    def get(self):
        self.render(self.template)
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error_username = error_password = error_verify = error_email = ''
        is_valid = True
        if not self.validateUsername(username):
            is_valid = False
            error_username = 'Invalid username'
        if not self.validatePassword(password):
            is_valid = False
            error_password = 'Invalid password'
        elif not self.validateVerify(password, verify):
            is_valid = False
            error_verify = 'Not match'
        if not self.validateEmail(email):
            is_valid = False
            error_email = 'Invalid email'
        user_key = db.Key.from_path('User', username)
        user = db.get(user_key)
        if user:
            is_valid = False
            username = ''
            error_username = 'User exists'
        if is_valid:
            pw_hash = hashlib.sha256(password).hexdigest()
            user = User(key_name = username,
                        username = username,
                        pw_hash = pw_hash,
                        email = email)
            user.put()
            self.response.headers.add_header(\
                'Set-Cookie', 'user=%s|%s' % (str(username), pw_hash))
            self.redirect('/')
        else:
            template_values = {
                'username': username,
                'email': email,
                'error_username': error_username,
                'error_password': error_password,
                'error_verify': error_verify,
                'error_email': error_email,
                }
            self.render(self.template, template_values)

class Login(MyHandler):
    template = jinja_environment.get_template('Login.html')
    def get(self):
        self.render(self.template)
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        error = ''
        if username and password:
            user_key = db.Key.from_path('User', username)
            user = db.get(user_key)
            if user:
                pw_hash = hashlib.sha256(password).hexdigest()
                if pw_hash == user.pw_hash:
                    self.response.headers.add_header(\
                        'Set-Cookie', 'user=%s|%s' % (str(username), pw_hash))
                    self.redirect('/')
                    return
                else:
                    error = 'Wrong password'
            else:
                error = 'User does not exist'
        else:
            error = 'Both username and password are required'
        template_values = {
            'error': error,
            }
        self.render(self.template, template_values)

class Logout(MyHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user=')
        self.redirect('/login')

class EditPage(MyHandler):
    template = jinja_environment.get_template('EditPage.html')
    def get(self, entry):
        fetch_back = db.GqlQuery(\
            "SELECT * FROM Page WHERE entry = '%s' ORDER BY timestamp DESC LIMIT 1" % entry)
        fetch_back = list(fetch_back)
        content = ''
        if len(fetch_back) == 1:
            page = fetch_back[0]
            content = page.content
        template_values = {
            'content': content,
            }
        self.render(self.template, template_values)
    def post(self, entry):
        content = self.request.get('content')
        error = ''
        user_from_cookie = self.request.cookies.get('user')
        if user_from_cookie:
            if len(user_from_cookie.split('|')) == 2:
                username, pw_hash = user_from_cookie.split('|')
                user_key = db.Key.from_path('User', username)
                user = db.get(user_key)
                if user:
                    if pw_hash == user.pw_hash:
                        if content:
                            page = Page(key_name = entry,
                                        entry = entry,
                                        author = username,
                                        content = content)
                            page.put()
                            self.redirect(entry)
                            return
                        else:
                            error = 'Content cannot be empty'
                    else:
                        error = 'Username and password do not match'
                else:
                    error = 'User does not exist'
            else:
                error = 'Invalid cookie'
        else:
            error = 'Login first'
        template_values = {
            'content': content,
            'error': error,
            }
        self.render(self.template, template_values)

class WikiPage(MyHandler):
    template = jinja_environment.get_template('WikiPage.html')
    def get(self, entry):
        fetch_back = db.GqlQuery(\
            "SELECT * FROM Page WHERE entry = '%s' ORDER BY timestamp DESC LIMIT 1" % entry)
        fetch_back = list(fetch_back)
        if len(fetch_back) == 1:
            page = fetch_back[0]
            template_values = {
                'content': page.content,
                }
            self.render(self.template, template_values)
        else:
            self.redirect('/_edit' + entry)

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/_edit' + PAGE_RE, EditPage),
                               (PAGE_RE, WikiPage),
                              ], debug = True)

