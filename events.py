
class event():
	type=None
	message=None


######################
#	 event classes  #
######################

class startover(event):
	type="startover"
		
class preview(event):
	type="preview"

class photo(event):
	type = "photo"
	name = None

	def __init__(self, name=None):
		self.name=name


class downloading(event):
	type="downloading"
	progress=0

	def __init__(self, progress=0):
		self.progress=progress

class press(event):
	type = "press"

