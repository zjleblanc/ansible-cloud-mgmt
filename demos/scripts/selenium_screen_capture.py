import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# run Chrome in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

# start a driver instance
driver = webdriver.Chrome(options=options)

# set the browser window size
driver.set_window_size(1500, 1000)

# Open the Python website
driver.get("https://www.python.org")
driver.implicitly_wait(2)

# Print the page title
print(driver.title)

# Find the search bar using its name attribute
search_bar = driver.find_element(By.NAME, "q")
search_bar.clear()
search_bar.send_keys("getting started with python")
search_button = driver.find_element(By.ID, "submit")
search_button.click()

# Print the current URL
full_body_element = driver.find_element(By.ID, "touchnav-wrapper")
full_body_element.screenshot(os.environ.get('SCREENSHOTS_DIR') + '/python_org_search.png')

# Close the browser window
driver.close()