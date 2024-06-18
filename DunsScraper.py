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

class DunsScraper:
    def __init__(self):
        self.PATH = "C:\\Program Files (x86)\\chromedriver.exe"

    '''RETURNS: Dict[str, List[str]]
    This method returns all the results from the search of the DUNS website.
    The key to the dictionary is a company name and the value is a list of two strings:
    The first string is the DUNS number and the second string is the address of the company.
    '''
    def scrape_all_results(self, company: str, country: str) -> Dict[str, List[str]]:
        # Check if the country is provided, if not, set it to US
        if (country is None):
            country = "US"
        else:
            country = country
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
            duns_numbers[company] = "N/A"
            return duns_numbers

        try:
            # Select a country option from the dropdown menu
            select = Select(dropdown)
            select.select_by_value(country)
            # Type into the search box the company name
            search_box.send_keys(company)
            # Submit the search form (if there is a specific button to submit the form)
            search_box.send_keys(Keys.RETURN)
        except:
            print("Error in selecting dropdown or typing into search box")
            driver.quit()
            duns_numbers[company] = "N/A"
            return duns_numbers

        # Wait for the results to load and perform further actions
        try:
            result = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'upik-search-result-paper')]")))
            # Retrieve the list of results
            result_cards = result.find_elements(By.XPATH, "//div[contains(@class, 'upik-search-result-item-card')]")
            # Check if there are any results
            if len(result_cards) > 0:
                # For each result, retrieve the DUNS, company name, and address and add it to the dictionary
                for card in result_cards:
                    result_company = card.find_element(By.XPATH, ".//a[contains(@class, 'company-title')]")
                    details = card.find_element(By.XPATH, ".//div[contains(@class, 'detail')]")
                    address = card.find_element(By.XPATH, ".//p[contains(@class, 'paragraph')]")
                    details_list = details.text.split(':')
                    number = details_list[1].strip()
                    return_list = [number, address.text]
                    duns_numbers[result_company.text] = return_list
            else:
                print("No results found")
                duns_numbers[company] = "N/A"
        except:
            print("Error in locating result cards")
            driver.quit()
            duns_numbers[company] = "N/A"
            return duns_numbers
        # Close the browser
        print(duns_numbers)
        print(len(duns_numbers))
        driver.quit()
        return duns_numbers

    '''RETURNS: Dict[str, List[str]]
    This method returns only the top result from the search of the DUNS website.
    The key to the dictionary is a company name and the value is a list of two strings:
    The first string is the DUNS number and the second string is the address of the company.
    '''
    def scrape_top_result(self, company: str, country: str) -> Dict[str, List[str]]:
        # Check if the country is provided, if not, set it to US
        if (country is None):
            country = "US"
        else:
            country = country
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
            duns_numbers[company] = "N/A"
            return duns_numbers

        try:
            # Select a country option from the dropdown menu
            select = Select(dropdown)
            select.select_by_value(country)
            # Type into the search box the company name
            search_box.send_keys(company)
            # Submit the search form (if there is a specific button to submit the form)
            search_box.send_keys(Keys.RETURN)
        except:
            print("Error in selecting dropdown or typing into search box")
            driver.quit()
            duns_numbers[company] = "N/A"
            return duns_numbers

        # Wait for the results to load and perform further actions
        try:
            result = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'upik-search-result-paper')]")))
            # Retrieve the list of results
            result_cards = result.find_elements(By.XPATH, "//div[contains(@class, 'upik-search-result-item-card')]")
            # Check if there is a result
            if len(result_cards) > 0:
                # For the first result only we process and return the DUNS, company name, and address and add it to the dictionary
                card = result_cards[0]
                result_company = card.find_element(By.XPATH, ".//a[contains(@class, 'company-title')]")
                details = card.find_element(By.XPATH, ".//div[contains(@class, 'detail')]")
                address = card.find_element(By.XPATH, ".//p[contains(@class, 'paragraph')]")
                details_list = details.text.split(':')
                number = details_list[1].strip()
                return_list = [number, address.text]
                duns_numbers[result_company.text] = return_list
            else:
                print("No results found")
                duns_numbers[company] = "N/A"
        except:
            print("Error in locating result cards")
            driver.quit()
            duns_numbers[company] = "N/A"
            return duns_numbers
        # Close the browser
        driver.quit()
        print(duns_numbers)
        return duns_numbers

if __name__=="__main__": 
    scraper_instance = DunsScraper()
    scraper_instance.scrape_top_result(company="FedEx", country="US")