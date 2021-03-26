#dependencies:
import pandas as pd
import time #allows for sleep method. To-Do: Research if there is a method that doesn't require an additional module
from bs4 import BeautifulSoup #html parser

#required for splinter (To-Do: need to verify splinter dependencies)
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
