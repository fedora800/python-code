import logging
# import sys
import time
import pandas

#from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


LOGGING_FORMAT = '%(asctime)s - [%(levelname)s] - [%(process)d:%(thread)d] - %(name)s:%(filename)s:%(funcName)s:%(lineno)d — %(message)s'
# logging.basicConfig(filename='example.log', filemode='w', format=LOGGING_FORMAT, level=logging.DEBUG)
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
#logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)

mylogger = logging.getLogger(__name__)


# allow to search using parameters
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# allows to specify what we expect to see to allow us to check if web page
# has loaded
# from selenium.webdriver.support import expected_conditions as EC
# allows for the web browser to load
# from selenium.webdriver.support.ui import WebDriverWait


# from selenium.common.exceptions import TimeoutException     # to handle
# exceptions

# # ## this is for firefox
# # binary = FirefoxBinary(r'C:\Users\sshinde\AppData\Local\Mozilla Firefox\firefox.exe')
# # # https://github.com/mozilla/geckodriver/releases
# # browser = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\python_others\geckodriver.exe')
# # browser.get(my_url)
# # browser.quit()
#
# # inspect the field in chrome and click on copy xpath to get info
# username_input = '//*[@id="usernameId"]'
# password_input = '//*[@id="wrapper"]/main/section/form/input[2]'
# login_submit = '//*[@id="wrapper"]/main/section/form/input[3]'
#
# # Enter username
# # x = browser.
# # (By.ID("username")).sendKeys("productsupportlondon@liquidnet.com");
#
# # Enter password
# browser.findElement(By.ID("passwd")).sendKeys("!Liquidnet.123!")
#
# # submit form
# browser.findElement(By.ID("password")).submit()
#
# browser.find_element(By.XPATH, username_input).send_keys(my_user_id)
# browser.find_element(By.XPATH, password_input).send_keys(my_password)
# browser.find_element(By.XPATH, login_submit).click()

# we might have to do exception handling here, but if no errors means we
# are now logged in and on the ISIN search screen


def fca_firds_lookup_isin(browser, isin):
    """
    in this function, we input ISIN and click on search button
    """

    mylogger.info("Looking up for ISIN : %s", isin)

    # if there is a browser popup to accept cookies, we need to handle it
    time.sleep(1)
    # click on 'Yes, I agree'
    browser.find_element(
        By.XPATH, '//*[@id="sliding-popup"]/div/div/div[2]/button[1]').click()
    print('Popup check done ...')
    time.sleep(1)

    # inspect the 'Instrument identification code' field
    instrument_identification_code_input = '//*[@id="isin"]'
    browser.find_element(
        By.XPATH, instrument_identification_code_input).clear()
    # Additional info if this solution of clear() doesn't work for someone: make sure that element.GetAttribute("value") really
    # has a value before calling element.clear() (wait for this value to be non empty)
    # also driver.get_element_by_id('foo').clear_field()
    # or driver.find_element_by_id('abc').clear();
    browser.find_element(
        By.XPATH, instrument_identification_code_input).send_keys(isin)
    time.sleep(1)
    # click search button
    search_button = '//*[@id="form1"]/div/div[14]/input[1]'
    browser.find_element(By.XPATH, search_button).click()
    time.sleep(1)


def get_table_data(browser):
    """
    in this function, we extract all the records from the table of data and print them
    """

    mylogger.debug('Fetching records ...')
    # locate the table and put it into a WebElement
    #table_we = browser.find_element(By.XPATH, '//*[@id="table"]')

    bs = BeautifulSoup(browser.page_source, features="lxml")
    
    # Verifying tables and their classes
    print('---1------------         Classes of each table:')
    for table in bs.find_all("table"):
        #print(table)
        print(table.get("class"))

    print('---2------------         soup_table')
    soup_table = bs.find("table")
    #print('contents = ', soup_table.contents)
    #print('attributes = ', soup_table.attrs)
    list_dfs = pandas.read_html(str(soup_table))
    #print(df_table.info(), df_table.size(), df_table.shape[0], df_table.shape[1])
    #print(df_table)
    #print('length of list_dfs = ', len(list_dfs))
    print('---3------------         df_table')
    df_table = list_dfs[0]
    print('df object of the table we needed =', df_table)

    # check and click on next page/subpage button to fetch more data
    print('---4------------         next button')
    browser.find_element(By.XPATH, '//*[@id="panel"]/div[4]/div[1]/ul/li[10]/a').click()            # worked
    print('---5------------         after the click')
    time.sleep(3)

    bs = BeautifulSoup(browser.page_source, features="lxml")
    print('---11------------         Classes of each table:')
    for table in bs.find_all("table"):
        #print(table)
        print(table.get("class"))

    print('---22------------         soup_table')
    soup_table = bs.find("table")
    #print('contents = ', soup_table.contents)
    #print('attributes = ', soup_table.attrs)
    list_dfs = pandas.read_html(str(soup_table))
    #print(df_table.info(), df_table.size(), df_table.shape[0], df_table.shape[1])
    #print(df_table)
    #print('length of list_dfs = ', len(list_dfs))
    print('---33------------         df_table')
    df_table = list_dfs[0]
    print('df object of the table we needed =', df_table)

    # check and click on next page/subpage button to fetch more data
    print('---44------------         next button')
    browser.find_element(By.XPATH, '//*[@id="panel"]/div[4]/div[1]/ul/li[10]/a').click()            # worked



"""
while True:
    try :
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='poststop' and @name='poststop']//following::table[1]//li[@class='prevnext']/a[contains(.,'Next')]"))).click()
    except :
        print("No more pages left")
        break
"""


    # --- this is another way to get table data, but beautiful soup might be better -- start x151 ----
""" num_rows = len(browser.find_element(By.XPATH, '//*[@id="table"]/tbody/tr'))
    num_cols = len(browser.find_element(
        By.XPATH, '//*[@id="table"]/tbody/tr[2]/td'))
    print('TEST --- rows=', num_rows, '  columns=', num_cols)
    print('---test---1 end  ----')    
    #row_count = len(table_we.find_elements_by_tag_name('tr')) - 1
    row_count = len(table_we.find_element(By.TAG_NAME, 'tr')) - 1
    # td HTML tags are used to form the cells
    # use XPath //tr[2]/td to find the number of columns, If we use //tr[1] then we may need to use th HTML tags
    # as tr[1]point to headers and header will not have the td tags.
    col_count = len(table_we.find_element(By.XPATH, '//tr[2]/td'))

#    print('rows=', row_count, '  columns=', col_count)
    mylogger.info("rows=%s, columns=%s", row_count, col_count)

    # iterate over the rows, to ignore the headers we have started the i with
    # '1'
    list_tabledata = []
    # make sure to test the ranges for rows and columns
    for i in range(1, row_count + 1):
        row_list = []    # reset the row data every time
        # iterate over columns
        for j in range(1, col_count):
            # get text from the i th row and j th column
            print("//tr[" + str(i) + "]/td[" + str(j) + "]")
            row_list.append(table_we.find_element(By.XPATH,
                                                  "//tr[" + str(i) + "]/td[" + str(j) + "]").text)
        # add the row data to the main table list
        list_tabledata.append(row_list) 

    for x in range(len(list_tabledata)):
        # mylogger.debug(list_tabledata[x])
        mylogger.info(list_tabledata[x]) """
    # ------------------------ end x151 -----------------


    #next_button = '//*[@id="form1"]/div/div[14]/input[1]'
    #browser.find_element(By.XPATH, search_button).click()


def search_for_next_button(browser):
    """
    once the ISIN lookup retrieves data, it only shows 10 rows at a time.
    we need to click on the 'Next' button to get the next 10 rows.
    this function will identify if there is a next button on the page or not
    """





def sort_table_by_oldest_admission_date(browser):
    """
    now sort the table by oldest date of admission to trading, oldest will be 1st row
    """
    # table_we = browser.find_element(By.XPATH, '//*[@id="T01"]')
    # sort_click = '//*[@id="mrkt_trdng_start_date"]/a'
    # browser.find_element(By.XPATH, sort_click).click()
    mylogger.info(
        'No sorting required, this FCA FIRDS table is already sorted by ISINs with oldest admission date at top')
    time.sleep(1)


def get_oldest_admission_record(browser):
    """
    will click on the 'More Info' link on the 8th column of 1st row of the sorted output to get a page with all the details for that (ie oldest) VENUE
    and then fetch the various required values like maturity date etc from the new page that is opened
    """
    first_more_info_click = '//*[@id="T01"]/tbody/tr[1]/td[8]/a'
    browser.find_element(By.XPATH, first_more_info_click).click()
    time.sleep(1)
    # new page will load with the details of that record
    # get the 'Trading Venue' and the 'Maturity Date' and any fields as
    # required
    found_isin_xpath = '//*[@id="detailsParent"]/tbody/tr[1]/td[2]'
    found_isin = browser.find_element(By.XPATH, found_isin_xpath)
    mylogger.debug(found_isin.text)
    found_cfi_code_xpath = '//*[@id="detailsParent"]/tbody/tr[3]/td[2]'
    found_cfi_code = browser.find_element(By.XPATH, found_cfi_code_xpath)
    mylogger.debug(found_cfi_code.text)
    trading_venue_xpath = '//*[@id="detailsParent"]/tbody/tr[6]/td[2]'
    trading_venue = browser.find_element(By.XPATH, trading_venue_xpath)
    mylogger.debug(trading_venue.text)
    date_of_admission_xpath = '//*[@id="detailsParent"]/tbody/tr[9]/td[2]'
    date_of_admission = browser.find_element(By.XPATH, date_of_admission_xpath)
    mylogger.debug(date_of_admission.text)
    mylogger.info(
        "RECORD WITH OLDEST ADMISSION : ISIN=%s, CFI_CODE=%s, Venue=%s, AdmissionDate=%s", found_isin.text, found_cfi_code.text, trading_venue.text, date_of_admission.text)


def main():
    my_url = 'https://data.fca.org.uk/#/viewdata'
    isin_not_found_text = "No search results found"
    list_isins = [
        'XS2288824969'
    ]

    # this is for google chrome
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_svc = Service('C:/myapps/python_drivers/chromedriver.exe')
    browser = webdriver.Chrome(options=options, service=chrome_svc)
    browser.get(my_url)
    
    # browser.maximize_window()

    for x in range(len(list_isins)):
        fca_firds_lookup_isin(browser, list_isins[x])
        # handle if the ISIN does not exists and we get below mesg on the page
        # ======================================================================
        #
        # # this is not working ....
        # if (isin_not_found_text in browser.page_source):
        #     print('There was no data found for ISIN ',
        #           list_isins[x], ' so going to next lookup ...')
        # else:
        #     sort_table_by_oldest_admission_date(browser)
        #     get_table_data(browser)
        #     get_oldest_admission_record(browser)
        #     browser.back()
        #     time.sleep(1)
        # ======================================================================

    sort_table_by_oldest_admission_date(browser)
    time.sleep(3)
    get_table_data(browser)
    get_oldest_admission_record(browser)
    browser.back()
    time.sleep(1)

    # just wait for some time before script terminates and browser exits
    mylogger.info(
        'Waiting 15 seconds before terminting browser and exiting ...')
    time.sleep(15)
    mylogger.info('Exiting script.')


# --- main ---
if __name__ == '__main__':
    #    main(sys.argv)
    main()


# browser.quit()

# https://chercher.tech/python/table-selenium-python        for getting html table data
# https://www.softwaretestinghelp.com/efficient-selenium-scripting-selenium-tutorial-27/
# https://www.techbeamers.com/locate-elements-selenium-python/
