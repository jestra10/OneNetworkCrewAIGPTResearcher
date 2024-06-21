# Warning control
import warnings
import os
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from DunsScraperTool import DunsScraperTool
from ScacScraperTool import ScacScraperTool
from ResearchAgents import ResearchAgents
from ResearchTasks import ResearchTasks

class ResearchCrew:
    def __init__(self):
        pass

    def run_crew(self, company:str) -> str:
        # Load the environment variables and different keys
        warnings.filterwarnings('ignore')
        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        serper_api_key = os.getenv('SERPER_API_KEY')
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
        # os.environ["SERPER_API_KEY"] = serper_api_key

        inquiry = ("The report should focus on finding information on the following for each company: Company email (using company email, not a personal gmail or other commercial mail)," \
                "phone number (company phone number, not personal), country, full corporate mailing address,"\
                "corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Lookup websites to find all the required information if needed. You should strive to find a factual tax identifier and DUNS. You can use https://scaccodelookup.com/scac-name-lookup/ to find the relevant SCAC\n" \
                "You should strive to write the report using all relevant and necessary information provided.\n" \
                "You must write the report provide a JSON format of the information. The JSON keys for each company should be the following:" \
                "Contact email, Phone number, Country, Mailing address, Website, Tax identifier, DUNS, SCAC. In the JSON, only provide one answer per key. In the JSON, make sure each company is included with the relevant information." \
                "If there are multiple different values for the same key, only provide the most general or relevant one.\n ")
        person = "Jason Esrada"

        # Create the agents
        senior_researcher_agent = ResearchAgents().senior_researcher_agent()
        duns_support_agent = ResearchAgents().duns_support_agent()
        scac_support_agent = ResearchAgents().scac_support_agent()
        # support_quality_assurance_agent = ResearchAgents().support_quality_assurance_agent()

        inquiry_resolution = ResearchTasks().inquiry_resolution(senior_researcher_agent, person, inquiry, company)
        duns_inquiry_resolution = ResearchTasks().duns_inquiry_resolution(duns_support_agent, person, inquiry, company)
        scac_inquiry_resolution = ResearchTasks().scac_inquiry_resolution(scac_support_agent, person, inquiry, company)
        # quality_assurance_review = ResearchTasks().quality_assurance_review(support_quality_assurance_agent, person, inquiry, company)

        crew = Crew(
        agents=[senior_researcher_agent, duns_support_agent, scac_support_agent],
        tasks=[inquiry_resolution, duns_inquiry_resolution, scac_inquiry_resolution],
        verbose=2,
        memory=True
        )

        inputs = {
            "company": company,
            "person": person,
            "inquiry": inquiry
        }
        result = crew.kickoff(inputs=inputs)
        print(result)
        return result