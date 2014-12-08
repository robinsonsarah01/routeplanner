from treeelements import *
import math
# below only used in testing, remove later
from readgeodata import *
import routesearch

def generateDirections(nodelist):
    """
     Generate human-readable directions given a list, in order, of Nodes.
    """
    directions = "Start on"
    prevRoad = None
    prevNode = nodelist[0]
    prevWays = prevNode.getContainingWays()
    prevHeading = None
    newRoad = False
    for i in range(1,len(nodelist)):
        # init current values
        currNode = nodelist[i]
        currWays = currNode.getContainingWays()
        currRoad = [ x for x in currWays if x in prevWays ] # get the road/way we're currently on
        currHeading = getBearing(prevNode,currNode)
        
        # check if we've changed roads
        if len(currRoad) == 0: # if the road has changed w/o an intersection, make sure currRoad is not null
            currRoad = [ x for x in currWays ]
            newRoad = True
            print "currRoad is empty"
        elif prevRoad and len(currRoad) != len(prevRoad):
            newRoad = True
            print "added a road"
        elif prevRoad:
            for road in currRoad:
                if road not in prevRoad:
                    newRoad = True
                    print "road changed"
                    
        print newRoad
            
        list.sort(currRoad) # make sure the roads are always in the same order
        
        if not prevRoad: # if this is the first node pair we have a special case
            prevRoad = currRoad
            # also, since we just started, generate the first sentence in the directions here
            roadname = getRoadNames(currRoad)
            if not roadname:
                roadname = " the road with no name."
            directions += " " + roadname + "."
        
        elif newRoad: # else check if we have changed roads between iterations
            # generate more directions and keep going
            dir, prep = generateNextDirection(prevHeading, currHeading)
            roadname = getRoadNames(currRoad)
            if roadname:
                directions += " " + dir + " " + prep + " " + roadname + "."
            else:
                directions += " " + dir + "."
            
        # increment for next iteration of loop
        prevHeading = currHeading
        prevRoad = currRoad
        prevWays = currWays
        prevNode = currNode
        newRoad = False
        
    directions += " Your route ends here."
    return directions
    
def generateNextDirection(curr,next):
    """
     Given two bearings (in degrees), returns 'turn left onto', 
     'turn right onto', or 'go straight on to'
     for use between two road names.
     
     Ideally the below would work; it needs more debugging.
     
     Left: 90 > next - curr > 0
     Right: next - curr < 0 OR next - curr > 180 > 0
     Straght: abs(next - curr) < 15 or next - curr > 345
    """
    diff = next - curr
    print diff
    if abs(diff) < 15 or diff > 345:
        return "Go straight","on to"
    if 90 > diff and diff > 0:
        return "Turn left","onto"
    # all other cases are right
    # (the above may not be true; check later.)
    return "Turn right","onto"
    # return "Turn", "onto"
    
    
def getRoadNames(currRoad):
    """
     Given a list of ways (1-many), return a name or names 
     separated by "/" for use in directions. 
     Uses the ways first, then checks the relations.
    """
    # print [ kid.attrib for kid in x.elt for x in currRoad ]
    
    # check the ways and get name(s) from them
    waynames = [ x.getRoadName() for x in currRoad ] # try to get a name from the ways first
    roadname = ""
    for n in waynames:
        if n:
            roadname += n + "/"
    
    # then check the relations, if there are any, for names
    relations = [ r.getRouteName() for r in x.getContainingRelations() for x in currRoad ]
    for n in relations:
        if n:
            roadname += n + "/"
    
    if len(roadname) > 0 and roadname[-1] == "/":
        roadname = roadname[:-1]
        
    return roadname
    
    
def getBearing(start,end):
    """
     Given two nodes with lat/long coordinates, return a bearing in degrees.
     Adapted from http://mathforum.org/library/drmath/view/55417.html
    """
    lat1,lon1 = start.getLat(), start.getLon()
    lat2,lon2 = end.getLat(), end.getLon()
    rlat1 = math.radians(float(lat1)) # convert from (str)degrees to radians
    rlat2 = math.radians(float(lat2))
    rlon1 = math.radians(float(lon1))
    rlon2 = math.radians(float(lon2))
    # get the angle east of north from start to end
    bearing = math.fmod(
                    math.atan2( math.sin(rlon2-rlon1)*math.cos(rlat2) 
                                , math.cos(rlat1)*math.sin(rlat2) - math.sin(rlat1)*math.cos(rlat2)*math.cos(rlon2-rlon1) )
                    , 2*math.pi )
    bearing = math.degrees(bearing)
    if bearing < 0:
        bearing = 360 + bearing # go between [0,360] instead of [-180,180]
    return bearing
    
    
if __name__ == "__main__":
    # create test list
    #testids = ["72088866","1354509391","2133302537","72053830","1353506942","2133302496","72062153","72075396","72084662","72014487","71987051","72066712"] # these aren't actually all neighbours
    testids = routesearch.startSearch(20)
    mhcdata = OsmDataReader("mhc.osm.xml")
    searchnodes = mhcdata.createSearchGraph()
    testlist = [ searchnodes[id] for id in testids ]
    dir = generateDirections(testlist)
    print dir