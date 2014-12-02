import util
import copy

from readgeodata import OsmDataReader

totalDistance = 0 # keep track of accrued cost a.k.a. distance
routes = {} # stop adding to routes when all nodes expanded
fringe = util.PriorityQueue() # curviest routes are given highest priority
maxDistance = 0

def isGoalState():
    """ stop searching for routes when all the nodes expanded or route length is complete"""
    if allNodesSearched() or routeComplete():
        return True
    else:
        return False

def allNodesSearched():
    """ stop expanding nodes for a route if all nodes have been searched"""
    return fringe.isEmpty()

def routeComplete():
    """ stop expanding nodes for a route when the distance constraint is reached"""
    print "maxDistance", maxDistance
    if totalDistance >= maxDistance:
        # maybe we can refine this to be a softer constraint on distance
        return True
    else:
        return False

def startSearch(constraint):
    """initialize search"""
    # global maxDistance
    # maxDistance = constraint
    # mhcdata = OsmDataReader("mhc.osm.xml")
    # graph = mhcdata.createSearchGraph()
    # treeString = ET.tostring(tree, "us-ascii", "text")
    # printDict(graph)

    # TODO: make start another parameter for startSearch
    # start = graph['72028025'] # for now, initialize start = root
    # return aStarSearch(start, graph)
    return searchFromPoint('72028025',constraint)
    
def searchFromPoint(startid, constraint):
    """ init search from a specific point """
    global maxDistance
    maxDistance = constraint
    mhcdata = OsmDataReader("mhc.osm.xml")
    graph = mhcdata.createSearchGraph()
    
    start = graph[startid]
    return aStarSearch(start, graph)

def aStarSearch(start, tree):
    """Search the node that has the lowest combined cost and heuristic first."""
    global totalDistance
    
    visitedNodes = set() # keep track of visited nodes

    gCost = 0 # cost of the best path
    hEst = 0 # heuristic's estimate
    fCost = 0 # gCost + hEst
    
    finalPath = [] # the path is just a list of nodes explored in order

    # get the start state
    currLat = start.getLat()
    currLon = start.getLon()

    # initialize search by pushing start node to front of priority queue
    fringe.push((start, [start]), 1)

    while not isGoalState():
        # get the coordinates, path leading up to, and total cost of path FOR step of highest priority
        node, path = fringe.pop()
        visitedNodes.add(node) # add to visited

        # do we need a check here?

        # get next possible nodes
        nextNodes = node.getNeighbors()

        for nextNode in nextNodes:
            # copy current path
            tempPath = copy.copy(path)

            # if this node was already explored, clear the temp path and move on to the next
            if nextNode in visitedNodes:
                tempPath = []
            else:
                tempPath.append(nextNode) # update the path

                # nodes from the osm xml were added in points where the road curved,
                # so getting manhattan distance between nodes does give good approximation of actual distance between nodes
                totalDistance += manhattanDistance(node, nextNode) # cumulative distance to this node
                print "totalDistance", totalDistance
                gCost = 1

                hEst = curvatureHeuristic(start, nextNode)
                fCost = gCost - hEst
                print "fCost", fCost

                # push a new tuple onto the fringe, using fCost as an indicator of priority
                finalPath = copy.copy(tempPath)
                pushThis = (nextNode, finalPath)
                fringe.push(pushThis, fCost)

                tempPath = [] # clear tempPath
    # print ""
    # print "finalPath:"
    # for node in finalPath:
    # 	print node.getId()
    
    return finalPath

def curvatureHeuristic(start, node):
    """ for now, the heuristic measures curvature via
    the deviation of distance between this node and the start node 
    FROM an expected distance if the route between this node and the start was straight"""

    # if it's a straight path from start to here, how long should the path be?
    expected = manhattanDistance(start, node)
    # what's the actual total distance?
    actual = totalDistance

    # the greater the deviation, the curvier this road is
    curviness = actual - expected

    return curviness

def manhattanDistance(currPos, nextPos):
    """ takes in 2 lat/long coordinates and returns distance between them """
    xy1 = currPos
    xy2 = nextPos
    distance = abs(float(xy1.getLat()) - float(xy2.getLat())) + abs(float(xy1.getLon()) - float(xy2.getLon()))
    return distance


# TESTING
if __name__ == "__main__":
    print ""
    print ""
    startSearch(0.3)