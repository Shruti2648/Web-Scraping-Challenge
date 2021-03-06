from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mongo"
mongo = PyMongo(app)

@app.route("/")
def index():
    marsmongo = mongo.db.mars_mongo.find_one()
    return render_template("index.html", mars_html=marsmongo)


@app.route("/scrape")
def scraper():
    mars_mongo = mongo.db.mars_mongo
    mars_data = mars_scrape.scrape()
    mars_mongo.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
