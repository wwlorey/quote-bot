import os
import re
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome('C:\Program Files\ChromeDriver\chromedriver.exe', chrome_options=options)
driver.get('http://wwlorey.x10host.com/quote_of_the_day.html')

match = re.search("Today's\sQuote(</b><br />|</b><br/>|<br/>)[\n\r\s]([\w\s]+\S).*\n.*_blank\">(.+)</a>", driver.page_source)

try:
  if match is None:
    raise Exception
except Exception:
  print(':-(')
else:
  print(match.group(2), match.group(3))

driver.close()