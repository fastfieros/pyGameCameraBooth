
class event():
	type=None
	message=None


######################
#	 event classes  #
######################

class startover(event):
	type="startover"

class press(event):
	type = "press"


class downloading(event):
	type="downloading"

class photo(event):
	type = "photo"
	name = None

	def __init__(self, name=None):
		self.name=name

		
class preview(event):
	type="preview"
	image = None

	def __init__(self, image=None):
		self.image=image

class thumbnail(preview):
	type="thumbnail"
