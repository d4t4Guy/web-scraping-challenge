from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#conn string
mongo_conn= 'mongodb://localhost:27017'
client = pymongo.MongoClient(mongo_conn)

#set collection variable
mars = client.mars_app.mars

@app.route("/")
def index():
    if mars.count_documents({})==0: 
        return render_template("index0.html")  #note: I tried to put the if logic in Jinja2 but after 80 minutes of trial and error I gave up and did this instead
    else:
        scrape_dict = mars.find_one()
        return render_template("index.html", scrape_dict=scrape_dict)


@app.route("/scrape")
def scraper():
    scrape_dict = scrape_mars.scrape()   ####replace when test done
    mars.drop()
    mars.insert_one(scrape_dict)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)