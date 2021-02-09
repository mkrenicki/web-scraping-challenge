from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Set up pymongo connection and link db
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mission_to_mars_2
listings = db.listings

@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)

@app.route("/scrape")
def scrape():
    listings = mongo.db.listings
    listings= scrape_mars.scrape()
    listings.update({}, listings, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)