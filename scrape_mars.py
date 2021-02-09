# import modules and dependencies
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time

# define executable path
executable_path = {"executable_path":"C:\webdrivers\chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)

# Scrape dictionary (collection) for return values below, following craigslist example from class
def scrape_():
    listings = {}
    listings["NasaMarsNews"] = Nasa_Mars_News()
    listings["NasaMarsPar"] = Nasa_Mars_News()
    listings["JPL_MarsSpace"] = JPL_Mars_Space()
    listings["Marsfacts"] = MarsFacts()
    listings["MarsHemis"] = Mars_Hemis()
    return listings

# Part 1: Nasa Mars News
# initiate visit to our URL given
def Nasa_Mars_News():
    browser.visit("https://mars.nasa.gov/news/")

    # BeautifulSoup module for HTML parsing
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')
    # Print to test scrape
    print(nasa_soup).pretify()

    # Collect the latest News Title Text
    titles_nasa = nasa_soup.find("div", class_ = "content_title").text
    print(f"Title: {titles_nasa}")
    return titles_nasa

    # Collect the latest Paragraph Text
    paragraphs_nasa = nasa_soup.find("div", class_ = "article_teaser_body").text
    print(f"Paragraph: {paragraphs_nasa}")
    return paragraphs_nasa

# Part 1: JPL Mars Space Images
# Space Images - JPL Mars, get the URL and initiate visit, and parse
def JPL_Mars_Space():
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(jpl_url)
    jpl_html = bs(browser.html, "html.parser")
    print(jpl_html)

    # Find the location of the images using inspector, get html string
    mars_image = jpl_html.find("img", class_ = "headerimage fade-in")["src"]
    print(mars_image)

    # Add to the end of the rest of the html string
    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + mars_image
    featured_image_url
    return featured_image_url

# Part 1: Mars Facts
# Visit the URL
def MarsFacts():
    mars_fact_url = "https://space-facts.com/mars/"
    browser.visit(mars_fact_url)

    # Get the data into a df
    fact_table = pd.read_html(mars_fact_url)
    #print(fact_table)
    fact_table_df = pd.DataFrame(fact_table[0])
    fact_table_df.columns = ["Description", "Metric"]
    print(fact_table_df)

    # Convert data to html table string
    fact_table_html = fact_table_df.to_html(header=False, index=True)
    fact_table_html
    return fact_table_html

# Part 1: Mars Hemispheres
# Visit the URL and parse
def Mars_Hemis():
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemis_url)

    hemis_html = browser.html
    hemis_soup = bs(hemis_html, 'html.parser')
    print(hemis_soup).pretify()

    # create empty list for our upcoming for loop to scrape images
    hemis_list = []

    # Use inspector to find location one level above images, assign to variable
    hemis_images = hemis_soup.find_all("div", class_ = "item")

    # URL to add image strings to
    hemis_base_url = "https://astrogeology.usgs.gov"

    # For loop through item class, gathering images
    for hemis_scrape in hemis_images:
        hemis_image_titles = hemis_scrape.find("h3").text
        hemis_links = hemis_scrape.find("a")["href"]
        total_hemis_urls = hemis_base_url + hemis_links
        # print(hemis_image_titles)
        # print(total_hemis_urls)
        hemis_append_dict = {"title": hemis_image_titles, "img_url": total_hemis_urls}
        hemis_list.append(hemis_append_dict)
    return hemis_list