from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from typing import Dict, List
import time


class Scraper:
    def __init__(self, company: str, country: str):
        self.PATH = "C:\\Program Files (x86)\\chromedriver.exe"
        self.company = company
        if (country is None):
            self.country = "US"
        else:
            self.country = country
    def scrape_all_results(self) -> Dict[str, List[str]]:
        # Setup dictionary to return
        duns_numbers = {}
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--log-level=3')

        # Initialize the service object
        service = Service(self.PATH)

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
            duns_numbers[self.company] = "N/A"
            return duns_numbers

        try:
            # Select an option from the dropdown menu
            select = Select(dropdown)
            select.select_by_value(self.country)
            # Type into the search box
            search_box.send_keys(self.company)
            # Submit the search form (if there is a specific button to submit the form)
            search_box.send_keys(Keys.RETURN)
        except:
            print("Error in selecting dropdown or typing into search box")
            driver.quit()
            duns_numbers[self.company] = "N/A"
            return duns_numbers

        # Optionally, wait for the results to load and perform further actions
        try:
            result = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'upik-search-result-paper')]")))
            result_cards = result.find_elements(By.XPATH, "//div[contains(@class, 'upik-search-result-item-card')]")
            if len(result_cards) > 0:
                for card in result_cards:
                    company = card.find_element(By.XPATH, ".//a[contains(@class, 'company-title')]")
                    details = card.find_element(By.XPATH, ".//div[contains(@class, 'detail')]")
                    address = card.find_element(By.XPATH, ".//p[contains(@class, 'paragraph')]")
                    details_list = details.text.split(':')
                    number = details_list[1].strip()
                    return_list = [number, address.text]
                    duns_numbers[company.text] = return_list
            else:
                print("No results found")
                duns_numbers[self.company] = "N/A"
        except:
            print("Error in locating result cards")
            driver.quit()
            duns_numbers[self.company] = "N/A"
            return duns_numbers
        # Close the browser
        print(duns_numbers)
        print(len(duns_numbers))
        driver.quit()

    def scrape_top_result(self) -> Dict[str, List[str]]:
        # Setup dictionary to return
        duns_numbers = {}
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--log-level=3')

        # Initialize the service object
        service = Service(self.PATH)

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
            duns_numbers[self.company] = "N/A"
            return duns_numbers

        try:
            # Select an option from the dropdown menu
            select = Select(dropdown)
            select.select_by_value(self.country)
            # Type into the search box
            search_box.send_keys(self.company)
            # Submit the search form (if there is a specific button to submit the form)
            search_box.send_keys(Keys.RETURN)
        except:
            print("Error in selecting dropdown or typing into search box")
            driver.quit()
            duns_numbers[self.company] = "N/A"
            return duns_numbers

        # Optionally, wait for the results to load and perform further actions
        try:
            result = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'upik-search-result-paper')]")))
            result_cards = result.find_elements(By.XPATH, "//div[contains(@class, 'upik-search-result-item-card')]")
            if len(result_cards) > 0:
                card = result_cards[0]
                company = card.find_element(By.XPATH, ".//a[contains(@class, 'company-title')]")
                details = card.find_element(By.XPATH, ".//div[contains(@class, 'detail')]")
                address = card.find_element(By.XPATH, ".//p[contains(@class, 'paragraph')]")
                details_list = details.text.split(':')
                number = details_list[1].strip()
                return_list = [number, address.text]
                duns_numbers[company.text] = return_list
            else:
                print("No results found")
                duns_numbers[self.company] = "N/A"
        except:
            print("Error in locating result cards")
            driver.quit()
            duns_numbers[self.company] = "N/A"
            return duns_numbers
        # Close the browser
        driver.quit()
        print(duns_numbers)
        return duns_numbers

if __name__=="__main__": 
    scraper_instance = Scraper(company="FedEx", country="US")
    scraper_instance.scrape_top_result()