from readgeodata import OsmDataReader

class Node:

	def __init__(self):
		self.tag = 'node'
		self.lat = 'get lat info'
		self.long = 'get long info'
		self.inWays = {}
		self.neighbors ={}


class Ways:

	def __init__(self):
		self.tag = 'ways'
		self.type = 'get type i.e. highway'
		self.inRelations = {}

class Relation:

	def __init__(self):
		self.tag = 'relation'

# TESTING
if __name__ == "__main__":
	mhcdata = OsmDataReader("mhc.osm.xml")
	mhcdata.getRoot = Node()
	print('long',mhcdata.getRoot.long)