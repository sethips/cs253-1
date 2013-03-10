import jinja2
import os
import webapp2

from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape = True)

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class ProblemSet3(webapp2.RequestHandler):
    template = jinja_environment.get_template('ProblemSet3.html')
    def get(self):
        blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC')
        template_values = {
            'blogs': blogs,
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
        blog = Blog.get_by_id(int(blog_id))
        template_values = {
            'subject': blog.subject,
            'created': blog.created,
            'content': blog.content,
            }
        self.response.out.write(self.template.render(template_values))

