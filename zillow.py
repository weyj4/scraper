import requests
from bs4 import BeautifulSoup
import re
import csv
import pickle

def Addresses():
  data = pickle.load( open("input.csv", "rb"))
  global addresses
  addresses = []
  for row in data:
    row = row.split(',')
    for add in row:
      addresses.append(add)

def getAddress():
  url='http://zillow.com' + address    
  page=requests.get(url)
  data=page.text
  global soup
  soup=BeautifulSoup(data)
  addr=page.url
  start=re.search('homedetails/', addr).end()
  end=re.search('941..', addr).end()
  addr = addr[start:end]
  array.append(addr)

def getComps():
  try:
    string=soup.find('h2', text='Comparable Homes').next_sibling
    start=string.index('$')
    comps=string[start:-1]
  except:
    comps='N/A'
    # compserr += 1
  array.append(comps)

def getZestimate():
  try:
    zest=soup.find('div', 'zest-value').string
  except:
    zest='N/A'
    # zesterr += 1
  array.append(zest)

def Scrape():
  Addresses()
  f = open('output.csv', 'wt')
  writer = csv.writer(f)
  writer.writerow(('Address', 'Zestimate', 'Comps'))
  # compserr = 0
  # zesterr = 0
  for x in addresses:
    global address
    address = x
    global array
    array = []
    getAddress()
    getComps()
    getZestimate()
    writer.writerow((array[0], array[1], array[2]))
  print compserr
  print zesterr

Scrape()





  
