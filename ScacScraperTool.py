from crewai_tools import BaseTool
from ScacScraper import ScacScraper

class ScacScraperTool(BaseTool):
    name: str ="SCAC Scraper Tool"
    description: str = ("Scrapes the SCAC code for a given company."
                        "Use this tool to get the SCAC code for a given company."
                        "When using this tool, please provide the company name."
                        "The result is a string with the SCAC code."
                        )
    
    def _run(self, company: str) -> str:
        # Your custom code tool goes here
        scraper_instance = ScacScraper()
        result = scraper_instance.scrape_all_results(company=company)
        return result