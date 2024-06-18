from crewai_tools import BaseTool
from DunsScraper import DunsScraper

class DunsScraperTool(BaseTool):
    name: str ="DUNS Scraper Tool"
    description: str = ("Scrapes the DUNS number and address for a given company and country."
                        "Use this tool to get the DUNS number and address for a given company and country."
                        "When using this tool, please provide the company name and the country code."
                        "The country code is the two-letter code for the country, for example, US for United States."
                        "The result is a string with the DUNS number and the address separated by a '|'."
                        "You must break the result into two variables, the DUNS number and the address."
                        )
    
    def _run(self, company: str, country: str) -> str:
        # Your custom code tool goes here
        scraper_instance = DunsScraper()
        result = scraper_instance.scrape_top_result_str(company=company, country=country)
        return result