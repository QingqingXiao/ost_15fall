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

class Delete(webapp2.RequestHandler):
    def get(self):
        rid = self.request.get('rid')
        resid = self.request.get('resid')
        if rid == '' and resid == '':
            template_values = {'message': 'No reservation id or rource id specified'}
            template = JINJA_ENVIRONMENT.get_template('templates/message.html')
            self.response.write(template.render(template_values))
        elif rid != '':
            rid = long(rid)
            rid = int(rid)
            user = users.get_current_user()
            resource = model.Resource.get_by_id(rid)
            if resource.owner != user:
                template_values = {'message': 'You don\'t have the permission to delete this resource' }
                template = JINJA_ENVIRONMENT.get_template('templates/message.html')
                self.response.write(template.render(template_values))
            else:
                resource.key.delete()
                query = model.Reservation.query(model.Reservation.rid==resource.key.id())
                fetch = query.fetch()
                for reservation in fetch:
                    reservation.key.delete()
                self.redirect('/view')
        elif resid != '':
            resid = long(resid)
            resid = int(resid)
            user = users.get_current_user()
            reservation = model.Reservation.get_by_id(resid)
            rid = reservation.rid
            if reservation.author != user:
                template_values = {'message': 'You don\'t have the permission to delete this reservation' }
                template = JINJA_ENVIRONMENT.get_template('templates/message.html')
                self.response.write(template.render(template_values))
            else:
                reservation.key.delete()
                temp = repr(int(rid))
                self.redirect('/view?rid=' + temp)



application = webapp2.WSGIApplication([
    ('/delete', Delete),
], debug=True)