from google.appengine.api import users
from sets import Set
import os
import webapp2
import jinja2
import model
from datetime import datetime

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
            print resource
            resource.put()
            rid = resource.key.id()
            url = '/view?rid=' + repr(int(rid))
            self.redirect(url)

class createReservation(webapp2.RequestHandler):
    def get(self):
        rid = self.request.get('rid')
        # rid = 5988627519635456
        if rid == '':
            self.redirect('/view')
        else:
            rid = long(rid)
            rid = int(rid)
            resource = model.Resource.get_by_id(rid)
            query = model.Reservation.query(model.Reservation.rid==rid)
            currentReservations = query.fetch()
            template_values = {'resource': resource, 'currentReservations' : currentReservations}
            template = JINJA_ENVIRONMENT.get_template('templates/createReservation.html')
            self.response.write(template.render(template_values))
            
    def post(self):
        name = self.request.get('name')
        description = self.request.get('description')
        startTime = self.request.get('startTime')
        endTime = self.request.get('endTime')
        if startTime == '' or endTime == '':
            template_values = {'message': 'Start time or end time cannot be empty!'}
            template = JINJA_ENVIRONMENT.get_template('templates/message.html')
            self.response.write(template.render(template_values))
        else:
            rid = self.request.get('rid')
            rid = long(rid)
            rid = int(rid)
            query = model.Reservation.query(model.Reservation.rid==rid)
            currentReservations = query.fetch()
            for res in currentReservations:
                if startTime > res.startTime or endTime < res.endTime:
                    template_values = {'message': 'This timeslot is not available!'}
                    template = JINJA_ENVIRONMENT.get_template('templates/message.html')
                    self.response.write(template.render(template_values))

            resource = model.Resource.get_by_id(rid)
            resource.lastReserveTime = datetime.datetime.now().time()
            resource.put()
            reservation = model.Reservation()
            reservation.author = users.get_current_user()
            reservation.description = description
            reservation.nickname = name
            rid = long(rid)
            reservation.rid = int(rid)
            reservation.put()
            temp = repr(int(rid))
            url = '/view?rid=' + temp
            self.redirect(url)

application = webapp2.WSGIApplication([('/creater', createResource),
                                        ('/createreservation', createReservation)], 
                                        debug = True)

