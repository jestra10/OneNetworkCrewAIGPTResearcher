import gradio as gr
from ResearchCrew import ResearchCrew

# crew = ResearchCrew()
# print(crew.run_crew("One Network Enterprises, FedEx, UPS"))

def crew_run(company):
    crew = ResearchCrew()
    return crew.run_crew(company)

demo = gr.Interface(
    fn=crew_run,
    inputs=[gr.Textbox(label='Company', info='Input company names to be researched. Seperate each company name by commas.')],
    outputs=[gr.Textbox(label='Company Information in JSON Format', info='This is the JSON output with all the information about the company.')],
    examples=["One Network Enterprises, FedEx, United Parcel Service"],
    title="AI Partner Onboarding Researcher",
    description="This tool helps with onboarding new partners. It uses AI agents to gather information about the company's contact email "
      " (using company email, not a personal gmail or other commercial mail), phone number (company phone number, not personal), "
      " country, mailing address, corporate website address, Tax Identifier (whatever tax id is appropriate in their country), DUNS, "
      " and SCAC code(if NA Carrier). It returns this information in a JSON format. Multiple companies can be entered at a time, as long as they are seperated by commas.",
    article= "To visit the code behind this tool, click here: https://github.com/jestra10/OneNetworkCrewAIGPTResearcher"
)

demo.launch()