# Warning control
import warnings
import os
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv
from DunsScraperTool import DunsScraperTool
from ScacScraperTool import ScacScraperTool

warnings.filterwarnings('ignore')

load_dotenv()

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
duns_scraper_tool = DunsScraperTool()
scac_scraper_tool = ScacScraperTool()

print("Hello World")


openai_api_key = os.getenv('OPENAI_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
# os.environ["SERPER_API_KEY"] = serper_api_key

support_agent = Agent(
    role="Senior Company Researcher",
	goal="Find the most relevant and useful information"
        "for the customer's inquiry and be the best at doing it",
	backstory=(
		"You are a Senior Company Researcher and "
        " are now working on providing "
		"research to {person}, a super important customer "
        " to you."
		"You need to make sure that you provide the best research and find all necessary information!"
		"Make sure to provide full complete answers for each company in {company}, provide necessary links of where information was gathered "
        " and make no assumptions. The information you will be finding for each company will be: Company email (using company email, not a personal gmail or other commercial mail)," \
        f"phone number (company phone number, not personal), country, full corporate mailing address,"\
        f"corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
        # f"To find the DUNS number and address for the company, use the DUNS Scraper Tool. When using this tool, please provide the company name and the country code."
        # "You will have to use this tool each time for each company in {company}."
        # "The country code is the two-letter code for the country, for example, US for United States."
        # "The result is a string with the DUNS number and the address separated by a '|'."
        # "You must break the result into two variables, the DUNS number and the address."
	),
	allow_delegation=False,
	verbose=True,
    # tools = [duns_scraper_tool]
    # tools = [scrape_tool, search_tool]
)

# support_quality_assurance_agent = Agent(
# 	role="Support Quality Assurance Specialist",
# 	goal="Get recognition for providing the "
#     "best support quality assurance in your team",
# 	backstory=(
# 		"You are quality assurance specialist and "
#         "are now working with your team "
# 		"on a request from {person} ensuring that "
#         "the researcher is "
# 		"providing the best research possible.\n"
# 		"You need to make sure that the researcher"
#         "is providing full complete answers for each company in {company}, and make sure that no field is left unanswered."
#         "Do not tell the researcher to change an answer if it has come up with one for a specific field. Just ensure that each company"
#         "has a tax ID, DUNS, and SCAC. Do not take N/A as an answer."
# 	),
# 	verbose=True
# )

duns_support_agent = Agent(
    role="Senior Company Researcher",
	goal="Find the DUNS number and address for each company in {company}"
        "and be the best at doing it",
	backstory=(
		"You are a Senior Company Researcher and "
        " are now working on providing "
		"research to {person}, a super important customer "
        " to you."
		"You need to make sure that you provide the best research and find all necessary information!"
		"You will take the outut from the previous agents and fill in for the DUNS number and address for each company in {company}."
        "Your information should replace the existing information, unless you get a 'N/A' for a DUNS number or address for that company"
		"Make sure to provide full complete answers for each company in {company}, provide necessary links of where information was gathered "
        "and make no assumptions. The information you will be finding for each company will be: DUNS number and address"
        "To find the DUNS number and address for each company, use the DUNS Scraper Tool. When using this tool, please provide the company name and the country code."
        "The country code is the two-letter code for the country, for example, US for United States."
        "The result is a string with the DUNS number and the address separated by a '|'."
        "You must break the result into two variables, the DUNS number and the address."
        "You will have to use this tool each time for each company in {company}. You can only enter one company and country at a time for this tool."
        "For example, if we have Google, Lenovo, and Microsoft as our list of companies, you will have to use this tool 3 times to retrieve all necessary information."
        "So the first entry into the tool would be 'company=Google, country=US'. After you get the first result the second entry would be 'company=Lenovo, country=US'. And you do this for each company in {company}"
        "As can be seen from the example, you may have to use this tool mutliple times in order to retrieve all necessary information."
        "The information you gained should trump all previous information and you should update the existing information as such for the DUNS number and address."
    ),
	allow_delegation=False,
	verbose=True,
    tools = [duns_scraper_tool]
    # tools = [scrape_tool, search_tool]
)

scac_support_agent = Agent(
    role="Senior Company Researcher",
	goal="Find the SCAC code for each company in {company}"
        "and be the best at doing it",
	backstory=(
		"You are a Senior Company Researcher and "
        " are now working on providing "
		"research to {person}, a super important customer "
        " to you."
		"You need to make sure that you provide the best research and find all necessary information!"
        "You will take the outut from the previous agents and fill in for the DUNS and address for each company in {company}."
        "Your information should replace the existing information, unless you get a 'N/A' for a SCAC code for that company"
		"Make sure to provide full complete answers for each company in {company}, provide necessary links of where information was gathered "
        "and make no assumptions. The information you will be finding for each company will be: SCAC Code"
        "You will have to use this tool each time for each company in {company}. You can only enter one company at a time for this tool."
        "For example, if we have Google, Lenovo, and Microsoft as our list of companies, you will have to use this tool 3 times to retrieve all necessary information."
        "So the first entry into the tool would be 'company=Google'. After you get the first result the second entry would be 'company=Lenovo'. And you do this for each company in {company}"
        "As can be seen from the example, you may have to use this tool mutliple times in order to retrieve all necessary information."
        "The information you gained should trump all previous information and you should update the existing information as such for the SCAC code."
	),
	allow_delegation=False,
	verbose=True,
    tools = [scac_scraper_tool]
    # tools = [scrape_tool, search_tool]
)

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
    agent=support_agent,
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
        "To find the DUNS number and address for the company, use the DUNS Scraper Tool. When using this tool, please provide the company name and the country code."
        "The country code is the two-letter code for the country, for example, US for United States."
        "The result is a string with the DUNS number and the address separated by a '|'."
        "You must break the result into two variables, the DUNS number and the address."
        "You will have to use this tool each time for each company in {company}. You can only enter one company and country at a time for this tool."
        "So you may have to use this tool mutliple times in order to retrieve all necessary information."
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
    agent=scac_support_agent,
)

crew = Crew(
  agents=[support_agent, duns_support_agent, scac_support_agent],
  tasks=[inquiry_resolution, duns_inquiry_resolution, scac_inquiry_resolution],
  verbose=2,
  memory=True
)

inputs = {
    "company": "One Network Enterprises, FedEx, UPS",
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