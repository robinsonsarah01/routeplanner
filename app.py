from flask import Flask, render_template, request
from readgeodata import OsmDataReader
import routesearch
import makedirections
app = Flask(__name__)

# Init graph here so we only do it once, for efficiency
print "starting data reader"
#datareader = OsmDataReader("southhadley.osm.xml")
datareader = OsmDataReader("mhc.osm.xml")
print "started data reader, initing graph"
searchnodes = datareader.createSearchGraph()
print "inited graph"

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html",graphnodes=searchnodes,searchresult=False,directions="")
    elif request.method == "POST":
        startid = request.form["node-id"]
        if not startid or startid not in searchnodes:
            return "Search not started; id '%s' not a valid node id." % startid
        curvature = request.form["curvature"]
        distanceconstraint = request.form["distance"]
        # for now, we ignore curvature preference
        reslist = routesearch.searchFromPoint(startid,int(distanceconstraint))
        # get directions
        dirstring = makedirections.generateDirections(reslist)
        # translate result infor the form expected by the template, ie a dict keyed by id
        searchresultnodes = {}
        for n in reslist:
            searchresultnodes[n.getId()] = n
        # return "Search started with id %s, aiming to %s curvature of route. Max distance is %s." % (startid, curvature, distanceconstraint)
        return render_template("home.html",graphnodes=searchresultnodes,searchresult=True,directions=dirstring)
    
if __name__ == "__main__":
    app.debug = True
    app.run()