import os, re, smtplib, tweepy, time, sis
import credentials as cred
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ambigSubject = 'ERROR | Twitter Bot v0r0'
ambigBody = 'Error in quote extraction or source connection :(' 
toAddr = 'wwlorey@gmail.com'

def sendEmail(subject, body, toAddr):
  msg = MIMEMultipart('alternative')

  # Message parameters
  msg['Subject'] = subject
  msg['From'] = cred.FROM_ADDR
  msg['To'] = toAddr

  # Message body
  msg.attach(MIMEText(body, 'plain'))

  s = smtplib.SMTP_SSL('smtp.gmail.com')
  s.login(cred.FROM_ADDR, cred.PASSWORD)

  s.sendmail(cred.FROM_ADDR, [toAddr], msg.as_string())
  s.quit()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome('C:\Program Files\ChromeDriver\chromedriver.exe', chrome_options=options)
driver.get('http://wwlorey.x10host.com/quote_of_the_day.htmll')

match = re.search("Today's\sQuote(</b><br />|</b><br/>|<br/>)[\n\r\s]([\w\s]+\S).*\n.*_blank\">(.+)</a>", driver.page_source)

try:
  if match is None:
    raise Exception
except Exception:
  sendEmail(ambigSubject, ambigBody, toAddr)
else:
  print(match.group(2), match.group(3))

driver.close()