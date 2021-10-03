# Set up and dependencies.
import datetime as dt 
import numpy as np 
import pandas as pd 
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import news_scrape
from login_info import *

# Create Flask
app = Flask(__name__)


# Connect to the Mongo database.
mongo = PyMongo(app, uri="mongodb://localhost:27017/news_app")

suburb_data = open("suburbs.json")

suburb_list = json.load(suburb_data)

incident_data = open("incidents.json")

incident_list = json.load(incident_data)

line_data = open("line_data.json")

line_list = json.load(line_data)

# Homepage Route. Grabs one entry from Mongo database for the news headlines.
@app.route("/")
def welcome():

    news_data = mongo.db.data.find_one()

    return render_template("index.html", news=news_data)


# Route that returns the news_scrape data
@app.route("/scrape")
def scrape():

    get_data = news_scrape.scrape_all()

    mongo.db.data.update({}, get_data, upsert=True)

    return redirect("/")


# Route used for when clicking on news tab 
# Note: If this route is not attached to the tab, if a person does not have an existing entry in the database the tab will not display because it can't iterate over the array's.
# Attaching the scraping route to the news tab link ensures that the scraping is complete and the page will generate (a bit time consuming, but necessary.)
@app.route("/news_tab_scrape")
def news_tab_scrape():

    get_data = news_scrape.scrape_all()

    mongo.db.data.update({}, get_data, upsert=True)
    
    news_data = mongo.db.data.find_one()

    return render_template("news.html", news=news_data)


@app.route("/suburbs")
def suburbs():

    return jsonify(suburb_list)


@app.route("/incidents")
def incidents():

    return jsonify(incident_list)


@app.route("/line_data")
def line_data():

    return jsonify(line_list)
   


if __name__ == "__main__":
    app.run(debug=True)


