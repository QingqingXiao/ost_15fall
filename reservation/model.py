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
	# availableStartTime = ndb.DateTimeProperty()
	# availableEndTime = ndb.DateTimeProperty()
	# createTime = ndb.DateTimeProperty(auto_now_add=True)
	# modifyTime = ndb.DateTimeProperty(auto_now=True)
	# lastReserveTime = ndb.DateTimeProperty()
	availableStartTime = ndb.TimeProperty()
	availableEndTime = ndb.TimeProperty()
	createTime = ndb.TimeProperty(auto_now_add=True)
	lastReserveTime = ndb.TimeProperty()


class Reservation(ndb.Model):
	author = ndb.UserProperty()
	nickname = ndb.StringProperty()
	# startTime = ndb.DateTimeProperty()
	# endTime = ndb.DateTimeProperty()
	startTime = ndb.TimeProperty()
	endTime = ndb.TimeProperty()
	description = ndb.StringProperty()
	rid = ndb.IntegerProperty()
	#createTime = ndb.DateTimeProperty(auto_now_add=True)
	createTime = ndb.TimeProperty(auto_now_add=True)