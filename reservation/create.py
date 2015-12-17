from google.appengine.api import users
from sets import Set
import os
import webapp2
import jinja2
import model

JINJA_ENVIRONMENT = jinja2.Environment(
						loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
						extensions = ['jinja2.ext.autoescape'],
						autoescape = True)

class createResource(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/createResource.html')
		self.response.write(template.render())
	def post(self):
		name = self.request.get('name')
		description = self.request.get('description')
		if name == '' or description == '':
			template_values = {'message' : 'Resource name and description could not be null!'}
			template = JINJA_ENVIRONMENT.get_template('templates/message.html')
			self.response.write(template.render(template_values))
		else:
			resource = model.Resource()
			resource.owner = users.get_current_user()
			resource.name = name
			resource.description = description
			tags_readin = self.request.get('tags')
			tokens = tags_readin.split(";")
			tags = []
			for tag in tokens:
				if tag != '':
					tag = tag.strip()
					tags.append(tag)
			resource.tags = tags
			resource.put()
			rid = resource.key.id()

			# url = '/view?qid=' + repr(int(qid))
			# self.redirect(url)

application = webapp2.WSGIApplication([('/creater', createResource)], 
										debug = True)

