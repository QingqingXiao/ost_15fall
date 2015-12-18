import webapp2
import jinja2
import os
import model
import re

NUM_IN_A_PAGE = 20

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class View(webapp2.RequestHandler):
    def get(self):
        rid = self.request.get('rid')
        if rid == '':
            self.viewAllResources()
        else:
            self.viewReservations(rid)
    def viewAllResources(self):
        tag = self.request.get('tag')
        query = model.Resource.query().order(-model.Resource.modifyTime)
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
        
        # show = qs
        # temp = show[0].key.id()
        '''
        template_values = {'message': tag}
        template = JINJA_ENVIRONMENT.get_template('templates/message.html')
        self.response.write(template.render(template_values))
        '''
        template_values = {'next': next, 'page': page, 'resources': show, 'tag':tag}
        template = JINJA_ENVIRONMENT.get_template('templates/viewAllResources.html')
        self.response.write(template.render(template_values))
        
    def viewReservations(self, rid):
        rid = long(rid)
        rid = int(rid)
        resource = model.Resource.get_by_id(rid)
        #description = self.processContent(resource.description)
        #description = self.processContent()
        #print description
        description = resource.description
        print description
        # question = model.Question.get_by_id(6410839984701440)
        query = model.Reservation.query(model.Reservation.rid==rid).order(-model.Reservation.createTime)
        fetch = query.fetch()
        show = fetch
        reservationContent = []
        for res in show:
            #reservationContent.append(self.processContent(reservation.description))
            reservationContent.append(res.description)
        
        # print acontent
        template_values = {'resource': resource, 'revervations':show, 'description': description, 'reservationContent': reservationContent}
        template = JINJA_ENVIRONMENT.get_template('templates/viewReservations.html')
        self.response.write(template.render(template_values))
        '''
        template_values = {'message': qcontent}
        template = JINJA_ENVIRONMENT.get_template('templates/message.html')
        self.response.write(template.render(template_values))
        '''
    
    def processContent(self, content):
        # print content
        images = re.findall(r"(https?://[^\s]*\.jpg|https?://[^\s]*\.png|https?://[^\s]*\.gif)",content)
        for i in images:
            # print i
            replace = ' <img src="'+ i + '"/> '
            # print replace
            content = content.replace(i,replace)
        links = re.findall(r"https?://[^\s]*\.[^\s\"]*",content)
        for l in links:
            if l not in images:
                replace = ' <a href="'+ l + '">' + l + '</a> '
                # print l
                # print replace
                content = content.replace(l+' ' ,replace)
        return content
    
application = webapp2.WSGIApplication([
    ('/view', View)
], debug=True)