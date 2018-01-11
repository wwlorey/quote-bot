import os, re, smtplib, tweepy, time, sys
import credentials as cred
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Variables
SUBJECT = 'ERROR | Twitter Bot v0r0'
BODY = 'Error in quote extraction or source connection :(' 
TO_ADDR = 'wwlorey@gmail.com'
SECONDS_IN_DAY = 24 * 60 * 60

# Creates twitter connection w/ credentials outlined in credentials.py
# return: twitter API object
def getTwitterAPI():
  auth = tweepy.OAuthHandler(cred.CONSUMER_KEY, cred.CONSUMER_SECRET)
  auth.set_access_token(cred.ACCESS_KEY, cred.ACCESS_SECRET)
  return tweepy.API(auth)

# Sends an email from the address outlined in credentials.py to the provided address (toAddr)
#  w/ provided subject and body fields
# return: None
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

# Creates Chrome connection
# return: Chrome webdriver object
def getBrowserConnection():
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  return webdriver.Chrome('C:\Program Files\ChromeDriver\chromedriver.exe', chrome_options=options)

# Scrape quote and tweet it out every 24 hours
while True:
  driver = getBrowserConnection()
  driver.get('http://wwlorey.x10host.com/quote_of_the_day.html')

  match = re.search("Today's\sQuote(</b><br />|</b><br/>|<br/>)[\n\r\s]([\w\s]+\S).*\n.*_blank\">(.+)</a>", driver.page_source)

  try:
    if match is None:
      raise Exception
  except Exception:
    sendEmail(SUBJECT, BODY, TO_ADDR)
  else:
    quote = match.group(2)
    author = match.group(3)
    quoteStr = '"%s" - %s' % (quote, author) 

    prevTweet = open('prev_tweet.txt', 'r')

    line = prevTweet.readline()
    if str(line) == quoteStr:
      print("Quote was already tweeted.")
      pass
    else:
      print("Tweeting new quote...")
      prevTweet.close()
      prevTweet = open('prev_tweet.txt', 'w') # Clear the file
      prevTweet.write(quoteStr)

      api = getTwitterAPI()
      api.update_status(quoteStr)
      print("Quote has been tweeted.")

    prevTweet.close()

  driver.close()
  print("\nWaiting for 24 hours...\n")
  time.sleep(SECONDS_IN_DAY) 