import time
import os
from selenium import webdriver
import re
from lxml import etree
import csv
import io

BASE_URL = 'http://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=26'
phantomjs_path = os.path.abspath("G:\phantomjs\\bin\phantomjs.exe")
print(phantomjs_path)

def write_svc(data):
    FILENAME = "users.csv"
    with io.open(FILENAME, "a", encoding="utf-8") as file:
        #f.write(html)
    #with open(FILENAME, "w", newline="") as file:
        columns = list(data[0].keys())
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        # запись нескольких строк
        writer.writerows(data)
        print("write Ok!")

def parse_url(html):
    tree = etree.HTML(html)
    name_list = tree.xpath('//div[@class="value varun-text"]/span/text()')

    #name_val = tree.xpath('//div[@class="value"]/span/text()')
    list_element = tree.xpath('//div[@class="fixed-table-body card-table"]')
    name = tree.xpath('.//div[@class="value varun-text"]/span/text()')
    el = list_element[0].xpath('.//div[@class="value"]/span/text()')
    list_data = []
    for element in list_element:
        table = element.xpath('.//div[@class="value"]/span/text()')
        dic = {}
        dic["name"] = element.xpath('.//div[@class="value varun-text"]/span/text()')[0]
        if len(table) == 6:
            dic['Registration No'] =  element.xpath('.//div[@class="value"]/span/text()')[0]
            dic['Telephone'] = "",
            dic['Fax No'] = "",
            dic['Address'] = element.xpath('.//div[@class="value"]/span/text()')[1]
            dic['Validity'] = element.xpath('.//div[@class="value"]/span/text()')[2]
            dic['Exchange Name'] = element.xpath('.//div[@class="value"]/span/text()')[3]
            dic['Affiliated Broke'] = element.xpath('.//div[@class="value"]/span/text()')[4]
            dic['Affiliated Broker Reg. No'] = element.xpath('.//div[@class="value"]/span/text()')[5]
        elif len(table) == 7:
            dic['Registration No'] = element.xpath('.//div[@class="value"]/span/text()')[0]
            dic['Telephone'] = element.xpath('.//div[@class="value"]/span/text()')[1]
            dic['Fax No'] = ""
            dic['Address'] = element.xpath('.//div[@class="value"]/span/text()')[2]
            dic['Validity'] = element.xpath('.//div[@class="value"]/span/text()')[3]
            dic['Exchange Name'] = element.xpath('.//div[@class="value"]/span/text()')[4]
            dic['Affiliated Broke'] = element.xpath('.//div[@class="value"]/span/text()')[5]
            dic['Affiliated Broker Reg. No'] = element.xpath('.//div[@class="value"]/span/text()')[6]
        elif len(table) == 8:
            dic['Registration No'] = element.xpath('.//div[@class="value"]/span/text()')[0]
            dic['Telephone'] = element.xpath('.//div[@class="value"]/span/text()')[1]
            dic['Fax No'] = element.xpath('.//div[@class="value"]/span/text()')[2]
            dic['Address'] = element.xpath('.//div[@class="value"]/span/text()')[3]
            dic['Validity'] = element.xpath('.//div[@class="value"]/span/text()')[4]
            dic['Exchange Name'] = element.xpath('.//div[@class="value"]/span/text()')[5]
            dic['Affiliated Broke'] = element.xpath('.//div[@class="value"]/span/text()')[6]
            dic['Affiliated Broker Reg. No'] = element.xpath('.//div[@class="value"]/span/text()')[7]
        list_data.append(dic)
    write_svc(list_data)
    print(list_data)
    return list_element

def next_page_link(driver, number_page):
    jscode = "javascript: searchFormFpi('n', '" + str(number_page) + "');"
    driver.execute_script(jscode);

class Web_Driver():
    def get_html(self):
        driver = webdriver.PhantomJS(executable_path=phantomjs_path)
        driver.set_window_size(1400, 1000)
        driver.get(BASE_URL)
        SCROLL_PAUSE_TIME = 3

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
        html = driver.page_source
        parse_url(html)
        return driver


def get_htmlN(n,N,driver):
    n_ = n
    N_ = N
    driver_ = driver
    next_page_link(driver, n_)
    time.sleep(2)
    html = driver.page_source
    n_=n_+1
    if n < N:
        get_htmlN(n_, N_, driver_)
    print('parse', n, parse_url(html))

def get_count_page(driver):
    element_li = driver.find_element_by_xpath('//li[@class=""]/a')
    result = re.findall(r'\d', element_li.get_attribute('href'))
    coun = int(''.join(result))
    return coun

from threading import Thread
def main():
    time1 = time.time()
    driver1 = Web_Driver().get_html()
    #driver2 = Web_Driver().get_html()
    #driver3 = Web_Driver().get_html()
    #driver4 = Web_Driver().get_html()
    #get_htmlN(1, 400, driver1)
    #t1 = Thread(target=get_htmlN, args=(0,0, driver1))
    #t2 = Thread(target=get_htmlN, args=(11,20, driver2))
    #t3 = Thread(target=get_htmlN, args=(201, 300, driver3))
    #t4 = Thread(target=get_htmlN, args=(301, 400, driver4))
    #t1.start()
    #t2.start()
    #t3.start()
    #t4.start()
    #t1.join()
    #t2.join()
    #t3.join()
    #t4.join()
    time2 = time.time()
    print(time2 - time1)


if __name__ == '__main__':
    main()


