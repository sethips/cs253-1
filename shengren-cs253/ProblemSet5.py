import webapp2
import json
from google.appengine.ext import db

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AllPosts(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC')
        all_posts = []
        for blog in blogs:
            post = {'subject': blog.subject,
                    'content': blog.content,
                   }
            all_posts.append(post)
        json_str = json.dumps(all_posts)
        self.response.out.write(json_str)

class SinglePost(webapp2.RequestHandler):
    def get(self, blog_id):
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        blog = Blog.get_by_id(int(blog_id))
        json_str = json.dumps({'subject': blog.subject,
                               'content': blog.content,
                              })
        self.response.out.write(json_str)

