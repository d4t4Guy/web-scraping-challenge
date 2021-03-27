#dependencies:
import pandas as pd
import time #allows for sleep method. To-Do: Research if there is a method that doesn't require an additional module
from bs4 import BeautifulSoup #html parser

#   required for splinter (To-Do: need to verify splinter dependencies)
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

#hardcoded URLs:

news_path = 'https://mars.nasa.gov/news/' #scrape most recent news article
gallery_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'


#fn to return bs4 soup object from a target URL. 
    # Takes string URL as argument, returns soup.

def scrape_url(target_url)
#create driver
executable_path = {'executable_path':ChromeDriverManager().install()}  #To-do: continue searching for more efficient method
#set up browser
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(target_url)
time.sleep(3) #wait for Browser to render JS
html = browser.html
browser.quit()
return BeautifulSoup(html, 'html.parser')
#############################################

#function to get news article teaser
def parse_news(soup)
news_title = soup.find('h3', class_='').text #works correctly 2021-03-17.
news_paragraph =soup.find('li', class_='slide') \
                    .find('div', class_="article_teaser_body").text
return (f'{news_title} \n {news_paragraph}')
#############################################

#using fns to pull info
soup = scrape_url(news_path)
teaser = parse_news(soup)
print(teaser)