# Set up and dependencies.
import datetime as dt 
import numpy as np 
import pandas as pd 

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

# Connect to the postgresql database.
engine = create_engine(f"postgresql://{username}:{password}@localhost:5432/crime_db")

# Connect to the Mongo database.
mongo = PyMongo(app, uri="mongodb://localhost:27017/news_app")


# Reflect an existing database into a new model.
Base = automap_base()

# Reflect the tables.
Base.prepare(engine, reflect=True)

# Save references to the table
crime = Base.classes.crime


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


# This route returns a list of unique suburbs - it is used to populate the suburb drop down boxes. 
@app.route("/api/v1.0/suburbs")
def suburbs():

    session = Session(engine)
    
    suburbs = session.query(crime.suburb).order_by((crime.suburb).asc()).distinct().all()
    
    session.close()

    suburb_list = list(np.ravel(suburbs))

    return jsonify(suburb_list)



# This route is used to create the bar graph. It shows all data for the year 2021, grouped by suburb.
@app.route("/api/v1.0/incidents")
def incidents():

    session = Session(engine)

    year = "2021"
    
    incidents = session.query(crime.year, crime.suburb, crime.offence_sub_div, func.sum(crime.incidents)).group_by(crime.year, crime.suburb, crime.offence_sub_div).filter((crime.year == year)).order_by(func.sum(crime.incidents).desc()).all()

    session.close()

    incident_list = []

    for year, suburb, offence_sub_div, sum_incidents in incidents:
        incident_dict ={}
        incident_dict["year"] = year
        incident_dict["suburb"] = suburb
        incident_dict["sub"] = offence_sub_div
        incident_dict["incidents"] = sum_incidents
        incident_list.append(incident_dict)

    return jsonify(incident_list)


# This route is used to create the 2021 layer of the map.
@app.route("/api/v1.0/map")
def total_map():

    session = Session(engine)

    year = "2021"

    total_map = session.query(crime.year, crime.suburb, crime.latitude, crime.longitude, func.sum(crime.incidents)).group_by(crime.year, crime.suburb, crime.latitude, crime.longitude).filter((crime.year == year)).order_by(func.sum(crime.incidents).desc()).all()

    map_list_2021 = []

    for year, suburb, latitude, longitude, sum_incidents in total_map:
        map_dict_2021 ={}
        map_dict_2021["year"] = year
        map_dict_2021["suburb"] = suburb
        map_dict_2021["latitude"] = latitude
        map_dict_2021["longitude"] = longitude
        map_dict_2021["incidents"] = sum_incidents
        map_list_2021.append(map_dict_2021)


    return jsonify(map_list_2021)


# This route is used to create the 2020 layer of the map.
@app.route("/api/v1.0/map2")
def map_2020():

    session = Session(engine)

    year = "2020"

    map_2020 = session.query(crime.year, crime.suburb, crime.latitude, crime.longitude, func.sum(crime.incidents)).group_by(crime.year, crime.suburb, crime.latitude, crime.longitude).filter((crime.year == year)).order_by(func.sum(crime.incidents).desc()).all()

    session.close()

    map_list_2020 = []

    for year, suburb, latitude, longitude, sum_incidents in map_2020:
        map_dict_2020 ={}
        map_dict_2020["year"] = year
        map_dict_2020["suburb"] = suburb
        map_dict_2020["latitude"] = latitude
        map_dict_2020["longitude"] = longitude
        map_dict_2020["incidents"] = sum_incidents
        map_list_2020.append(map_dict_2020)


    return jsonify(map_list_2020)


# This route is used to create the 2015 layer of the map.
@app.route("/api/v1.0/map3")
def map_2015():

    session = Session(engine)

    year = "2015"

    map_2015 = session.query(crime.year, crime.suburb, crime.latitude, crime.longitude, func.sum(crime.incidents)).group_by(crime.year, crime.suburb, crime.latitude, crime.longitude).filter((crime.year == year)).order_by(func.sum(crime.incidents).desc()).all()

    session.close()

    map_list_2015 = []

    for year, suburb, latitude, longitude, sum_incidents in map_2015:
        map_dict_2015 ={}
        map_dict_2015["year"] = year
        map_dict_2015["suburb"] = suburb
        map_dict_2015["latitude"] = latitude
        map_dict_2015["longitude"] = longitude
        map_dict_2015["incidents"] = sum_incidents
        map_list_2015.append(map_dict_2015)


    return jsonify(map_list_2015)


# This route is used to render the data tab.
@app.route("/data.html")
def data_tab():

    return render_template("data.html")


# This route is used to generate the table on the data tab.
@app.route("/api/v1.0/data_tab")
def data():

    session = Session(engine)
    
    data_tab = session.query(crime.year, crime.suburb, crime.offence_div, crime.offence_sub_div, func.sum(crime.incidents)).group_by(crime.offence_sub_div, crime.suburb, crime.year, crime.offence_div).order_by((crime.suburb).asc()).all()

    session.close()

    data_list = []

    for year, suburb, offence_div, offence_sub_div, sum_incidents in data_tab:
        data_dict ={}
        data_dict["year"] = year
        data_dict["suburb"] = suburb
        data_dict["off_div"] = offence_div
        data_dict["sub_div"] = offence_sub_div
        data_dict["incidents"] = sum_incidents
        data_list.append(data_dict)

    return jsonify(data_list)


# This route is used to generate the line graph.
@app.route("/api/v1.0/line_data")
def line():

    session = Session(engine)
    
    line_data = session.query(crime.year, crime.suburb, func.sum(crime.incidents)).group_by(crime.year, crime.suburb).order_by((crime.year).desc()).all()

    session.close()

    line_list = []

    for year, suburb, sum_incidents in line_data:
        line_dict ={}
        line_dict["year"] = year
        line_dict["suburb"] = suburb
        line_dict["incidents"] = sum_incidents
        line_list.append(line_dict)

    return jsonify(line_list)


# This route is used to generate the stats data on the home page.
@app.route("/api/v1.0/stats_data")
def stats():

    session = Session(engine)

    year = "2020"
    
    stats = session.query(crime.year, crime.suburb, func.sum(crime.incidents)).group_by(crime.year, crime.suburb).filter((crime.year >= year)).order_by(func.sum(crime.incidents).desc()).all()

    session.close()

    stats_list = []

    for year, suburb, sum_incidents in stats:
        stats_dict ={}
        stats_dict["year"] = year
        stats_dict["suburb"] = suburb
        stats_dict["incidents"] = sum_incidents
        stats_list.append(stats_dict)

    return jsonify(stats_list)

if __name__ == "__main__":
    app.run(debug=True)


