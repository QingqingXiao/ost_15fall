from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
import model

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class DeleteAll(webapp2.RequestHandler):
    def get(self):
        query = model.
        for resource in model.Resource.all():
            resource.key.delete()
        self.redirect('/view')



application = webapp2.WSGIApplication([
    ('/deleteAll', DeleteAll),
], debug=True)