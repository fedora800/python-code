
import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox import firefox_binary
from msilib import Binary
#from bs4 import BeautifulSoup as bs

sys.path.append('C:\\python_others')
print(sys.path)


my_url='https://registers.esma.europa.eu/publication/searchRegister?core=esma_registers_firds'

# Create a new instance of the Firefox browser and provide the path of the binary browser file
#path = 'C:\\python_others\\geckodriver'
#binary = FirefoxBinary('path/to/installed firefox binary')
#browser = webdriver.Firefox()
browser = webdriver.Firefox(executable_path='C:\python_others\geckodriver.exe')

# go to web page specified
#browser.get(my_url)
browser.get('http://inventwithpython.com')       # test

# the page is ajaxy so the title is originally this:
print(browser.title)
# gets the html output of the entire page
html_output = browser.page_source
print(html_output)

browser.close()
browser.quit()

'''

from selenium import webdriver
browser = webdriver.Firefox(executable_path=r'your\path\geckodriver.exe')
browser.get('http://inventwithpython.com')

self.browser = webdriver.Firefox(executable_path = 'D:\Selenium_RiponAlWasim\geckodriver-v0.18.0-win64\geckodriver.exe')


============
browser = webdriver.Firefox()
browser.get("http://somedomain/url_that_delays_loading")
    try:
        element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))) #waits 10 seconds until element is located. Can have other wait conditions  such as visibility_of_element_located or text_to_be_present_in_element

        html = browser.page_source
        soup = bs(html, "lxml")
        dynamic_text = soup.find_all("p", {"class":"class_name"}) #or other attributes, optional
    else:
        print("Couldnt locate element")


====================



# find the element that's name attribute is q (the google search box)
inputElement = browser.find_element_by_name("q")

# type in the search
inputElement.send_keys("cheese!")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

try:
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    WebDriverWait(browser, 10).until(EC.title_contains("cheese!"))

    # You should see "cheese! - Google Search"
    print browser.title

finally:
    browser.quit()        
    
'''    