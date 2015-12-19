from google.appengine.api import users
import webapp2
import jinja2
import os
import model

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Edit(webapp2.RequestHandler):
    def get(self):
        rid = self.request.get('rid')
        user = users.get_current_user()
        if rid == '':
            template_values = {'message': 'No resource is specified!'}
            template = JINJA_ENVIRONMENT.get_template('templates/message.html')
            self.response.write(template.render(template_values))
        else:
            rid = long(rid)
            rid = int(rid)
            resource = model.Resource.get_by_id(rid)
            if resource.owner != user:
                template_values = {'message': 'You don\'t have the permission to edit this resource' }
                template = JINJA_ENVIRONMENT.get_template('templates/message.html')
                self.response.write(template.render(template_values))
            else:
                temp = ''
                for s in resource.tags:
                    temp = temp + ';' + s
                template_values = {'resource': resource, 'tags':temp}
                template = JINJA_ENVIRONMENT.get_template('templates/editResource.html')
                self.response.write(template.render(template_values))
    def post(self):
        rid = self.request.get('rid')
        rid = long(rid)
        rid = int(rid)
        name = self.request.get('name')
        description = self.request.get('description')
        availableStartTime = self.request.get('availableStartTime')
        availableEndTime = self.request.get('availableEndTime')
        if name == '':
            template_values = {'message': 'Name cannot be null!'}
            template = JINJA_ENVIRONMENT.get_template('templates/message.html')
            self.response.write(template.render(template_values))
        else:
            resource = model.Resource.get_by_id(rid)
            resource.name = name
            resource.description = description
            resource.availableStartTime = availableStartTime
            resource.availableEndTime = availableEndTime
            temp = self.request.get('tags')
            token = temp.split(";")
            tags = []
            for str in token:
                if str != '':
                    str = str.strip()
                    tags.append(str)
            resource.tags = tags
            resource.put()
            rid = resource.key.id()
            temp = repr(int(rid))
            url = '/view?rid=' + temp
            self.redirect(url)
        
application = webapp2.WSGIApplication([('/edit', Edit)], debug=True)