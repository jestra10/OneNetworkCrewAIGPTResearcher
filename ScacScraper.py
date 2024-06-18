from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class ScacScraper:
    def __init__(self,):
        self.PATH = "C:\\Program Files (x86)\\chromedriver.exe"

    def scrape_all_results(self,  company: str) -> str:
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
        driver.get("https://scaccodelookup.com/scac-name-lookup/")

        # Wait until the submit button and search box elements are present
        wait = WebDriverWait(driver, 15)
        try:
            search_box = wait.until(EC.presence_of_element_located((By.ID, "namet")))
            submit_button = wait.until(EC.presence_of_element_located((By.ID, "sub")))
        except:
            print("Error in locating submit button or search box")
            driver.quit()
            scac_code = "N/A"
            return scac_code

        try:
            # Type into the search box the company name
            search_box.send_keys(company)
            # Submit the search form (if there is a specific button to submit the form)
            submit_button.send_keys(Keys.RETURN)
        except:
            print("Error in selecting dropdown or typing into search box")
            driver.quit()
            scac_code = "N/A"
            return scac_code
        
        # Wait for the page containing results to load
        time.sleep(2)
        try:
            # Wait until the element containing results loads in
            result_module = wait.until(EC.presence_of_element_located((By.ID, "primary")))
            results = result_module.find_element(By.CLASS_NAME, "paragraph")
            # Parse and retrieve the SCAC code from the results
            result_array = results.text.splitlines()
            # Check if the result array has a valid result. If it doesn't return 'N/A'
            if len(result_array) < 3:
                scac_code = "N/A"
                return scac_code
            else:
                # Retrieve and parse the SCAC code from the result
                scac_code = result_array[2].split(":")[1].strip()
                # Commented code right below this sentence can be used to retrieve the company name from the result 
                # as wont be same as the company name inputted.
                # result_company = result_array[3].split(":")[1].strip()
                print(scac_code)
        except:
            print("Error in locating results")
            driver.quit()
            scac_code = "N/A"
            return scac_code
        driver.quit()
        return scac_code

    def check_results(self, code: str) -> str:
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
        driver.get("https://scaccodelookup.com/scac-code-lookup/#")

        # Wait until the submit button and search box elements are present
        wait = WebDriverWait(driver, 15)
        try:
            search_box = wait.until(EC.presence_of_element_located((By.ID, "code")))
            submit_button = wait.until(EC.presence_of_element_located((By.ID, "sub")))
        except:
            print("Error in locating submit button or search box")
            driver.quit()
            result_company = "N/A"
            return result_company

        try:
            # Type into the search box the code
            search_box.send_keys(code)
            # Submit the search form (if there is a specific button to submit the form)
            submit_button.send_keys(Keys.RETURN)
        except:
            print("Error in selecting dropdown or typing into search box")
            driver.quit()
            result_company = "N/A"
            return result_company
        
        # Wait for the page containing results to load
        time.sleep(2)
        try:
            # Wait until the element containing results loads in
            result_module = wait.until(EC.presence_of_element_located((By.ID, "primary")))
            results = result_module.find_element(By.CLASS_NAME, "paragraph")
            # Parse and retrieve the company name from the results
            result_array = results.text.splitlines()
            # Check if the result array has a valid result. If it doesn't return 'N/A'
            if len(result_array) < 3:
                result_company = "N/A"
                print(result_company)
                return result_company
            else:
                # Retrieve and parse the company name from the result
                result_company = result_array[3].split(":")[1].strip()
                print(result_company)
        except:
            print("Error in locating results")
            driver.quit()
            result_company = "N/A"
            return result_company
        driver.quit()
        return result_company
        
if __name__=="__main__": 
    scraper_instance = ScacScraper()
    scraper_instance.scrape_all_results(company="FedEx")
    # scraper_instance.check_results(code="JDSFIJSD")