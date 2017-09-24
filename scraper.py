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
All_list_data = []

def cler_file(file_name):
    with open(file_name, 'r') as f_input, open('data2.csv', 'w',newline='') as f_output:
        csv_output = csv.writer(f_output, delimiter = '\t')
        n = 0
        for row in csv.reader(f_input, delimiter = '\t'):
            n = n + 1
            if len(row):


               if row[0][0:4] != 'Name' or n == 1:
                   csv_output.writerow(row)

def write_svc(data):
    FILENAME = "Data.csv"
    with io.open(FILENAME, "a", encoding="utf-8", newline='') as file:
        #f.write(html)
    #with open(FILENAME, "w", newline="") as file:
        #columns = list(data[0].keys())
        columns = ['Name', 'Registration No', 'E-mail', 'Telephone', 'Fax No', 'Address', 'Validity',
                   'Exchange Name', 'Affiliated Broke', 'Affiliated Broker Reg. No']
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        # запись нескольких строк
        writer.writerows(data)

        print("write Ok!")

def replace(st):
    return re.sub("^\s+|\n|\r|\s+$", '',st)

def parse_url(html, n):
    tree = etree.HTML(html)
    list_element = tree.xpath('//div[@class="fixed-table-body card-table"]')
    #name = tree.xpath('.//div[@class="value varun-text"]/span/text()')
    #el = list_element[0].xpath('.//div[@class="value"]/span/text()')
    list_data = []

    for element in list_element:
        table = element.xpath('.//div[@class="value"]/span/text()')
        dic = {}
        dic["Name"] = replace(element.xpath('.//div[@class="value varun-text"]/span/text()')[0])
        try:
            i = 0
            el_email = replace(element.xpath('.//div[@class="value"]/span/text()')[1])
            el_fax = replace(element.xpath('.//div[@class="value"]/span/text()')[2])
            if re.search('@', el_email):
                dic['E-mail'] = el_email
                i = i + 1
                el_fax = ""
            else:
                dic['E-mail'] = ""

            if len(table) == 6:
                dic['Registration No'] =  replace(element.xpath('.//div[@class="value"]/span/text()')[0])
                dic['Telephone'] = "",
                dic['Fax No'] = "",
                dic['Address'] = replace(element.xpath('.//div[@class="value"]/span/text()')[1])
                dic['Validity'] = replace(element.xpath('.//div[@class="value"]/span/text()')[2])
                dic['Exchange Name'] = replace(element.xpath('.//div[@class="value"]/span/text()')[3])
                dic['Affiliated Broke'] = replace(element.xpath('.//div[@class="value"]/span/text()')[4])
                dic['Affiliated Broker Reg. No'] = replace(element.xpath('.//div[@class="value"]/span/text()')[5])
            elif len(table) == 7:
                dic['Registration No'] = replace(element.xpath('.//div[@class="value"]/span/text()')[0])
                dic['Telephone'] = replace(element.xpath('.//div[@class="value"]/span/text()')[1])
                dic['Fax No'] = ""
                dic['Address'] = replace(element.xpath('.//div[@class="value"]/span/text()')[2])
                dic['Validity'] = replace(element.xpath('.//div[@class="value"]/span/text()')[3])
                dic['Exchange Name'] = replace(element.xpath('.//div[@class="value"]/span/text()')[4])
                dic['Affiliated Broke'] = replace(element.xpath('.//div[@class="value"]/span/text()')[5])
                dic['Affiliated Broker Reg. No'] = replace(element.xpath('.//div[@class="value"]/span/text()')[6])
            elif len(table) == 8:
                dic['Registration No'] = replace(element.xpath('.//div[@class="value"]/span/text()')[0])
                dic['Telephone'] = replace(element.xpath('.//div[@class="value"]/span/text()')[1+i])
                dic['Fax No'] = el_fax
                dic['Address'] = replace(element.xpath('.//div[@class="value"]/span/text()')[3])
                dic['Validity'] = replace(element.xpath('.//div[@class="value"]/span/text()')[4])
                dic['Exchange Name'] = replace(element.xpath('.//div[@class="value"]/span/text()')[5])
                dic['Affiliated Broke'] = replace(element.xpath('.//div[@class="value"]/span/text()')[6])
                dic['Affiliated Broker Reg. No'] = replace(element.xpath('.//div[@class="value"]/span/text()')[7])
        except IndexError as e:
            print('line=', n ,'...', e)
        list_data.append(dic)
    print(list_data)
    #write_svc(list_data)

    global All_list_data
    All_list_data = All_list_data + list_data
    #return list_element

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
        #html = driver.page_source
        #parse_url(html)
        return driver


def get_htmlN(n,N,driver):
    n_ = n
    N_ = N
    driver_ = driver
    next_page_link(driver, n_)
    time.sleep(14)
    html = driver.page_source
    #time.sleep(3)
    parse_url(html, n_)
    n_=n_+1
    if n < N:
        get_htmlN(n_, N_, driver_)


def get_count_page(driver):
    element_li = driver.find_element_by_xpath('//li[@class=""]/a')
    result = re.findall(r'\d', element_li.get_attribute('href'))
    coun = int(''.join(result))
    return coun

from threading import Thread
def main():

    time1 = time.time()
    driver1 = Web_Driver().get_html()
    #get_htmlN(0,0,driver1)
    coun = get_count_page(driver1)
    print(coun)
    driver2 = Web_Driver().get_html()
    driver3 = Web_Driver().get_html()
    driver4 = Web_Driver().get_html()
    driver5 = Web_Driver().get_html()
    driver6 = Web_Driver().get_html()
    driver7 = Web_Driver().get_html()
    driver8 = Web_Driver().get_html()
    driver9 = Web_Driver().get_html()
    driver10 = Web_Driver().get_html()
    driver11 = Web_Driver().get_html()
    #et_htmlN(1, 400, driver1)
    t1 = Thread(target=get_htmlN, args=(0,100, driver1))
    t2 = Thread(target=get_htmlN, args=(101,200, driver2))
    t3 = Thread(target=get_htmlN, args=(201, 300, driver3))
    t4 = Thread(target=get_htmlN, args=(301, 400, driver4))
    t5 = Thread(target=get_htmlN, args=(401, 500, driver5))
    t6 = Thread(target=get_htmlN, args=(501, 600, driver6))
    t7 = Thread(target=get_htmlN, args=(601, 700, driver7))
    t8 = Thread(target=get_htmlN, args=(701, 800, driver8))
    t9 = Thread(target=get_htmlN, args=(801, 900, driver9))
    t10 = Thread(target=get_htmlN, args=(901, 1000, driver10))
    t11 = Thread(target=get_htmlN, args=(1001, coun, driver11))

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()

    global All_list_data
    write_svc(All_list_data)

    time2 = time.time()
    #cler_file("Data.csv")
    print(time2 - time1)


if __name__ == '__main__':
    main()


