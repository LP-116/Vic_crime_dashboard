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

