# Import dependencies:
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time 
import pandas as pd

def scrape():

    # PART 1: NASA MARS NEWS 

    # Declare url:
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Retrieve page using the requests module:
    news_response = requests.get(news_url)

    # Create BeautifulSoup object and parse with html.parser:
    news_soup = bs(news_response.text, "html.parser")

    # Retrieve latest news article's title from soup object:
    news_title = news_soup.find_all("div", class_="content_title")[0].text

    # Retrieve latest article's paragraph text from soup object:
    news_p = news_soup.find_all("div", class_="image_and_description_container")[0].text

    # PART 2: JPL MARS SPACE IMAGE

    # Declare executable path and browser:
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Declare and visit url:
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Create soup object:
    jpl_html = browser.html
    jpl_soup = bs(jpl_html, 'html.parser')

    # Retrieve latest Mars image from webpage:
    image = jpl_soup.find_all("img", class_="thumb", alt="Wind Erosion")
    featured_image_url = image[0]["src"]

    featured_image_url = "https://www.jpl.nasa.gov/" + featured_image_url

    # PART 3: MARS WEATHER

    # Declare url:
    nasa_twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(nasa_twitter_url)

    # Pause for 5 seconds:
    time.sleep(5)

    # Create soup object:
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'html.parser')

    # Retrieve current Mars weather from soup object:
    mars_weather_article = twitter_soup.find("article")
    mars_weather = mars_weather_article.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")[4].text

    # PART 4: MARS FACTS

    # Declare url:
    facts_url = "https://space-facts.com/mars/"

    # Scrape tabular data:
    facts_table = pd.read_html(facts_url)
    facts_table

    # Insert scraped data into dataframe:
    facts_df = pd.DataFrame(facts_table)

    facts_df = facts_table[2]
    facts_df.columns = ["Metric", "Measurement"]

    # Convert to html:
    facts_table_html = facts_df.to_html(classes="table table-striped")

    # PART 5: MARS HEMISPHERES

    # Declare url:
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)

    # Pause for 5 seconds:
    time.sleep(5)

    # Create soup object:
    usgs_html = browser.html
    usgs_soup = bs(usgs_html, 'html.parser')

    # Retrieve Mars hemispheres images from soup object:

    cerberus_image_url = usgs_soup.find("img", alt="Cerberus Hemisphere Enhanced thumbnail")["src"]
    cerberus_image_url = "https://astrogeology.usgs.gov/" + cerberus_image_url

    schiaparelli_image_url = usgs_soup.find("img", alt="Schiaparelli Hemisphere Enhanced thumbnail")["src"]
    schiaparelli_image_url = "https://astrogeology.usgs.gov/" + schiaparelli_image_url

    syrtis_major_image_url = usgs_soup.find("img", alt="Syrtis Major Hemisphere Enhanced thumbnail")["src"]
    syrtis_major_image_url = "https://astrogeology.usgs.gov/" + syrtis_major_image_url

    valles_marineris_image_url = usgs_soup.find("img", alt="Valles Marineris Hemisphere Enhanced thumbnail")["src"]
    valles_marineris_image_url = "https://astrogeology.usgs.gov/" + valles_marineris_image_url

    # DICTIONARY:

    mars_dictionary = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "facts_table_html": facts_table_html,
        "cerberus_image_url": cerberus_image_url,
        "schiaparelli_image_url": schiaparelli_image_url,
        "syrtis_major_image_url": syrtis_major_image_url,
        "valles_marineris_image_url": valles_marineris_image_url
    }

    return mars_dictionary