import util
import copy

from readgeodata import OsmDataReader
import xml.etree.ElementTree as ET

totalDistance = 0 # keep track of accrued cost a.k.a. distance
routes = {} # stop adding to routes when all nodes expanded
fringe = util.PriorityQueue() # curviest routes are given highest priority
maxDistance = 0

def isGoalState(self):
 	""" stop searching for routes when all the nodes expanded or route length is complete"""
 	if allNodesSearched or routeComplete:
 		return True
 	else:
 		return False

def allNodesSearched(self):
	""" stop expanding nodes for a route if all nodes have been searched"""
	return fringe.isEmpty()

def routeComplete(self):
	""" stop expanding nodes for a route when the distance constraint is reached"""
	if totalDistance >= maxDistance:
		# maybe we can refine this to be a softer constraint on distance
		return True
	else:
		return False

def startSearch(constraint):
	"""initialize search"""
	maxDistance = constraint
	mhcdata = OsmDataReader("mhc.osm.xml")
	graph = mhcdata.createSearchGraph()
	#treeString = ET.tostring(tree, "us-ascii", "text")
	#printDict(graph)

	# TODO: make start another parameter for startSearch
	start = graph['72028025'] # for now, initialize start = root
	print "start", start
	aStarSearch(start, graph)

def printDict(something):
	print "graph[0]"
	for key in something:
		print "key: ", key, " value: ", something[key]

def aStarSearch(start, tree):
	"""Search the node that has the lowest combined cost and heuristic first."""
	visitedNodes = set() # keep track of visited nodes

	gCost = 0 # cost of the best path
	hEst = 0 # heuristic's estimate
	fCost = 0 # gCost + hEst
	
	finalPath = [] # the path is just a list of nodes explored in order

	# get the start state
	currLat = start.getLat()
	currLon = start.getLon()
	print "currLat:", currLat, " currLon:", currLon

	# initialize search by pushing start node to front of priority queue
	fringe.push((start, [start]), 1)

	while isGoalState is False:
		# get the coordinates, path leading up to, and total cost of path FOR step of highest priority
		(node, path) = fringe.pop()
		visitedNodes.add(node) # add to visited

		# do we need a check here?

		# get next possible nodes
		nextNodes = node.getNeighbors()

		for nextNode in nextNodes:
			print "nextNode ", nextNode.getID
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
				gCost = totalDistance

				hEst = curvatureHeuristic(start, nextNode)
				# fCost maybe incorporating total distance in here does not make sense.
				fCost = gCost - hEst

				# push a new tuple onto the fringe, using fCost as an indicator of priority
				pushThis = (nextNode, copy.copy(tempPath), addDistance)
				fringe.push(pushThis, fCost)

				tempPath = [] # clear tempPath

	return None

def curvatureHeuristic(node):
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
	distance = abs(xy1.getLat - xy2.getLat) + abs(xy1.getLon - xy2.getLon)
	print "distance between", currPos, " and ", nextPos, " = ", distance


# TESTING
if __name__ == "__main__":
	print ""
	print ""
	startSearch(20)