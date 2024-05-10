# uses chromedriver in headless fashion with selenium to get a table from a HTML with javascript website

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Open the webpage
url = 'https://app.extrafi.io/farm'
driver.get(url)

# Wait for dynamic content to load (adjust the wait time as needed)
print("waiting for 5sec for javascript content to load ...")
driver.implicitly_wait(5)  # Wait for up to 5 seconds

# Print the entire HTML content of the webpage
print(driver.page_source)
print("--------------------------------------------------------------------------------")

# Once the content is loaded, you can extract data using Selenium's find methods
# For example:
#element = driver.find_element_by_xpath('//div[@class="your-class"]')
#print(element.text)

# Find all elements within the table using CSS selector
#table_we = driver.find_element(By.XPATH, '//*[@id="ant-table-content"]')
#print(table_we.text)

table_we = driver.find_element(By.CLASS_NAME, "ant-table-content")
table_text = driver.find_element(By.CLASS_NAME, "ant-table-content").text
print(table_text)


# After you've finished scraping, close the driver
driver.quit()

