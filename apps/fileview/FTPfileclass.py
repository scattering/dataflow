
class FTPfile():
	def __init__(self, id_num=None, path=None, children=None, leaf=None):
		self.id = id_num #integer
		self.path = path #string
		self.children = children # list of FTPfiles
		self.leaf = leaf #boolean
		
	def setChildren(self, children):
		self.children=children
	def isLeaf(self):
		self.leaf=True
	def __str__(self):
		return str(self.path)
