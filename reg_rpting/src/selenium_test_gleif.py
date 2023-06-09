import sys
import time

from selenium import webdriver
# allow to search using parameters
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
# allows to specify what we expect to see to allow us to check if web page
# has loaded
from selenium.webdriver.support import expected_conditions as EC
# allows for the web browser to load
from selenium.webdriver.support.ui import WebDriverWait


# from selenium.common.exceptions import TimeoutException     # to handle
# exceptions
r"""
# ## this is for firefox
# binary = FirefoxBinary(r'C:\Users\sshinde\AppData\Local\Mozilla Firefox\firefox.exe')
# # https://github.com/mozilla/geckodriver/releases
# browser = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\python_others\geckodriver.exe')
# browser.get(my_url)
# browser.quit()

# inspect the field in chrome and click on copy xpath to get info
username_input = '//*[@id="usernameId"]'
password_input = '//*[@id="wrapper"]/main/section/form/input[2]'
login_submit = '//*[@id="wrapper"]/main/section/form/input[3]'

# Enter username
#x = browser. (By.ID("username")).sendKeys("productsupportlondon@liquidnet.com");

# Enter password
browser.findElement(By.ID("passwd")).sendKeys("!Liquidnet.123!");

# submit form
browser.findElement(By.ID("password")).submit();

browser.find_element_by_xpath(username_input).send_keys(my_user_id)
browser.find_element_by_xpath(password_input).send_keys(my_password)
browser.find_element_by_xpath(login_submit).click()

# we might have to do exception handling here, but if no errors means we are now logged in and on the ISIN search screen
"""


def gleif_lookup_LEI(browser, LEI):
    """
    in this function, we input LEI and click on search button 
    """

    print('Looking up for LEI : ', LEI)
    # inspect the 'Instrument identification code' field
    find_leis_input = '//*[@id="search"]'
    browser.find_element_by_xpath(find_leis_input).clear()
    browser.find_element_by_xpath(find_leis_input).send_keys(LEI)
    time.sleep(1)
    # click search button
    search_button = '//*[@id="search-form"]/div[2]/div[1]/div[3]/span/img'
    browser.find_element_by_xpath(search_button).click()
    time.sleep(1)


def traverse_records(rec_list):
    """
    in this function, list of href links are passed to the function and this will loop through them
    and fetch the data 
    """

    print('Looping through the records...')
    # for x in range(len(rec_list)):
    for x in rec_list:
        print(x)
        # eg x = https://search.gleif.org/#/record/549300EI2QZDOKF0UR93, open a
        # new browser with this link
        level1_browser = webdriver.Chrome(
            executable_path=r'C:\python_others\chromedriver.exe')
        level1_browser.get(x)
        time.sleep(5)
        print('--4--')
        # lookup the requisite fields from that LEI record page
        legal_name_xpath = '//*[@id="lei"]/main/div/div[1]/div[1]/section[1]/div/div[2]/div[1]/div/div[2]/p'
        entity_status_xpath = '//*[@id="lei"]/main/div/div[1]/div[1]/section[1]/div/div[2]/div[6]/div/div[2]/p/div'
        """
        last_update_xpath   = '//*[@id="lei"]/main/div/div[1]/div[1]/section[3]/div/div[2]/div[2]/div/div[2]/p'
        status_xpath        = '//*[@id="lei"]/main/div/div[1]/div[1]/section[3]/div/div[2]/div[3]/div/div[2]/p/div/text()' 
        """
        legal_name = level1_browser.find_element_by_xpath(
            legal_name_xpath).text

        x1 = level1_browser.find_element_by_class_name('lei-status')
        print(x1, '--val=', x1.text)
        #entity_status = level1_browser.find_element_by_xpath(entity_status_xpath).text
        """
        last_update   = level1_browser.find_element_by_xpath(last_update_xpath).text
        status        = level1_browser.find_element_by_xpath(status_xpath).text
        print('--values = ', legal_name, entity_status, last_update, status)
        """
        #print('--values = ', legal_name, entity_status)
        print(legal_name)
        print('sleeping for 5...')
        time.sleep(5)


def get_table_data(browser):
    """
    in this function, we extract all the records from the table of data and print them 
    """

    print('Fetching records ...')
    # locate the table and put it into a WebElement
    #table_we = browser.find_element_by_xpath('//*[@id="result-list"]')
    #table_we = browser.find_element_by_class_name('data-table')
    #table_we = browser.find_element_by_class_name('tbody')
    table_we = browser.find_element_by_xpath('//*[@id="tbody"]')
    print(table_we.text)

    print('---0---')
    # table_x1 = table_we.find_elements(By.CLASS_NAME, 'table-row')        # will return object having multiple elements matching the class name
    #table_x1 = browser.find_elements(By.CSS_SELECTOR, '//*[@id="tbody"]/a')
    #table_x1 = browser.find_elements(By.TAG_NAME , 'a href')
    #table_x1 = browser.find_elements_by_css_selector()
    # print(table_x1)
    # for x in range(len(table_x1)):
    #    print(table_x1[x])
    #    print(table_x1[x].text)

    # get the href record_links to the individual records from the above
    # driver subset
    elems = table_we.find_elements_by_css_selector("[href]")
    record_links = [elem.get_attribute('href') for elem in elems]
    print(record_links)

    traverse_records(record_links)

    """
    #table_y1 = table_x1.find_elements_by_tag_name('a')
    #table_y1 = browser.find_elements_by_class_name('table_row')     # not working ....
    table_y1 = table_we.find_elements_by_partial_link_text('record')
    for x in range(len(table_y1)):
        print('--4--') 
        print(table_y1[x])
        print(table_y1[x].text)

    print('---5---')
    elems = browser.find_elements_by_xpath('//*[@id="tbody"]')      # not working ...
    for elem in elems:
        print(elem.get_attribute("href"))
    
    print('---6---')
    row_count = len(table_we.find_elements_by_tag_name('table-row')) - 1
    # td HTML tags are used to form the cells
    # use XPath //tr[2]/td to find the number of columns, If we use //tr[1] then we may need to use th HTML tags 
    # as tr[1]point to headers and header will not have the td tags.
    col_count = len(table_we.find_elements_by_xpath('//tr[2]/td'))
    
    print('rows=', row_count, '  columns=', col_count)
    time.sleep(3)
    # iterate over the rows, to ignore the headers we have started the i with '1'
    list_tabledata = []
    # make sure to test the ranges for rows and columns
    for i in range(1, row_count+1):
        row_list = []    # reset the row data every time 
        # iterate over columns
        for j in range(1, col_count) :
            # get text from the i th row and j th column
            #print("//tr["+str(i)+"]/td["+str(j)+"]")
            row_list.append(table_we.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]").text)
        # add the row data to the main table list 
        list_tabledata.append(row_list)
    
    for x in range(len(list_tabledata)): 
        print(list_tabledata[x])
    
    """


def main(argv):
    my_url = 'https://search.gleif.org/#/search/'
    list_LEIs = ['US25256V1098']

    # this is for google chrome
    browser = webdriver.Chrome(
        executable_path=r'C:\python_others\chromedriver.exe')
    browser.get(my_url)

    for x in range(len(list_LEIs)):
        #print(x, list_LEIs[x])
        gleif_lookup_LEI(browser, list_LEIs[x])
        get_table_data(browser)
        """
        browser.back()
        time.sleep(1)
        """
        gleif_lookup_LEI(browser, list_LEIs[x])

    # just wait for some time before script terminates and browser exits
    time.sleep(15)
    print('Exiting script.')


# --- main ---
if __name__ == '__main__':
    main(sys.argv)


# browser.quit()

# https://chercher.tech/python/table-selenium-python        for getting html table data
# https://www.softwaretestinghelp.com/efficient-selenium-scripting-selenium-tutorial-27/
# https://www.techbeamers.com/locate-elements-selenium-python/
