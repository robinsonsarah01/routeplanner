import xml.etree.ElementTree as ET
from treeelements import *


class OsmDataReader:
    """
     Reads data from a file in OSM XML format.
     
     See http://wiki.openstreetmap.org/wiki/OSM_XML .
    """
    
    def __init__(self, filename):
        """
         The constructor takes one argument: the filename to read data from.
         It instantiates the instance variables of the class.
        """
        self.tree = ET.parse(filename)
        self.nodes = {} # all the xml node elements
        self.graphnodes = {} # The nodes objs that relate to roads and that therefore we care about
        self.ways = {}
        self.roads = {} # All ways with a 'highway' tag
        self.wayObjs = {} # the object wrappers around the ways
        self.relations = {}
        self.relationObjs = {} # the object wrappers around the relations
    
    def sortElements(self):
        root = self.tree.getroot()
        for child in root:
            id = ""
            if child.tag != "bounds":
                id = child.get("id")
            if child.tag == "node":
                self.nodes[id] = child
            elif child.tag == "way":
                self.ways[id] = child
            elif child.tag == "relation":
                self.relations[id] = child
                
    def getRoads(self, footways = False):
        """
         Get all the ways that are roads (some are other things).
         If True is passed as a parameter, footways (pedestrian paths) are included.
         This is by default false.
        """
        for id in self.ways:
            way = self.ways[id]
            tag_elements = way.findall("tag")
            for tag_elt in tag_elements:
                if tag_elt.attrib["k"] == "highway":
                    if footways or (tag_elt.attrib["v"] != "footway" and tag_elt.attrib["v"] != "steps"):
                        self.roads[id] = way
                        way.set("highway",tag_elt.attrib["v"])
            
    def buildNodesAndWays(self):
        counter = 0
        for id in self.roads:
            # if counter > 25:
                # break
            # counter += 1
            
            road = self.roads[id] # the way/road we're currently looking at
            currWay = Way(road, id)
            self.wayObjs[id] = currWay
            
            prevNodeObj = None # the previously created node object
            relatednodes = road.findall("nd")
            for nd in relatednodes: # for each of the nodes in the way, create a node object in the search graph
                ndid = nd.attrib["ref"]
                if ndid in self.nodes: # the node is most likely there, but to be safe we check for existence
                    # "nodes defining the geometry of the way are enumerated in the correct order"
                    # Do the graph-building stuff
                    currNode = None
                    if ndid in self.graphnodes: # node already exists
                        currNode = self.graphnodes[ndid]
                        # TESTING
                        # print "already in graph", [ x.getRoadType() for x in currNode.getContainingWays() ]
                        # print currNode.getNeighbors()
                    else: # node hasn't been instantiated yet, so create it
                        nodeelt = self.nodes[ndid]
                        self.graphnodes[ndid] = Node(nodeelt, ndid)
                        currNode = self.graphnodes[ndid]                    
                    if prevNodeObj: # add the previous node as a neighbor
                        currNode.addNeighbor(prevNodeObj)
                    else: # this is the first node in the list
                        currWay.setFirstNode(currNode)
                    currNode.addToWay(currWay) # reference its containing way element
                    prevNodeObj = currNode # we're done, so curr becomes prev
            
            # prevNodeObj is now the last node
            currWay.setLastNode(prevNodeObj)
        
        
    def applyRelations(self):
        """
         Processes relations.
         Groups together ways as a road. See http://wiki.openstreetmap.org/wiki/Relation:route
        
         Not dealt w/ because of limited data set:
         Apply turn bans (remove connections b/w graph nodes),
         etc. See http://wiki.openstreetmap.org/wiki/Relation:restriction          
         Should possibly take params to determine what type of vehicle is being used.
        """
        for id in self.relations:
            relation = self.relations[id]
            type = ""
            name = None
            tag_elements = relation.findall("tag")
            for tag_elt in tag_elements:
                if tag_elt.attrib["k"] == "ref":
                    name = tag_elt.attrib["v"]
                # elif tag_elt.attrib["k"] == "route": # don't really need this
                    # print "route", tag_elt.attrib["v"]
                elif tag_elt.attrib["k"] == "type":
                    type = tag_elt.attrib["v"]
            if type != "route" and type != "restriction": # ignore things that aren't routes or restrictions
                continue
            self.relationObjs[id] = Relation(relation, id, type, name) # Create the relation object
            currRelation = self.relationObjs[id]
            
            member_elts = relation.findall("member") # get all the ways/nodes in the relation
            for m_elt in member_elts:
                if m_elt.attrib["type"] != "way": # For now, ignore all members that aren't ways
                    continue
                mid = m_elt.attrib["ref"]
                if mid in self.wayObjs: # some/most ways in the relation are not within our data's scope
                    way = self.wayObjs[mid]
                    way.addToRelation(currRelation)
                    # unfortunately it seems that the ways aren't enumerated in order in the relation
                    # so we can't connect the first node and the last node in neighbouring ways
            
    def createSearchGraph(self, pedestrian = False):
        mhcdata.sortElements()
        mhcdata.getRoads(pedestrian)
        mhcdata.buildNodesAndWays()
        mhcdata.applyRelations()
        
        return self.graphnodes
        

# TESTING
if __name__ == "__main__":
    mhcdata = OsmDataReader("mhc.osm.xml")
    mhcdata.createSearchGraph()
    