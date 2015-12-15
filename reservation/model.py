from google.appengine.ext import ndb
from google.appengine.ext import blobstore

DEFAULT_PROJECT_NAME = 'default_project'

def getProjectKey(projectName = DEFAULT_PROJECT_NAME):
	return ndb.Key('Project', projectName)

class Resource(ndb.Model):
	owner = ndb.UserProperty()
	name = ndb.StringProperty()
	tags = ndb.JsonProperty()
	description = ndb.StringProperty()
	createTime = ndb.DateTimeProperty(auto_now_add=True)
	modifyTime = ndb.DateTimeProperty(auto_now=True)


class Reservation(ndb.Model):
	author = ndb.UserProperty()
	startTime = ndb.DateTimeProperty()
	endTime = ndb.DateTimeProperty()
	description = ndb.StringProperty()
	createTime = ndb.DateTimeProperty(auto_now_add=True)