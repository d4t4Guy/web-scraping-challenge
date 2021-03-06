#dependencies:
import pandas as pd
import time #allows for sleep method. To-Do: Research if there is a method that doesn't require an additional module
from bs4 import BeautifulSoup #html parser

#   required for splinter (To-Do: need to verify splinter dependencies)
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser

#hardcoded URLs:

news_path = 'https://mars.nasa.gov/news/' #scrape most recent news article
gallery_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars' #get link for photo
JPL_base_url = 'https://www.jpl.nasa.gov' #root URL related to link for photo
mars_facts_url = 'https://www.space-facts.com/mars/' #table
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
    ]


#fn to return bs4 soup object from a target URL. 
    # Takes string URL as argument, returns soup.

def scrape_url(target_url):
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
def parse_news(soup):
	news_title = soup.find('h3', class_='').text #works correctly 2021-03-17.
	news_paragraph =soup.find('li', class_='slide') \
	                    .find('div', class_="article_teaser_body").text
	return news_title, news_paragraph
#############################################

#function to parse gallery soup to get URL for full-size image. returns URL as a string
def parse_gallery(soup):
	top_photo_url = JPL_base_url+soup.find('div', class_="SearchResultCard").find('a', class_="group cursor-pointer block").get('href')
	return top_photo_url
#############################################

#function to parse gallery soup to get URL for full-size image. returns URL as a string
def parse_featured_image(soup):
	return soup.find(string='Download JPG ').find_previous('a').get('href')
#############################################

#function to parse mars facts into a table
def parse_facts(soup):
	labels = []
	points = []

	table = soup.find('table', class_='tablepress tablepress-id-p-mars')
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	for row in rows:
	    cols=row.find_all('td', class_='column-1')
	    for col in cols:
	        txt = col.get_text()
	        labels.append(txt)
	    
	    cols=row.find_all('td', class_='column-2')
	    for col in cols:
	        txt = col.get_text()
	        points.append(txt)

	df = pd.DataFrame({'Mars':points}, index=labels)
	html_table = df.to_html()
	return html_table


def scrape():
	#using fns to pull news
	soup = scrape_url(news_path)
	news_headline, news_teaser = parse_news(soup)
	#Get URL for current photo from gallery
	soup = scrape_url(gallery_url)
	top_photo_url = parse_gallery(soup)
	soup = scrape_url(top_photo_url)
	featured_image_url = parse_featured_image(soup)
	#get mars facts for table
	soup = scrape_url(mars_facts_url)
	html_table = parse_facts(soup)
#loading vars into dict. Could probably have boiled down to fewer steps, but breaking out for readability
	scrape_dict = {}
	scrape_dict['news_headline'] = news_headline
	scrape_dict['news_teaser']   = news_teaser
	scrape_dict['featured_image_url'] = featured_image_url
	scrape_dict['html_table'] = html_table
	scrape_dict['hemisphere_image_urls'] = hemisphere_image_urls 
	#scrape_dict = {'news_headline': "NASA's Mars Helicopter to Make First Flight Attempt Sunday", 'news_teaser': 'The small rotorcraft???s ???Wright brothers moment??? is two Mars days away.', 'featured_image_url': 'https://d2pn8kiwq2w21t.cloudfront.net/original_images/jpegPIA24556.jpg', 'html_table': '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Mars</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.39 ?? 10^23 kg (0.11 Earths)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.38 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-87 to -5 ??C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>', 'hemisphere_image_urls': [{'title': 'Valles Marineris Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}, {'title': 'Cerberus Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'}, {'title': 'Schiaparelli Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'}, {'title': 'Syrtis Major Hemisphere', 'img_url': 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'}]}
	return scrape_dict
