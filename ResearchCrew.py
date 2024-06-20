# Warning control
import warnings
import os
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from DunsScraperTool import DunsScraperTool
from ScacScraperTool import ScacScraperTool
from ResearchAgents import ResearchAgents

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

        # Create the agents
        senior_researcher_agent = ResearchAgents().senior_researcher_agent()
        duns_support_agent = ResearchAgents().duns_support_agent()
        scac_support_agent = ResearchAgents().scac_support_agent()
        # support_quality_assurance_agent = ResearchAgents().support_quality_assurance_agent()

        inquiry_resolution = Task(
            description=(
                "{person} just reached out with a super important ask:\n"
                "{inquiry}\n\n"
                "Make sure to use everything you know "
                "to provide the best answers possible for these companies: {company}."
                "You must strive to provide a complete "
                "and accurate response to the customer's inquiry."
            ),
            expected_output=(
                "A detailed, informative response to the "
                "customer's inquiry that addresses "
                "all aspects of their question.\n"
                "The response should include the following for each company in {company}: Company email (using company email, not a personal gmail or other commercial mail)," \
                f"phone number (company phone number, not personal), country, full corporate mailing address,"\
                f"corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Include everything you used to find the answer, "
                "including external data or solutions. "
                "Ensure the answer is complete and in proper JSON format, "
                "leaving no questions unanswered, and maintain a helpful and friendly "
                "tone throughout."
            ),
            agent=senior_researcher_agent,
        )

        # quality_assurance_review = Task(
        #     description=(
        #         "Review the response drafted by the Senior Company Researcher. "
        #         "Ensure that the answer is comprehensive, accurate, and adheres to the "
        # 		"high-quality standards expected for customer support.\n"
        #         "Verify that all parts of the customer's inquiry "
        #         "have been addressed which are  Company email (using company email, not a personal gmail or other commercial mail)," \
        #            f"phone number (company phone number, not personal), country, full corporate mailing address,"\
        #            f"corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
        #            "Display this information in a nicely formatted JSON format.\n"
        #         "Check for references and sources used to "
        #         " find the information, "
        # 		"ensuring the response is well-supported and "
        #         "leaves no questions unanswered."
        #     ),
        #     expected_output=(
        #         "A final, detailed, and informative response "
        #         "ready to be sent to the customer in JSON format.\n"
        #         "This response should fully address the "
        #         "customer's inquiry, incorporating all "
        # 		"relevant feedback and improvements.\n"
        #     ),
        #     agent=support_quality_assurance_agent,
        # )
        duns_inquiry_resolution = Task(
            description=(
                "{person} just reached out with a super important ask:\n"
                "{inquiry}\n\n"
                "Make sure to use everything you know "
                "to provide the best answers possible for these companies: {company}."
                "You must strive to provide a complete "
                "and accurate response to the customer's inquiry."
                "To find the DUNS number and mailing address for the company, use the DUNS Scraper Tool. When using this tool, please provide the company name and the country code."
                "The country code is the two-letter code for the country, for example, US for United States."
                "The result is a string with the DUNS number and the mailing address separated by a '|'."
                "You must break the result into two variables, the DUNS number and the mailing address."
                "You will have to use this tool each time for each company in {company}. You can only enter one company and country at a time for this tool."
                "So you may have to use this tool mutliple times in order to retrieve all necessary information."
                "The information you gained should trump all previous information and you should update the existing information as such for the DUNS number and mailing address only."
                "Only use this tool once for each company in {company}."
            ),
            expected_output=(
                "A JSON that addresses "
                "all aspects of their question.\n"
                "The response should include the following for each company in {company}: Company email (using company email, not a personal gmail or other commercial mail)," \
                f"phone number (company phone number, not personal), country, full corporate mailing address,"\
                f"corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Ensure that the information you find on DUNS and mailing address replaces existing information in the JSON."
                "Ensure the answer is complete and in proper JSON format."
            ),
            agent=duns_support_agent,
        )

        scac_inquiry_resolution = Task(
            description=(
                "{person} just reached out with a super important ask:\n"
                "{inquiry}\n\n"
                "Make sure to use everything you know "
                "to provide the best answers possible for these companies: {company}."
                "You must strive to provide a complete "
                "and accurate response to the customer's inquiry."
                "To find the SCAC code for each company, use the SCAC Scraper Tool. When using this tool, please provide the company name."
                "You will have to use this tool each time for each company in {company}. You can only enter one company at a time for this tool."
                "So you may have to use this tool mutliple times in order to retrieve all necessary information."
                "The information you gained should trump all previous information and you should update the existing information as such for the SCAC code only."
                "Only use this tool once for each company in {company}."
            ),
            expected_output=(
                "A JSON that addresses "
                "all aspects of their question.\n"
                "The response should include the following for each company in {company}: Company email (using company email, not a personal gmail or other commercial mail)," \
                f"phone number (company phone number, not personal), country, full corporate mailing address,"\
                f"corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Ensure that the information you find on SCAC replaces existing information in the JSON."
                "Ensure the answer is complete and in proper JSON format."
            ),
            agent=scac_support_agent,
        )

        crew = Crew(
        agents=[senior_researcher_agent, duns_support_agent, scac_support_agent],
        tasks=[inquiry_resolution, duns_inquiry_resolution, scac_inquiry_resolution],
        verbose=2,
        memory=True
        )

        inputs = {
            "company": company,
            "person": "Jason Esrada",
            "inquiry": "The report should focus on finding information on the following for each company: Company email (using company email, not a personal gmail or other commercial mail)," \
                f"phone number (company phone number, not personal), country, full corporate mailing address,"\
                f"corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Lookup websites to find all the required information if needed. You should strive to find a factual tax identifier and DUNS. You can use https://scaccodelookup.com/scac-name-lookup/ to find the relevant SCAC\n" \
                "You should strive to write the report using all relevant and necessary information provided.\n" \
                "You must write the report provide a JSON format of the information. The JSON keys for each company should be the following:" \
                "Contact email, Phone number, Country, Mailing address, Website, Tax identifier, DUNS, SCAC. In the JSON, only provide one answer per key. In the JSON, make sure each company is included with the relevant information." \
                "If there are multiple different values for the same key, only provide the most general or relevant one.\n " \
        }
        result = crew.kickoff(inputs=inputs)
        print(result)
        return result