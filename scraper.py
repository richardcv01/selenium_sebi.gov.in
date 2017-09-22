from urllib.request import Request, urlopen
import re,csv

import time

import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from lxml import etree


BASE_URL = 'http://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=26'
phantomjs_path = os.path.abspath("G:\phantomjs\\bin\phantomjs.exe")
print(phantomjs_path)

def parse_url(html):
    tree = etree.HTML(html)
    name_list = tree.xpath('//div[@class="value varun-text"]/span/text()')
    name_val = tree.xpath('//div[@class="value"]/span/text()')

    #print(len(name_list))
    print(name_val)

n=0
#driver = webdriver.Chrome(executable_path='\chromedriver.exe')
driver = webdriver.PhantomJS(executable_path=phantomjs_path)
driver.set_window_size(1400, 1000)
driver.get(BASE_URL)

def get_html(n):
    n=n+1
    # req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    # response = urlopen(req).read()
    #driver = webdriver.Chrome(executable_path='\chromedriver.exe')
    #driver.get(url)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    #print(get_count_page(driver))
    #next_page_link(driver)
    #time.sleep(3)
    html = driver.page_source
    parse_url(html)
    print('parse', n)
    if n < 4 :
        next_page_link(driver, n)
        time.sleep(1)
        get_html(n)

    return driver.page_source

def next_page_link(driver, number_page):
    jscode = "javascript: searchFormFpi('n', '" + str(number_page) + "');"
    driver.execute_script(jscode);

def get_count_page(driver):
    element_li = driver.find_element_by_xpath('//li[@class=""]/a')
    result = re.findall(r'\d', element_li.get_attribute('href'))
    coun = int(''.join(result))
    return coun



    #return projects

def main():
    #html = parse_url(get_html(BASE_URL))
    html = get_html(0)

    #print(html)
    parse_url(html)
    driver.close()
    # get_html(BASE_URL)
if __name__ == '__main__':
    main()