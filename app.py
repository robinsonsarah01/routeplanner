from flask import Flask, render_template, request
from readgeodata import OsmDataReader
app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method == "GET":
        datareader = OsmDataReader("mhc.osm.xml")
        searchnodes = datareader.createSearchGraph()
        return render_template("home.html",graphnodes=searchnodes)
    else:
        return "POST requests not yet supported."
    
if __name__ == "__main__":
    app.debug = True
    app.run()