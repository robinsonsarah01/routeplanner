import xml.etree.ElementTree as ET
import operator


class OsmDataReader:
    """
     Reads data from a file in OSM XML format.
     
     See http://wiki.openstreetmap.org/wiki/OSM_XML .
    """
    
    def __init__(self, filename):
        """
         The constructor takes one argument: the filename to read data from.
         It instantiates the instance variables of the 
        """
        self.tree = ET.parse(filename)
        self.nodes = {}
        self.ways = {}
        self.relations = {}
        self.roads = {} # All ways with a 'highway' tag
        self.graphnodes = {} # The nodes that relate to roads/ways and therefore we care about
    
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
                
    def getRoads(self):
        for id in self.ways:
            way = self.ways[id]
            tag_elements = way.findall("tag")
            for tag_elt in tag_elements:
                if tag_elt.attrib["k"] == "highway":
                    self.roads[id] = way
                    way.set("highway",tag_elt.attrib["v"])
            
    def buildSearchGraph(self):
        counter = 0
        for id in self.roads:
            if counter > 5:
                break
            counter += 1
            
            road = self.roads[id]
            # print id, road.attrib["highway"]
            relatednodes = road.findall("nd")
            for nd in relatednodes:
                ndid = nd.attrib["ref"]
                if ndid in self.nodes: # the node is most likely there, but to be safe
                    # "nodes defining the geometry of the way are enumerated in the correct order"
                    print self.nodes[ndid].attrib["lat"],self.nodes[ndid].attrib["lon"]
                    #pass
                    # TODO create a graph node class and create the nodes here
                    # if it exists, just add its connections & relate it to the way
                    # else, create it and link it back to its way
        
        
    def applyRelations(self):
        """
         Apply turn bans (remove connections b/w graph nodes),
         apply restrictions (remove roads restricted to bikes),
         etc. See http://wiki.openstreetmap.org/wiki/Relation:restriction 
         
         Also group together ways as a road. See http://wiki.openstreetmap.org/wiki/Relation:route
         
         Should take params to determine what type of vehicle is being used.
        """
        counter = 0
        for id in self.relations:
            if counter > 5:
                break
            counter += 1
            for child in self.relations[id]:
                print child.tag, child.attrib
            print "\n"
        

# TESTING
if __name__ == "__main__":
    mhcdata = OsmDataReader("mhc.osm.xml")
    mhcdata.sortElements()
    mhcdata.getRoads()
    mhcdata.buildSearchGraph()
    mhcdata.applyRelations()