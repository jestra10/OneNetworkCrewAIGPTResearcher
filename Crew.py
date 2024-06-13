# Warning control
import warnings
import os

warnings.filterwarnings('ignore')

from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from dotenv import load_dotenv

load_dotenv()

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

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
	),
	allow_delegation=False,
	verbose=True,
    # tools = [scrape_tool, search_tool]
)

support_quality_assurance_agent = Agent(
	role="Support Quality Assurance Specialist",
	goal="Get recognition for providing the "
    "best support quality assurance in your team",
	backstory=(
		"You are quality assurance specialist and "
        "are now working with your team "
		"on a request from {person} ensuring that "
        "the researcher is "
		"providing the best research possible.\n"
		"You need to make sure that the researcher"
        "is providing full complete answers for each company in {company}, and make sure that no field is left unanswered."
        "Do not tell the researcher to change an answer if it has come up with one for a specific field. Just ensure that each company"
        "has a tax ID, DUNS, and SCAC. Do not take N/A as an answer."
	),
	verbose=True
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

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Company Researcher. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
		"high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed which are  Company email (using company email, not a personal gmail or other commercial mail)," \
           f"phone number (company phone number, not personal), country, full corporate mailing address,"\
           f"corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
           "Display this information in a nicely formatted JSON format.\n"
        "Check for references and sources used to "
        " find the information, "
		"ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer in JSON format.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
		"relevant feedback and improvements.\n"
    ),
    agent=support_quality_assurance_agent,
)

crew = Crew(
  agents=[support_agent, support_quality_assurance_agent],
  tasks=[inquiry_resolution, quality_assurance_review],
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