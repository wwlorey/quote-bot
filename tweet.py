import os, re, smtplib, tweepy, time, sys
import credentials as cred
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variables
ambigSubject = 'ERROR | Twitter Bot v0r0'
ambigBody = 'Error in quote extraction or source connection :(' 
toAddr = 'wwlorey@gmail.com'
SECONDS_IN_DAY = 24 * 60 * 60


# return: twitter API object authenticated with quote_bot_ credentials
def getTwitterAPI():
  auth = tweepy.OAuthHandler(cred.CONSUMER_KEY, cred.CONSUMER_SECRET)
  auth.set_access_token(cred.ACCESS_KEY, cred.ACCESS_SECRET)
  return tweepy.API(auth)

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


while True:
  driver.get('http://wwlorey.x10host.com/quote_of_the_day.html')

  match = re.search("Today's\sQuote(</b><br />|</b><br/>|<br/>)[\n\r\s]([\w\s]+\S).*\n.*_blank\">(.+)</a>", driver.page_source)

  try:
    if match is None:
      raise Exception
  except Exception:
    sendEmail(ambigSubject, ambigBody, toAddr)
  else:
    quote = match.group(2)
    author = match.group(3)

    api = getTwitterAPI()
    api.update_status('"%s" - %s' % (quote, author))

  time.sleep(SECONDS_IN_DAY) 