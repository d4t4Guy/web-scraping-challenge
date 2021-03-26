#dependencies:
import pandas as pd
import time #allows for sleep method. To-Do: Research if there is a method that doesn't require an additional module
from bs4 import BeautifulSoup #html parser

#   required for splinter (To-Do: need to verify splinter dependencies)
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

#create driver
executable_path = {'executable_path':ChromeDriverManager().install()}  #To-do: continue searching for more efficient method
#set up browser
browser = Browser('chrome', **executable_path, headless=False)
#scrape most recent news article
news_path = 'https://mars.nasa.gov/news/'
browser.visit(news_path)
time.sleep(3) #wait for Browser to render JS
html = browser.html
browser.quit()

#use bs4 to parse the title and paragraph
soup=BeautifulSoup(html, 'html.parser') #returns a soup object
news_title = soup.find('h3', class_='').text #works correctly 2021-03-17.
# Observation that most recent news article headline is under the first 
# <h3> tag with no CSS class assigned