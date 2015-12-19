from google.appengine.api import users
from sets import Set
import webapp2
import jinja2
import os
import model
import re


NUM_IN_A_PAGE = 10

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class ViewYourResource(webapp2.RequestHandler):
    def get(self):
        currentUser = users.get_current_user()
        query = model.Resource.query(model.Resource.owner==currentUser).order(-model.Resource.createTime)
        fetch = query.fetch()
        tag = self.request.get('tag')
        rs = []
        if tag != '':
            for r in fetch:
                if tag in r.tags:
                    rs.append(r)
        else:
            rs = fetch
        page = self.request.get('page')
        if page == '':
            page = 1
        else:
            page = int(page)
        
        print rs
        num = len(rs)
        max = int(page) * NUM_IN_A_PAGE
        if max >= num:
            next = -1
            show = rs[(max-10):num]
        else:
            next = int(page) + 1
            show = rs[(max-10):max]

        template_values = {'next': next, 'page': page, 'resources': show, 'tag':tag}
        template = JINJA_ENVIRONMENT.get_template('templates/viewYourResource.html')
        self.response.write(template.render(template_values))


class ViewYourReservations(webapp2.RequestHandler):
     def get(self):
        currentUser = users.get_current_user()
        query = model.Reservation.query(model.Reservation.author==currentUser).order(model.Reservation.startTime)
        fetch = query.fetch()
        show = fetch

        if len(show) == 0:
            template_values = {'message' : 'You have no available reservation!'}
            template = JINJA_ENVIRONMENT.get_template('templates/message.html')
            self.response.write(template.render(template_values))
        else:
            reservationContent = []
            for res in show:
                reservationContent.append(res.description)
            
            # print acontent
            template_values = {'revervations':show}
            template = JINJA_ENVIRONMENT.get_template('templates/ViewYourReservations.html')
            self.response.write(template.render(template_values))

    
application = webapp2.WSGIApplication([
    ('/viewyourresource', ViewYourResource),
    ('/viewyourreservations', ViewYourReservations)], debug=True)
