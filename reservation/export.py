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

class Export(webapp2.RequestHandler):
    def get(self):
        rid = self.request.get('rid')
        rid = long(rid)
        rid = int(rid)

        resource = model.Resource.get_by_id(rid)
        query = model.Reservation.query(model.Reservation.rid==rid).order(-model.Reservation.createTime)
        fetch = query.fetch()
        show = []
        currentTime = datetime.now()
        for res in fetch:
            if res.startTime.hour > currentTime.hour:
                show.append(res)
        # resString = makeString(show)
        template_values = {'resource': resource, 'reservations': show}
        template = JINJA_ENVIRONMENT.get_template('templates/rss.xml')
        self.response.write(template.render(template_values))

def makeString(show):
    resString = '\n'
    for reservation in show:
        resString += '<item></item>'
        print resString
    return resString
    
application = webapp2.WSGIApplication([
    ('/export', Export)], debug=True)