import logging
# import sys
import time

from selenium import webdriver


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
# browser.find_element_by_xpath(username_input).send_keys(my_user_id)
# browser.find_element_by_xpath(password_input).send_keys(my_password)
# browser.find_element_by_xpath(login_submit).click()

# we might have to do exception handling here, but if no errors means we
# are now logged in and on the ISIN search screen


def fca_firds_lookup_isin(browser, isin):
    """
    in this function, we input ISIN and click on search button
    """

    mylogger.info("Looking up for ISIN : %s", isin)
    # inspect the 'Instrument identification code' field
    instrument_identification_code_input = '//*[@id="searchFields"]/div[1]/div/input'
    browser.find_element_by_xpath(instrument_identification_code_input).clear()
    # Additional info if this solution of clear() doesn't work for someone: make sure that element.GetAttribute("value") really
    # has a value before calling element.clear() (wait for this value to be non empty)
    # also driver.get_element_by_id('foo').clear_field()
    # or driver.find_element_by_id('abc').clear();
    browser.find_element_by_xpath(
        instrument_identification_code_input).send_keys(isin)
    time.sleep(1)
    # click search button
    search_button = '//*[@id="searchSolrButton"]'
    browser.find_element_by_xpath(search_button).click()
    time.sleep(1)


def get_table_data(browser):
    """
    in this function, we extract all the records from the table of data and print them
    """

    mylogger.debug('Fetching records ...')
    # locate the table and put it into a WebElement
    table_we = browser.find_element_by_xpath('//*[@id="T01"]')

    row_count = len(table_we.find_elements_by_tag_name('tr')) - 1
    # td HTML tags are used to form the cells
    # use XPath //tr[2]/td to find the number of columns, If we use //tr[1] then we may need to use th HTML tags
    # as tr[1]point to headers and header will not have the td tags.
    col_count = len(table_we.find_elements_by_xpath('//tr[2]/td'))

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
            # print("//tr["+str(i)+"]/td["+str(j)+"]")
            row_list.append(table_we.find_element_by_xpath(
                "//tr[" + str(i) + "]/td[" + str(j) + "]").text)
        # add the row data to the main table list
        list_tabledata.append(row_list)

    for x in range(len(list_tabledata)):
        # mylogger.debug(list_tabledata[x])
        mylogger.info(list_tabledata[x])


def sort_table_by_oldest_admission_date(browser):
    """
    now sort the table by oldest date of admission to trading, oldest will be 1st row
    """
    # table_we = browser.find_element_by_xpath('//*[@id="T01"]')
    sort_click = '//*[@id="mrkt_trdng_start_date"]/a'
    browser.find_element_by_xpath(sort_click).click()
    time.sleep(1)


def get_oldest_admission_record(browser):
    """
    will click on the 'More Info' link on the 8th column of 1st row of the sorted output to get a page with all the details for that (ie oldest) VENUE
    and then fetch the various required values like maturity date etc from the new page that is opened
    """
    first_more_info_click = '//*[@id="T01"]/tbody/tr[1]/td[8]/a'
    browser.find_element_by_xpath(first_more_info_click).click()
    time.sleep(1)
    # new page will load with the details of that record
    # get the 'Trading Venue' and the 'Maturity Date' and any fields as
    # required
    found_isin_xpath = '//*[@id="detailsParent"]/tbody/tr[1]/td[2]'
    found_isin = browser.find_element_by_xpath(found_isin_xpath)
    mylogger.debug(found_isin.text)
    found_cfi_code_xpath = '//*[@id="detailsParent"]/tbody/tr[3]/td[2]'
    found_cfi_code = browser.find_element_by_xpath(found_cfi_code_xpath)
    mylogger.debug(found_cfi_code.text)
    trading_venue_xpath = '//*[@id="detailsParent"]/tbody/tr[6]/td[2]'
    trading_venue = browser.find_element_by_xpath(trading_venue_xpath)
    mylogger.debug(trading_venue.text)
    date_of_admission_xpath = '//*[@id="detailsParent"]/tbody/tr[9]/td[2]'
    date_of_admission = browser.find_element_by_xpath(date_of_admission_xpath)
    mylogger.debug(date_of_admission.text)
    mylogger.info(
        "RECORD WITH OLDEST ADMISSION : ISIN=%s, CFI_CODE=%s, Venue=%s, AdmissionDate=%s", found_isin.text, found_cfi_code.text, trading_venue.text, date_of_admission.text)


def main():
    my_url = 'https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_firds'
    isin_not_found_text = "No data found"
    list_isins = [
'IE00BF541080',
'NL0009265404',
'NL0009296649',
'NL0009693258',
'NL0009756394',
'NL0010278073',
'NL0010489373',
'NL0012044739',
'NL0012512958',
'NL0012817134',
'NL0013025539',
'NL0013087968'
    ]
    # this is for google chrome
    browser = webdriver.Chrome(
        executable_path=r'C:\python_others\chromedriver.exe')
    browser.get(my_url)


    num_isins = len(list_isins)
    for i in range(num_isins):
        print('-----index=', i, ' of ', num_isins - 1, '----')
        isin_to_lookup = list_isins[i]
        fca_firds_lookup_isin(browser, isin_to_lookup)
        # handle if the ISIN does not exists and we get below mesg on the page
        # this is not working ....
        if (isin_not_found_text in browser.page_source):
            sort_table_by_oldest_admission_date(browser)
            get_table_data(browser)
            get_oldest_admission_record(browser)
            browser.back()
            time.sleep(1)
        else:
            print('No data found for ISIN ', isin_to_lookup,
                  ' so going to next lookup ...')

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
