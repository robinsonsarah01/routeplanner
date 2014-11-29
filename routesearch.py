from readgeodata import OsmDataReader
import xml.etree.ElementTree as ET
import util
import copy

currRoute = [] # keeps track of total distance
routes = {} # stop adding to routes when all nodes expanded
fringe = util.PriorityQueue() # use priority queue for fringe
maxDistance = 0

def isGoalState(self):
 	""" stop searching for routes when all the nodes expanded"""
 	if allNodesSearched or routeComplete:
 		return True
 	else:
 		return False

def allNodesSearched(self):
	""" stop expanding nodes for a route if all nodes have been searched"""
	return fringe.isEmpty()

def routeComplete(self):
	""" stop expanding nodes for a route when the distance constraint is reached"""
	if sum(currRoute) >= maxDistance:
		# maybe we can refine this to be a softer constraint on distance
		return True
	else:
		return False

def startSearch(constraint):
	"""initialize search"""
	maxDistance = constraint
	mhcdata = OsmDataReader("mhc.osm.xml")
	mhcdata.createSearchGraph()
	tree = mhcdata.tree
	#treeString = ET.tostring(tree, "us-ascii", "text")

	# TODO: make start another parameter for startSearch
	start = tree.getroot() # for now, initialize start = root
	aStarSearch(start, tree)

def aStarSearch(start, tree):
	"""Search the node that has the lowest combined cost and heuristic first."""
	visitedNodes = set() # keep track of visited nodes

	gCost = 0 # cost of the best path
	hEst = 0 # heuristic's estimate
	fCost = 0 # gCost + hEst
	
	totalDistance = 0 # keep track of accrued cost a.k.a. distance
	finalPath = [] # the path is just a list of nodes explored in order

	# get the start state
	currLat = start.getLat()
	currLong = start.getLon()

	# initialize search by pushing start node to front of priority queue
	fringe.push((start, [start], totalDistance), 1)
	visitedNodes.add(start)

	while isGoalState is False:
		# get the coordinates, path leading up to, and total cost of path FOR step of highest priority
		(node, path, distance) = fringe.pop()
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

			# if we haven't explored the node
			else:
				# update the path
				tempPath.append(nextNode)
				# determine cumulative distance of traveling to this node
				addDistance = manhattanDistance(node, nextNode)
				gCost = distance + addDistance
				# the heuristic estimates curvature
				hEst = curvatureHeuristic(node, nextNode)
				# fCost 
				fCost = gCost + hEst

				# push a new tuple onto the fringe, using fCost as an indicator of priority
				pushThis = (nextNode, copy.copy(tempPath), addDistance)
				fringe.push(pushThis, fCost)

				tempPath = [] # clear tempPath

	return None

def curvatureHeuristic(currPos, nextPos):
	""" for now, the heuristic measures curvature via
	the deviation of distance between two nodes FROM the expected distance between two nodes connected by straight line """
	return 0

def distanceBetween(currPos, nextPos):
	""" gets the real distance between two nodes"""
	util.raiseNotDefined()

def manhattanDistance(currPos, nextPos):
	""" takes in 2 lat/long coordinates and returns distance between them """
	xy1 = currPos
	xy2 = nextPos
	distance = abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
	print "distance between", currPos, " and ", nextPos, " = ", distance


# TESTING
if __name__ == "__main__":
	print ""
	print ""
	startSearch(20)
