import webapp2
import jinja2
import os
import model
import re
from datetime import datetime

NUM_IN_A_PAGE = 10

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class View(webapp2.RequestHandler):
    def get(self):
        rid = self.request.get('rid')
        if rid != '':
            self.viewReservations(rid)
        else:
            self.viewAllResources()

    def viewAllResources(self):
        tag = self.request.get('tag')
        query = model.Resource.query().order(-model.Resource.createTime)
        fetch = query.fetch()
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
        
        num = len(rs)
        max = int(page) * NUM_IN_A_PAGE
        if max >= num:
            next = -1
            show = rs[(max-10):num]
        else:
            next = int(page) + 1
            show = rs[(max-10):max]
        
        template_values = {'next': next, 'page': page, 'resources': show, 'tag':tag}
        template = JINJA_ENVIRONMENT.get_template('templates/viewAllResources.html')
        self.response.write(template.render(template_values))
        
    def viewReservations(self, rid):
        rid = long(rid)
        rid = int(rid)

        resource = model.Resource.get_by_id(rid)
        query = model.Reservation.query(model.Reservation.rid==rid).order(-model.Reservation.createTime)
        fetch = query.fetch()
        # show = fetch
        # reservationContent = []
        # for res in show:
        #     reservationContent.append(res.description)
        
        # template_values = {'resource': resource, 'revervations':show, 'description': description, 'reservationContent': reservationContent}
        show = []
        currentTime = datetime.now()
        for res in fetch:
            if res.startTime.hour > currentTime.hour:
                show.append(res)
        
        
        template_values = {'resource': resource, 'revervations': show}
        template = JINJA_ENVIRONMENT.get_template('templates/viewReservations.html')
        self.response.write(template.render(template_values))

    
application = webapp2.WSGIApplication([
    ('/view', View)], debug=True)