# -*- coding: utf-8 -*-
"""
Scrape the COVID-19 tracking tables from VWU
"""
import json
import requests
from slugify import slugify
from bs4 import BeautifulSoup
from datetime import datetime as dt

# !pip install -r requirements.txt
# !pip freeze > requirements.txt

response = requests.get('https://www.wvu.edu/return-to-campus/daily-test-results/morgantown/all')
split = "".join(line.strip() for line in response.text.split('\n')) ## remove newlines
soup = BeautifulSoup(split)

## find the data tables on the page
tables = soup.findAll('table')

## ensure tr is not a header
#### headers have bg and are not border-left
def tr_no_bg(css_class):
    notHeader = css_class not in ['background-yellow','background-blue-grey']
    hasBorderLeft = css_class == 'border-left'
    return notHeader and hasBorderLeft

## grab data from tr
#### iteratively preserve column name in obj
def extract_tr(row, headers):
  parsed = {}
  for idx,header in enumerate(headers):
    parsed[header] = row.contents[idx].find('time')['datetime'] if row.contents[idx].find('time') not in [-1, None] else row.contents[idx].string
  return parsed

## iterate through all tables on page
for table in tables:
  title = table.previous.find('caption').contents[0]
  slug = slugify(title)
  description = table.previous.find('caption').contents[1].text
  headers = [th.text for th in table.findAll('th', class_='background-blue-grey')] if table.findAll('th', class_='background-blue-grey') else [th.text for th in table.findAll('th', class_='background-yellow')]
  rows = table.findAll('tr', class_=tr_no_bg)
  data = [extract_tr(row, headers) for row in rows]
  formatted = {
      'title': title,
      'description': description,
      'date_scraped': dt.now().strftime("%Y-%m-%d-%H:%M:%S"),
      'data': data
  }

  with open(f'{slug}.json', 'w') as file:
    json.dump(formatted, file)