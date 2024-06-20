from textwrap import dedent
from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from DunsScraperTool import DunsScraperTool
from ScacScraperTool import ScacScraperTool

class ResearchAgents():
	def senior_researcher_agent(self):
		return Agent(
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

	# def support_quality_assurance_agent(self):
	# 	return Agent(
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

	def duns_support_agent(self):
		# search_tool = SerperDevTool()
		# scrape_tool = ScrapeWebsiteTool()
		duns_scraper_tool = DunsScraperTool()
		return Agent(
            role="Senior Company Researcher",
            goal="Find the DUNS number and address for each company in {company}"
                "and be the best at doing it",
            backstory=(
                "You are a Senior Company Researcher and "
                " are now working on providing "
                "research to {person}, a super important customer "
                " to you."
                "You need to make sure that you provide the best research and find all necessary information!"
                "You will take the outut from the previous agents and fill in for the DUNS number and mailing address for each company in {company}."
                "Your information should replace the existing information, unless you get a 'N/A' for a DUNS number or mailing address for that company"
                "Make sure to provide full complete answers for each company in {company}, provide necessary links of where information was gathered "
                "and make no assumptions. The information you will be finding for each company will be: DUNS number and mailing address"
                "To find the DUNS number and mailing address for each company, use the DUNS Scraper Tool. When using this tool, please provide the company name and the country code."
                "The country code is the two-letter code for the country, for example, US for United States."
                "The result is a string with the DUNS number and the mailing address separated by a '|'."
                "You must break the result into two variables, the DUNS number and the mailing address."
                "You will have to use this tool each time for each company in {company}. You can only enter one company and country at a time for this tool."
                "For example, if we have Google, Lenovo, and Microsoft as our list of companies, you will have to use this tool 3 times to retrieve all necessary information."
                "So the first argument into the tool would be 'Google'. After you get the first result the next argument put in would be 'Lenovo'. And you do this for each company in {company}"
                "As can be seen from the example, you may have to use this tool mutliple times in order to retrieve all necessary information."
                "The information you gained should be updates as such for only the DUNS number and mailing address."
            ),
            allow_delegation=False,
            verbose=True,
            tools = [duns_scraper_tool]
            # tools = [scrape_tool, search_tool]
        )
	
	def scac_support_agent(self):
		# search_tool = SerperDevTool()
		# scrape_tool = ScrapeWebsiteTool()
		scac_scraper_tool = ScacScraperTool()
		return Agent(
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
                "So the first argument into the tool would be 'Google'. After you get the first result the next argument put in would be 'Lenovo'. And you do this for each company in {company}"
                "As can be seen from the example, you may have to use this tool mutliple times in order to retrieve all necessary information."
                "The information you gained should be updated as such for only the SCAC code."
            ),
            allow_delegation=False,
            verbose=True,
            tools = [scac_scraper_tool]
            # tools = [scrape_tool, search_tool]
        )