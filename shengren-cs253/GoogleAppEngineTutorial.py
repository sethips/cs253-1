import jinja2
import os
import webapp2

jinja_environment = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class GoogleAppEngineTutorial(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('GoogleAppEngineTutorial.html')
        template_values = {
            'test_string_0': 'Hello',
            'test_string_1': 'World',
            }
        self.response.out.write(template.render(template_values))
