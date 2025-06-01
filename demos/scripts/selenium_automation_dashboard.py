import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# run Chrome in headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--ignore-certificate-errors")
options.accept_insecure_certs = True

# start a driver instance
driver = webdriver.Chrome(options=options)

# set the browser window size
driver.set_window_size(1500, 1000)

try:
  admin_password = os.environ.get('ADMIN_PWD')
  driver.get(f"https://admin:{admin_password}@192.168.0.120:8447/")
  driver.implicitly_wait(2)
  WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "app")))
  app = driver.find_element(By.ID, "app")
  app.screenshot(os.environ.get('SCREENSHOTS_DIR') + '/automation_dashboard.png')
except Exception:
  sys.stderr.write("Automation dashboard failed to load")
  sys.exit(1)
finally:
    driver.close()
