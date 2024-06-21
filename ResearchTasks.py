from crewai import Task
from textwrap import dedent

class ResearchTasks():
  def inquiry_resolution(self, agent, person, inquiry, company):
    return Task(
            description=(
                f"{person} just reached out with a super important ask:\n"
                f"{inquiry}\n\n"
                "Make sure to use everything you know "
                f"to provide the best answers possible for these companies: {company}."
                "You must strive to provide a complete "
                "and accurate response to the customer's inquiry."
            ),
            expected_output=(
                "A detailed, informative response to the "
                "customer's inquiry that addresses "
                "all aspects of their question.\n"
                f"The response should include the following for each company in {company}: Company email (using company email, not a personal gmail or other commercial mail)," \
                "phone number (company phone number, not personal), country, full corporate mailing address,"\
                "corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Include everything you used to find the answer, "
                "including external data or solutions. "
                "Ensure the answer is complete and in proper JSON format, "
                "leaving no questions unanswered, and maintain a helpful and friendly "
                "tone throughout."
            ),
            agent=agent,
        )
    
#   def quality_assurance_review(self, agent): 
#     return Task(
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
        #     agent=agent,
        # )
    # )

  def duns_inquiry_resolution(self, agent, person, inquiry, company):
    return Task(
            description=(
                f"{person} just reached out with a super important ask:\n"
                f"{inquiry}\n\n"
                "Make sure to use everything you know "
                f"to provide the best answers possible for these companies: {company}."
                "You must strive to provide a complete "
                "and accurate response to the customer's inquiry."
                "To find the DUNS number and mailing address for the company, use the DUNS Scraper Tool. When using this tool, please provide the company name and the country code."
                "The country code is the two-letter code for the country, for example, US for United States."
                "The result is a string with the DUNS number and the mailing address separated by a '|'."
                "You must break the result into two variables, the DUNS number and the mailing address."
                f"You will have to use this tool each time for each company in {company}. You can only enter one company and country at a time for this tool."
                "So you may have to use this tool mutliple times in order to retrieve all necessary information."
                "The information you gained should trump all previous information and you should update the existing information as such for the DUNS number and mailing address only."
                f"Only use this tool once for each company in {company}."
            ),
            expected_output=(
                "A JSON that addresses "
                "all aspects of their question.\n"
                f"The response should include the following for each company in {company}: Company email (using company email, not a personal gmail or other commercial mail)," \
                "phone number (company phone number, not personal), country, full corporate mailing address,"\
                "corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Ensure that the information you find on DUNS and mailing address replaces existing information in the JSON."
                "Ensure the answer is complete and in proper JSON format."
            ),
            agent=agent,
        )

  def scac_inquiry_resolution(self, agent, person, inquiry, company):
    return Task(
            description=(
                f"{person} just reached out with a super important ask:\n"
                f"{inquiry}\n\n"
                "Make sure to use everything you know "
                f"to provide the best answers possible for these companies: {company}."
                "You must strive to provide a complete "
                "and accurate response to the customer's inquiry."
                "To find the SCAC code for each company, use the SCAC Scraper Tool. When using this tool, please provide the company name."
                f"You will have to use this tool each time for each company in {company}. You can only enter one company at a time for this tool."
                "So you may have to use this tool mutliple times in order to retrieve all necessary information."
                "The information you gained should trump all previous information and you should update the existing information as such for the SCAC code only."
                f"Only use this tool once for each company in {company}."
                f"Your final response should still include the following for each company in {company}: Company email (using company email, not a personal gmail or other commercial mail)," \
                "phone number (company phone number, not personal), country, full corporate mailing address,"\
                "corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
            ),
            expected_output=(
                "A JSON that addresses "
                "all aspects of their question.\n"
                f"The response should include the following for each company in {company}: Company email (using company email, not a personal gmail or other commercial mail)," \
                "phone number (company phone number, not personal), country, full corporate mailing address,"\
                "corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, and SCAC (if NA Carrier)."
                "Ensure that the information you find on SCAC replaces existing information in the JSON."
                "Ensure the answer is complete and in proper JSON format."
            ),
            agent=agent,
        )