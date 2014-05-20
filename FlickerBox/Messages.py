import json
import uuid
from datetime import datetime

class Message(object):
	""" Message handled by the Box could be inbound or outbound messages.	
	{"id":"219129-303","sender":"yesSender","to":"yesTo","content":"This is a test"}
	"""
	
	def __init__(self, fromJsonString = "notSet"):	
		if(fromJsonString == "notSet") :		
			self.id = uuid.uuid4()
			self.sender = "senderFieldNotSet"
			self.to = "toFieldNotSet"
			self.content = "contentNotSet"
			self.creationTime = datetime.utcnow()
		else :
			data = json.loads(fromJsonString)
			self.id = self.__get__(data, "id","idNotSet")			
			self.sender = self.__get__(data, "sender","senderNotSet")
			self.to = self.__get__(data, "to","")	
			self.content = self.__get__(data, "content","No content")	
			self.creationTime = self.__get__(data, "creationTime","")	

	def __get__(self, dict, key, defaultValue):
		if(key in dict) :
			result = dict[key]
		else :
			result = defaultValue
		return result
			
	
	def setNewId(self):
		self.id = uuid.uuid4()
		
	def setCreationTime(self):
		self.creationTime = datetime.utcnow()	
		
	def getJson(self):
		result = "{{\"id\":\"{0}\", \"sender\":\"{1}\", \"to\":\"{2}\", \"creationtime\":\"{3}\", \"content\":\"{4}\"}}".format(self.id,self.sender,self.to,self.creationTime,self.content)
		return result	
	
	def __str__(self):
		result = "id={0}, sender={1}, to={2}, creationtime={3}, content={4}".format(self.id,self.sender,self.to,self.creationTime,self.content)
		return result

if __name__ == "__main__":
	msg = Message()
	print msg
	msg = Message('{"sender":"yesSender","to":"yesTo","content":"This is a test","creationTime":"'+str(datetime.utcnow())+'"}')
	print msg