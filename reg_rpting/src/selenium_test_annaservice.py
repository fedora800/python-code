from asyncio.tasks import sleep
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd


# allow to search using parameters
# allows to specify what we expect to see to allow us to check if web page
# has loaded
# allows for the web driver to load
# from selenium.common.exceptions import TimeoutException     # to handle exceptions
# my_url='http://google.com/'
#my_url = 'https://www.annaservice.com/anna/annaisin/login.jsp'
my_url = 'https://www.annaservice.com/isinlookup/login'
my_user_id = 'productsupportlondon@liquidnet.com'
my_password = '!Liquidnet.123!'
my_isin = 'US1714392016'

# ## this is for firefox
# binary = FirefoxBinary(r'C:\Users\sshinde\AppData\Local\Mozilla Firefox\firefox.exe')
# # https://github.com/mozilla/geckodriver/releases
# browser = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\python_others\geckodriver.exe')
# browser.get(my_url)
# browser.quit()


def get_table_data(browser):
    """
    in this function, we extract all the records from the table of data and print them 
    """

    print('Fetching records ...')
    # locate the table and put it into a WebElement
    table_we = browser.find_element_by_xpath('//*[@id="isinDetailTable"]')

    row_count = len(table_we.find_elements_by_tag_name('tr'))
    # td HTML tags are used to form the cells
    # use XPath //tr[2]/td to find the number of columns, If we use //tr[1] then we may need to use th HTML tags
    # as tr[1]point to headers and header will not have the td tags.
    col_count = len(table_we.find_elements_by_xpath('//tr[2]/td'))

    print('rows=', row_count, '  columns=', col_count)
    # print(table_we.find_element_by_xpath('//tr[2]/td[3]').text)

    # iterate over the rows, to ignore the headers we have started the i with
    # '1'
    list_tabledata = []
    # make sure to test the ranges for rows & columns, causes problems many
    # times
    # we do not want the 1st row as it's the header, and +1 will make it enter
    # the loop
    for i in range(2, row_count + 1):
        row_list = []    # reset the row data every time
        # iterate over columns
        for j in range(1, col_count + 1):
            #             # get text from the i th row and j th column
            #             print('i=', i, ' j=', j, '---lookup xpath=',
            #                   "//tr[" + str(i) + "]/td[" + str(j) + "]")
            #             print(table_we.find_element_by_xpath(
            #                 "//tr[" + str(i) + "]/td[" + str(j) + "]").text)
            row_list.append(table_we.find_element_by_xpath(
                "//tr[" + str(i) + "]/td[" + str(j) + "]").text)
        # add data extracted for this row to the main table list
        list_tabledata.append(row_list)

    print('Table data :')
    for row in range(len(list_tabledata)):
        print('Row ', row, '= ', list_tabledata[row])

    output_isin = list_tabledata[0][1]
    output_cficode = list_tabledata[0][8]
    output_maturitydate = list_tabledata[0][6]
    # if no maturity date provided on the site, they will put P or Q or null
    # in the field
    if list_tabledata[0][6] not in ['P', 'Q', '']:
        output_maturitydate = datetime.strptime(
            output_maturitydate, '%m/%d/%Y').strftime('%Y-%m-%d')
    print('*** MY_OUTPUT=, ' + output_isin + ', ' +
          output_cficode + ',  ' + output_maturitydate)


def fetch_isin_details(isin_to_fetch):

    print('At SEARCH ISIN page. Submitting ISIN: ', isin_to_fetch)
    isin_input = '//*[@id="isinValue"]'
    browser.find_element_by_xpath(isin_input).clear()
    browser.find_element_by_xpath(isin_input).send_keys(isin_to_fetch)

    # SEARCH button
    isin_submit = '//*[@id="wrapper"]/main/section/form/center/input'
    browser.find_element_by_xpath(isin_submit).click()

    print('At SEARCH RESULT page...')
    print('Checking if any results found ...')
    print('Current Page URL : ', browser.current_url)

#    browser.find_element_by_xpath("// a[contains(text(),'No result found.')]")
    if 'No result found.' in browser.page_source:
        # text exists in page
        print('NO RESULTS WERE FOUND, going back 1 page now ...')
        # browser.execute_script("window.history.go(-1)")    # this is for
        # javascript
        print('*** MY_OUTPUT=, ' + isin_to_fetch + ', NO RESULTS FOUND')
        browser.back()
    else:
        print('Some results have been found, continuing ...')

        print('Now Selecting the 1st row link ')
        browser.find_element_by_xpath(
            '//*[@id="isinRecordsTable"]/tr/td[1]/a').click()

        print('At SEARCH DETAILS page. Extracting the fields ...')
        # now access and print the table data
        time.sleep(1)

        # # get number of rows of the table
        # num_rows = len(browser.find_elements_by_xpath(
        #     '//*[@id="isinDetailTable"]/tbody/tr'))
        # # print(num_rows)
        # # get number of columns
        # num_cols = len(browser.find_elements_by_xpath(
        #     '//*[@id="isinDetailTable"]/tbody/tr[2]/td'))
        # # print(num_cols)
        # print('Rows=', num_rows, ' and Columns=', num_cols)
        #
        # num_cols = len(browser.find_elements_by_xpath(
        #     '//*[@id="isinDetailTable"]/tbody/tr/td'))
        # print(num_cols)

        get_table_data(browser)
        browser.find_element_by_xpath(SEARCH_AGAIN_BUTTON).click()

    print('COMPLETED search for ISIN - ', isin_to_fetch)
    print('Current Page URL after going back 1 page: ', browser.current_url)
    time.sleep(1)


# --- main ---
# this is for google chrome browser
#browser = webdriver.Chrome(executable_path=r'C:\python_drivers\chromedriver.exe')
#browser.get(my_url)

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_svc = Service('C:/python_drivers/chromedriver.exe')
browser = webdriver.Chrome(options=options, service=chrome_svc)
browser.get(my_url)
    


# inspect the field in chrome and click on copy xpath to get info
""" stopped working 11-nov-2021
USERNAME_INPUT = '//*[@id="usernameId"]'
PASSWORD_INPUT = '//*[@id="wrapper"]/main/section/form/input[2]'
LOGIN_SUBMIT = '//*[@id="wrapper"]/main/section/form/input[3]'
SEARCH_AGAIN_BUTTON = '//*[@id="wrapper"]/main/section/div/center/table/tbody/tr/td/div/center/form/input'
"""
USERNAME_INPUT = '//*[@id="username"]'
PASSWORD_INPUT = '//*[@id="password"]'
LOGIN_SUBMIT = '//*[@id="wrapper"]/main/section/form/font/font/input[3]'
ISIN_SEARCH_DETAILS_TABLE = '//*[@id="isinDetailTable"]'
# SEARCH AGAIN button
SEARCH_AGAIN_BUTTON = '//*[@id="wrapper"]/main/section/div/center/table/tbody/tr/td/div/center/form/input[2]'

"""
# Enter username
#x = browser. (By.ID("username")).sendKeys("productsupportlondon@liquidnet.com");

# Enter password
browser.findElement(By.ID("passwd")).sendKeys("!Liquidnet.123!");

# submit form
browser.findElement(By.ID("password")).submit();

"""
# if there is a browser popup to accept cookies, we need to handle it
time.sleep(1)
# browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
print('Popup check is commented out ...')
time.sleep(1)


# input userid, password and click submit
print('Inputting userid and password ...')
browser.find_element_by_xpath(USERNAME_INPUT).send_keys(my_user_id)
browser.find_element_by_xpath(PASSWORD_INPUT).send_keys(my_password)
browser.find_element_by_xpath(LOGIN_SUBMIT).click()

# we might have to do exception handling here, but if no errors means we
# are now logged in and on the ISIN search screen
# sleep for suitable amount of time (seconds) as otherwise the find
# element will get details from the old page
time.sleep(1)

# we are now at the page where it shows all the issuers for the ISIN we
# input above, and we need to click on the link of the company we need to
# get details about
time.sleep(1)

isins_list = [
'GB00BFXW0630',
'PTAVBAOT0003',
'USP32466AA50',
'USP79171AF45',
'USP9485MAC30',
'XS0800185174',
'XS1879603717',
'XS1910828182',
'XS1910867081',
'XS2022203801',
'XS2226898216',
'XS2307633565',
'XS2339102878',
'XS2454288122',
'XS2527432277'
]

num_isins = len(isins_list)
for i in range(num_isins):
    print('-----index=', i, ' of ', num_isins - 1, '----')
    isin_to_lookup = isins_list[i]
    fetch_isin_details(isin_to_lookup)


time.sleep(3)
print('NOW EXITING ...')

browser.quit()
