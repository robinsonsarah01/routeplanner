from flask import Flask, render_template, request
from readgeodata import OsmDataReader
app = Flask(__name__)

print "starting data reader"
#datareader = OsmDataReader("southhadley.osm.xml")
datareader = OsmDataReader("mhc.osm.xml")
print "started data reader, initing graph"
searchnodes = datareader.createSearchGraph()
print "inited graph"

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html",graphnodes=searchnodes)
    else:
        return "POST requests not yet supported. This will eventually be a search result."
    
if __name__ == "__main__":
    app.debug = True
    app.run()