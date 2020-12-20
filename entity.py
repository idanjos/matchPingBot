import random
class Guild():
	def __init__(self):
		self.channels = ["matchmaking"]
		self.commands = ["!MatchPing"]
		self.messages = ['until you can match ping again!']
		self.roles = ["Match Ping"]
		self.delay = 15
		self.lastReq = 0
		self.debug = False

	def addChannel(self,channel):
		
		if channel in self.channels:
			return False
		self.channels += [channel]
		return True
		
	def delChannel(self, channel):
		if channel not in self.channels:
			return False
		try:
			self.channels.remove(channel)
		except Exception:
			print("Error in removing channel "+channel)
			return False
		
		return True
		pass
	def listChannel(self):
		#print channels
		pass
	def getMessage(self):
		return random.choice(self.messages)
	def addMessage(self,message):		
		if message in self.messages:
			return False
		self.messages += [message]
		return True	
		
	def delMessage(self,message):
		if message not in self.messages:
			return False
		try:
			self.messages.remove(message)
		except Exception:
			print("Error in removing message "+message)
			return False
		
		return True
	def listMessage(self):
		#print
		pass

	def addRole(self,role):		
		if role in self.roles:
			return False
		self.roles += [role]
		return True	
		
	def delRole(self,role):
		if role not in self.roles:
			return False
		try:
			self.roles.remove(role)
		except Exception:
			print("Error in removing message "+role)
			return False
		
		return True
	def listRole(self):
		#print
		pass

	def addCommand(self,command):
		if command in self.commands:
			return False
		self.commands += [command]
		return True
	def delCommand(self,command):
		if command not in self.commands:
			return False
		try:
			self.commands.remove(command)
		except Exception:
			print("Error in removing message "+command)
			return False
		return True

	def listCommand(self):
		pass

	def setDelay(self,delay):
		self.delay = delay
		return True
		
	def getDelay(self):
		return self.delay
	
	def setDebug(self,debug):
		self.debug = debug
	