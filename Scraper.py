from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

PATH = "C:\\Program Files (x86)\\chromedriver.exe"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--log-level=3')

# Initialize the service object
service = Service(PATH)

# Initialize the webdriver with the service
driver = webdriver.Chrome(service=service)


# Open the target website
driver.get("https://www.dnb.com/de-de/upik.html?new=1")

# Wait until the dropdown and search box elements are present
wait = WebDriverWait(driver, 15)
try:
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "country")))
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[class*='searchUpikInputBox']")))
except:
    print("Error in locating dropdown or search box")
    driver.quit()

try:
    # Select an option from the dropdown menu
    select = Select(dropdown)
    select.select_by_value("US")
    # Type into the search box
    search_box.send_keys("FedEx")
    # Submit the search form (if there is a specific button to submit the form)
    search_box.send_keys(Keys.RETURN)
except:
    print("Error in selecting dropdown or typing into search box")
    driver.quit()

# Optionally, wait for the results to load and perform further actions
try:
    result = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'upik-search-result-paper')]")))
    result_cards = result.find_elements(By.XPATH, "//div[contains(@class, 'upik-search-result-item-card')]")
    duns_numbers = {}
    for card in result_cards:
        company = card.find_element(By.XPATH, ".//a[contains(@class, 'company-title')]")
        details = card.find_element(By.XPATH, ".//div[contains(@class, 'detail')]")
        details_list = details.text.split(':')
        number = details_list[1].strip()
        duns_numbers[company.text] = number
except:
    print("Error in locating result cards")
    driver.quit()
# Close the browser
print(duns_numbers)
print(len(duns_numbers))
driver.quit()
