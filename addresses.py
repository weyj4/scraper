import csv
import requests
from bs4 import BeautifulSoup
import sys
import getopt
import pickle

def getZips():
  with open(inputfile, 'rU') as csvfile:
    global zipcodes
    zipcodes = []
    codes = (csvfile)
    for row in codes:
      row = row.split(',')
      for code in row:
        zipcodes.append(code)

def getZillow(url):
  zillow = requests.get(url)
  data = zillow.text
  global soup
  soup = BeautifulSoup(data)

def getCount():
  global count
  try:
    count = int(soup.find('li', 'zsg-pagination-next').previous_sibling.string)
  except:
    count = 1

def getUrls():
  print len(soup.find_all('a', 'hdp-link routable'))
  for house in soup.find_all('a', 'hdp-link routable'):
    print house.get('href')
    addresses.append(house.get('href'))

def getPages(code):
  for i in range(count + 1):
    url = 'http://zillow.com/homes/' + code + '_rb/1_rs/' + str(i+1) + '_p'
    print url
    getZillow(url)
    getUrls()

def getFiles(argv):

  global inputfile
  global outputfile

  try:
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
  except getopt.GetoptError:
    print 'test.py -i <inputfile> -o <outputfile>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'scriptname.py -i <inputfile> -o <outputfile>'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg

  try:
    testInputFile = open(inputfile, "rU")
    testInputFile.close()
  except:
    print 'scriptname.py -i <inputfile> -o <outputfile>'
    sys.exit()

  try:
    newFile = open(outputfile, "a")
  except:
    print 'scriptname.py -i <inputfile> -o <outputfile>'
    sys.exit()

def writeAddresses():
  with open(outputfile, 'w') as csv:
    pickle.dump(addresses, csv)

def doScrape():
  getFiles(sys.argv[1:])
  getZips()
  global addresses
  addresses = []
  for code in zipcodes:
    print code
    url = 'http://zillow.com/homes/' + str(code) + '_rb/1_rs'
    getZillow(url)
    getCount()
    getPages(code)
  writeAddresses()
  print len(addresses)

doScrape()