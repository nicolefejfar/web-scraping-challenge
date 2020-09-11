from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of the Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create index route that will query the Mongo database
@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template('index.html', mars_data=mars_data)

# Route to render index.html template using data from Mongo
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    mars_data.update({}, mars_info, upsert=True)
    # return 'Scraping Successful!'
    return redirect('/', code=302)

# Required flask app code
if __name__ == "__main__":
    app.run(debug=True)
