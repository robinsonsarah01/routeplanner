from readgeodata import OsmDataReader

class Node:

    def __init__(self, nodeelt, nodeid):
        self.elt = nodeelt # the original xml element
        self.id = nodeid
        self.lon = nodeelt.attrib["lon"]
        self.lat = nodeelt.attrib["lat"]
        self.inWays = []
        self.neighbors = [] # list of node objects
    
    def addToWay(self, way):
        if way not in self.inWays:
            self.inWays.append(way)
    
    def getContainingWays(self):
        return self.inWays
        
    def getId(self):
        return self.id
        
    def getLat(self):
        return self.lat
    
    def getLon(self):
        return self.lon
        
    def addNeighbor(self, other):
        if other not in self.neighbors:
            self.neighbors.append(other)
            other.addNeighbor(self)
    
    def getNeighbors(self):
        return self.neighbors


class Way:

    def __init__(self, wayelt, wayid):
        self.elt = wayelt # the original xml element
        self.id = wayid
        self.inRelations = []
        self.firstNode = None
        self.lastNode = None
        self.highwayType = wayelt.attrib["highway"]
        
    def getFirstNode(self):
        return self.firstNode
        
    def setFirstNode(self, first):
        self.firstNode = first
        
    def getLastNode(self):
        return self.lastNode
        
    def setLastNode(self, last):
        self.lastNode = last
        
    def getId(self):
        return self.id
    
    def getRoadType(self):
        return self.highwayType
        
    def addToRelation(self, relation):
        if relation not in self.inRelations:
            self.inRelations.append(relation)
        
    def getContainingRelations(self):
        return self.inRelations
    

class Relation:

    def __init__(self, relationelt, rid, rtype, routename = None):
        self.elt = relationelt # the original xml element
        self.type = rtype
        self.id = rid
        self.name = routename
        
    def getRouteName(self):
        """
         Depends on relation type. If it's a route, returns
         the name of the route. Otherwise, returns None. 
        """
        return self.name
        
    def getType(self):
        return self.type
        
    def getId(self):
        return self.id
    

# TESTING
if __name__ == "__main__":
    # mhcdata = OsmDataReader("mhc.osm.xml")
    pass
    