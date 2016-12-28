import urllib2
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pprint as pp
import re
import csv
import time

def prefixing(base_url, links):
    prefixed_link = str(links).replace("/", base_url, 1)
    return prefixed_link

def set_price(set_url):
    # include set release date as a value
    # returns set name using the url provided
    reg_exp = re.compile('(\w|[()\w])*$') # move outside the function so it doesnt reassign each time the function runs. Alternative regex = \w*$
    set_name = reg_exp.search(set_url).group()
    # add a regular expression to check for foil values
    # webdriver
    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
    driver.get(set_url)
    time.sleep(5)
    set_page = driver.page_source
    set_soup = BeautifulSoup(set_page, 'html.parser')
    card_tables = set_soup.findAll('tr', attrs={'class': 'ng-scope'})
    for card in card_tables:
        card_name = card.find('a').get_text()
        card_price = card.find('td', attrs={'class': 'ng-binding'}).get_text()
        print card_name, "\t", card_price
        with open('mtg_prices_total.csv', 'ab') as prices:
            csv_scraped = csv.writer(prices)
            csv_scraped.writerow([card_name, card_price, set_name])
            # csv_scraped.close # close the csv file
    driver.close()
    # wait for a moment...
    time.sleep(30)


# Base page crawler
url = "http://www.mtgprice.com/magic-the-gathering-prices.jsp"
html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Max OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})
page_html = html.text
bsObj = BeautifulSoup(page_html, 'html.parser')
set_rows = bsObj.findAll("table", attrs={'id': 'setTable'})
set_links = bsObj.findAll('td')
card_set_urls = []
card_set_date = [] # retrieve dates
for set in set_links:
    links = set.find('a')
    if links is not None:
        card_set_urls.append(prefixing("http://www.mtgprice.com/", links['href']))
    """
    for link in links:
        print link
        card_set_url.append(link['href'])
        card_set.append(link.content[0])
    """
#print card_set #doesnt retrieve card set names.
#pp.pprint(card_set_urls)

[set_price(href) for href in card_set_urls]
