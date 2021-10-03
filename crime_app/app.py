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

map_2020_data = open("map_2020.json")

map_2020_list = json.load(map_2020_data)

map_2021_data = open("map_2021.json")

map_2021_list = json.load(map_2021_data)

stats_data = open("stats_data.json")

stats_list = json.load(stats_data)

data_tab = open("data_data.json")

data_list = json.load(data_tab)

# Homepage Route. Grabs one entry from Mongo database for the news headlines.
@app.route("/")
def welcome():

    news_data = mongo.db.data.find_one()

    return render_template("index.html", news=news_data)



@app.route("/data.html")
def data_tab():

    return render_template("data.html")


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
   

@app.route("/map_data")
def map_data():

    return jsonify(map_list)


@app.route("/map_2020")
def map_2020():

    return jsonify(map_2020_list)


@app.route("/map_2021")
def map_2021():

    return jsonify(map_2021_list)


@app.route("/stats_data")
def stats_data():

    return jsonify(stats_list)


@app.route("/data_tab")
def data():

    return jsonify(data_list)





if __name__ == "__main__":
    app.run(debug=True)


