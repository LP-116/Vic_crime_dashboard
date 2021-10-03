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

# Import and dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd
import json


def scrape_all():

    # Establishing connection to the browser.
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # News webpage to scrape the data.
    url='https://www.news.com.au/national/victoria/crime'
    browser.visit(url)

    # Create BeautifulSoup object
    html = browser.html
    soup = bs(html, 'html.parser')


    try:
        # Finding the first 5 headlines, urls and descriptions and adding to a list.

        headline_list = []

        headlines = soup.find_all('a', class_='storyblock_title_link')

        for headline in headlines:
            if len(headline_list) < 5:
                title= headline.text.strip()
                headline_list.append(title)


        link_list = []

        results = soup.find_all('h4', class_='storyblock_title')

        for result in results:
            if len(link_list) < 5:
                link = result.a['href']
                link_list.append(link)


        paragraph_list = []

        for item in soup.find_all('p', class_="storyblock_standfirst g_font-body-s"):
            if len(paragraph_list) < 5:
                about= item.text.strip()
                paragraph_list.append(about)


        # Creating a dictionary to hold all the data.
        news_dict = {
            'Headline':headline_list,
            'URL':link_list,
            'Description':paragraph_list}


        # Ending the browser session.
        browser.quit()

    except AttributeError:
        return None

    # The news_dict is returned once the scrape is complete.
    return news_dict

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

    get_data = scrape_all()

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


