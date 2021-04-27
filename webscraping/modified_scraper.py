#!/usr/bin/python

import sys
import os
import lxml.etree
import lxml.html
import html
from lxml.etree import tostring
from urllib.request import Request, urlopen
import json
import time
import random
import re
import json
from datetime import timedelta, date
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

import urllib

# Reference the local Chromedriver instance
chrome_path = r'/Users/ccb/Data/Google-News-Crawler/chromedriver'

"""
This script was written to search Google news for a list of search terms over a 
specified range of dates.  The idea here is to replicate the methodology used by
Jennifer Mascia to put together the The Gun Report, which was a New York Times blog
that chronicled daily shootings across the country.  The methodology is described 
in an On the Media interview:  http://www.onthemedia.org/story/end-gun-report/
"""


# do this for sureeeeeeeeeeeeeeeeeeee
# Run pip install webdriver-manager

# def install_chromedriver():
#     """
#     You should run this install method once to install
#     the Chrome Driver for Selenium, and then modify the
#     `chrome_path` variable above.
#     """
#     driver = webdriver.Chrome(ChromeDriverManager().install())


def launch_selenium(login=False):
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=chromeuserdata")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.implicitly_wait(4)
    if login:
        driver.get(dndbeyon_login)
        input("Please login in Chrome, and then press Enter on the terminal to continue...")
    return driver


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield end_date - timedelta(n)


if len(sys.argv) < 3:
    sys.stderr.write(
        "Usage: python compile_google_news_links_selenium.py startYear-startMonth-startDay endYear-endMonth-endDay\n")
    exit(0)

sdate = sys.argv[1]
edate = sys.argv[2]
sy, sm, sd = sdate.split('-')
ey, em, ed = edate.split('-')
start_date = date(int(sy), int(sm), int(sd))
end_date = date(int(ey), int(em), int(ed))

# search_terms = ["Supplemental Nutrition Assistance Program", "food stamps", "SNAP"]
search_terms = ["Supplemental Nutrition Assistance Program", "food stamps"]

sys.stderr.write("Search from %s to %s for terms %s\n" % (start_date, end_date, str(search_terms)))


def add_to_database(data_dict, date_str, term, link):
    entry = {
        'term': term.strip().lower(),
        'link': link.strip()
    }
    if date_str.strip().lower() not in data_dict.keys():
        # new date
        data_dict[date_str.strip().lower()] = [entry]
    else:
        data_dict[date_str.strip().lower()].append(entry)


def write_data_to_output_json(data_dict, output_name=None):
    if not output_name:
        output_name = 'output.json'
    with open(output_name, 'w+') as file:
        file.write(json.dumps(data_dict, indent=2))


def filter_article_text(text):
    return text
    # define some filtering logic here


def get_article_text(url):
    from newspaper import Article

    # download and parse article
    article = Article(url)
    article.download()
    article.parse()

    # print article text
    return filter_article_text(article.text)


def main():
    first_run = True
    driver = launch_selenium()
    seen = set()
    data = {}
    # Iterate through dates
    for single_date in daterange(start_date, end_date):
        for term in search_terms:
            url = 'https://www.google.com/search?'
            values = {'q': term,
                      'hl': 'en',
                      'gl': 'us',
                      'authuser': '0',
                      'source': 'lnt',
                      'tbs': 'cdr:1,cd_min:' + single_date.strftime("%m/%d/%Y") + ",cd_max:" + single_date.strftime(
                          "%m/%d/%Y"),
                      'tbm': 'nws',
                      'start': '0'}

            sys.stderr.write("***" + url + urllib.parse.urlencode(values) + '\n')
            driver.get(url + urllib.parse.urlencode(values))
            if first_run:
                sys.stderr.write(
                    "Set search preferences by going to Settings > Search Settings, and set the Results per page to 100")
                confirmation = input("type \"done\" when this is complete and hit Enter/Return\n")
                while confirmation.strip() != 'done':
                    confirmation = input("type \"done\" when this is complete and hit Enter/Return\n")
                first_run = False
            for i, a in enumerate(driver.find_elements_by_tag_name('a')):
                try:
                    link = a.get_attribute('href')
                    while (link is not None) and (link.startswith('https://www.google.com/sorry')):  # detect captchas
                        sys.stderr.write("Blocked on: %s\n" % (str(link)))
                        sleep(10)
                        link = a.get_attribute('href')
                    if (link is not None) and (link not in seen):
                        if "google.com" not in link and "webcache.googleusercontent" not in link:  # remove some obvious ads and junk <a> elements
                            print(single_date.strftime("%Y-%m-%d"), "\t", term, "\t", link)
                            add_to_database(data, str(single_date.strftime("%Y-%m-%d")), term, link)
                            seen.add(link)
                except StaleElementReferenceException:
                    sys.stderr.write("Stale element: %s\n" % str(a))
    write_data_to_output_json(data)
    driver.close()


if __name__ == "__main__":
    # main()
    pass
    # this code doesn't do anything right now