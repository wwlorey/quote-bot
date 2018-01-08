import os
import re
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options

chrome_options = Options()  
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('C:\Program Files\ChromeDriver\chromedriver.exe')
driver.get("http://wwlorey.x10host.com/quote_of_the_day.html")

page_text = driver.page_source
print(page_text)

driver.close()