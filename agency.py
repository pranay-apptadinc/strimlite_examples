from typing import List, Literal, Dict, Optional
from agency_swarm import Agent, Agency, set_openai_key, BaseTool
from pydantic import Field, BaseModel
import streamlit as st
import argparse
from streamlit_echarts import st_echarts
import streamlit.components.v1 as components
import time

parser = argparse.ArgumentParser()
parser.add_argument("--api_base_path", type=str, default="http://default-api-path.com", help="Base path for the API")
args, _ = parser.parse_known_args()

class AnalyzeProjectRequirements(BaseTool):

    

    project_name: str = Field(..., description="Name of the project")
    project_description: str = Field(..., description="Project description and goals")
    project_type: Literal["Web Application", "Mobile App", "API Development", 
                         "Data Analytics", "AI/ML Solution", "Other"] = Field(..., 
                         description="Type of project")
    budget_range: Literal["$10k-$25k", "$25k-$50k", "$50k-$100k", "$100k+"] = Field(..., 
                         description="Budget range for the project")

   
    

    
    

    class ToolConfig:
        name = "analyze_project"
        description = "Analyzes project requirements and feasibility"
        one_call_at_a_time = True

    def run(self) -> str:
        """Analyzes project and stores results in shared state"""
        if self._shared_state.get("project_analysis", None) is not None:
            raise ValueError("Project analysis already exists. Please proceed with technical specification.")
        
        analysis = {
            "name": self.project_name,
            "type": self.project_type,
            "complexity": "high",
            "timeline": "6 months",
            "budget_feasibility": "within range",
            "requirements": ["Scalable architecture", "Security", "API integration"]
        }
        
        self._shared_state.set("project_analysis", analysis)
        return "Project analysis completed. Please proceed with technical specification."

class CreateTechnicalSpecification(BaseTool):
    architecture_type: Literal["monolithic", "microservices", "serverless", "hybrid"] = Field(
        ..., 
        description="Proposed architecture type"
    )
    core_technologies: str = Field(
        ..., 
        description="Comma-separated list of main technologies and frameworks"
    )
    scalability_requirements: Literal["high", "medium", "low"] = Field(
        ..., 
        description="Scalability needs"
    )

    class ToolConfig:
        name = "create_technical_spec"
        description = "Creates technical specifications based on project analysis"
        one_call_at_a_time = True

    def run(self) -> str:
        """Creates technical specification based on analysis"""
        project_analysis = self._shared_state.get("project_analysis", None)
        if project_analysis is None:
            raise ValueError("Please analyze project requirements first using AnalyzeProjectRequirements tool.")
        
        spec = {
            "project_name": project_analysis["name"],
            "architecture": self.architecture_type,
            "technologies": self.core_technologies.split(","),
            "scalability": self.scalability_requirements
        }
        
        self._shared_state.set("technical_specification", spec)
        return f"Technical specification created for {project_analysis['name']}."

def init_session_state() -> None:
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None

def main() -> None:
    st.set_page_config(page_title="AI For Software Comany Project Plan", layout="wide")
    init_session_state()
    
    st.title("🚀 AI For Software Comany Project Plan")
    st.write(f"API Base Path: {args.api_base_path}")
    # API Configuration
    with st.sidebar:
        st.header("🔑 API Configuration")
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key to continue"
        )

        if openai_api_key:
            st.session_state.api_key = openai_api_key
            st.success("API Key accepted!")
        else:
            st.warning("⚠️ Please enter your OpenAI API Key to proceed")
            st.markdown("[Get your API key here](https://platform.openai.com/api-keys)")
            return
        
    # Initialize agents with the provided API key
    set_openai_key(st.session_state.api_key)
    api_headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
    
    # Project Input Form
    @st.dialog("Cast your vote")
    def vote(item):
        st.write(f"Why is your favorite in {item}?")
        reason = st.text_input("Because...")
        if st.button("Submit"):
            st.session_state.vote = {"item": item, "reason": reason}
            st.rerun()

    if "vote" not in st.session_state:
        st.write("Vote for your favorite")
        if st.button("chatgpt"):
            vote("chatgpt")
        if st.button("perplexity"):
            vote("perplexity")
    else:
        f"You voted for {st.session_state.vote['item']} because {st.session_state.vote['reason']}"

    with st.popover("Open popover"):
        st.markdown("Hello World 👋")
        name = st.text_input("What's your name?")

        st.write("Your name:", name)

    popover = st.popover("Filter items")
    red = popover.checkbox("Show red items.", True)
    blue = popover.checkbox("Show blue items.", True)

    if red:
        st.write(":red[This is a red item.]")
    if blue:
        st.write(":blue[This is a blue item.]")

    sub_col1, sub_col2, sub_col3 = st.columns(3)
    sub_col1.metric("SPDR S&P 500", "$437.8", "-$1.25")
    sub_col2.metric("FTEC", "$121.10", "0.46%")
    sub_col3.metric("BTC", "$96,629.26", "+0.93%")

    st.link_button("Go to gallery", "https://streamlit.io/gallery")

    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

    options = st.multiselect(
        "What are your favorite colors",
        ["Green", "Yellow", "Red", "Blue"],
        ["Yellow", "Red"],
    )

    st.write("You selected:", options)

    options = ["North", "East", "South", "West"]
    selection = st.pills("Directions", options, selection_mode="multi")
    st.markdown(f"Your selected options: {selection}.")

    a, b = st.columns(2)
    c, d = st.columns(2)

    a.metric("Temperature", "30°F", "-9°F", border=True)
    b.metric("Wind", "4 mph", "2 mph", border=True)

    c.metric("Humidity", "77%", "5%", border=True)
    d.metric("Pressure", "30.34 inHg", "-2 inHg", border=True)

    echartOptions: dict = {
        "xAxis": {
            "type": "category",
            "data": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": [820, 932, 901, 934, 1290, 1330, 1320], "type": "line"}
        ],
    }
    st_echarts(options=echartOptions)

    with st.form("project_form"):
        st.subheader("Project Details")
        
        project_name = st.text_input("Project Name")
        project_description = st.text_area(
            "Project Description",
            help="Describe the project, its goals, and any specific requirements"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            project_type = st.selectbox(
                "Project Type",
                ["Web Application", "Mobile App", "API Development", 
                 "Data Analytics", "AI/ML Solution", "Other"]
            )
            timeline = st.selectbox(
                "Expected Timeline",
                ["1-2 months", "3-4 months", "5-6 months", "6+ months"]
            )
        


            # bootstrap 4 collapse example
            components.html(
                """
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
                <div id="accordion">
                <div class="card">
                    <div class="card-header" id="headingOne">
                    <h5 class="mb-0">
                        <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                        Collapsible Group Item #1
                        </button>
                    </h5>
                    </div>
                    <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
                    <div class="card-body">
                        Collapsible Group Item #1 content
                    </div>
                    </div>
                </div>
                <div class="card">
                    <div class="card-header" id="headingTwo">
                    <h5 class="mb-0">
                        <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                        Collapsible Group Item #2
                        </button>
                    </h5>
                    </div>
                    <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
                    <div class="card-body">
                        Collapsible Group Item #2 content
                    </div>
                    </div>
                </div>
                </div>
                """,
                height=600,
            )

            components.iframe("https://apptad.com/", height=500)
            st.toast('Your edited image was saved!', icon='😍')
            st.success('This is a success message!', icon="✅")
            st.info('This is a purely informational message', icon="ℹ️")
            st.warning('This is a warning', icon="⚠️")
            st.error('This is an error', icon="🚨")
            e = RuntimeError("This is an exception of type RuntimeError")
            st.exception(e)
            
            

        with col2:
            budget_range = st.selectbox(
                "Budget Range",
                ["$10k-$25k", "$25k-$50k", "$50k-$100k", "$100k+"]
            )
            priority = st.selectbox(
                "Project Priority",
                ["High", "Medium", "Low"]
            )
        slider_val = st.slider("Form slider")
        checkbox_val = st.checkbox("Form checkbox")
        tech_requirements = st.text_area(
            "Technical Requirements (optional)",
            help="Any specific technical requirements or preferences"
        )
        
        special_considerations = st.text_area(
            "Special Considerations (optional)",
            help="Any additional information or special requirements"
        )
        
        submitted = st.form_submit_button("Analyze Project")
        
        if submitted and project_name and project_description:
            try:
                # Set OpenAI key
                set_openai_key(st.session_state.api_key)
                st.toast('First Message')
                time.sleep(.5)
                st.toast('After 5 second')
                time.sleep(.5)
                st.toast('Last Success', icon='🎉')

                # Create agents
                ceo = Agent(
                    name="Project Director",
                    description="You are a CEO of multiple companies in the past and have a lot of experience in evaluating projects and making strategic decisions.",
                    instructions="""
                    You are an experienced CEO who evaluates projects. Follow these steps strictly:

                    1. FIRST, use the AnalyzeProjectRequirements tool with:
                       - project_name: The name from the project details
                       - project_description: The full project description
                       - project_type: The type of project (Web Application, Mobile App, etc)
                       - budget_range: The specified budget range

                    2. WAIT for the analysis to complete before proceeding.
                    
                    3. Review the analysis results and provide strategic recommendations.
                    """,
                    tools=[AnalyzeProjectRequirements],
                    api_headers=api_headers,
                    temperature=0.7,
                    max_prompt_tokens=25000
                )

                cto = Agent(
                    name="Technical Architect",
                    description="Senior technical architect with deep expertise in system design.",
                    instructions="""
                    You are a technical architect. Follow these steps strictly:

                    1. WAIT for the project analysis to be completed by the CEO.
                    
                    2. Use the CreateTechnicalSpecification tool with:
                       - architecture_type: Choose from monolithic/microservices/serverless/hybrid
                       - core_technologies: List main technologies as comma-separated values
                       - scalability_requirements: Choose high/medium/low based on project needs

                    3. Review the technical specification and provide additional recommendations.
                    """,
                    tools=[CreateTechnicalSpecification],
                    api_headers=api_headers,
                    temperature=0.5,
                    max_prompt_tokens=25000
                )

                product_manager = Agent(
                    name="Product Manager",
                    description="Experienced product manager focused on delivery excellence.",
                    instructions="""
                    - Manage project scope and timeline giving the roadmap of the project
                    - Define product requirements and you should give potential products and features that can be built for the startup
                    """,
                    api_headers=api_headers,
                    temperature=0.4,
                    max_prompt_tokens=25000
                )

                developer = Agent(
                    name="Lead Developer",
                    description="Senior developer with full-stack expertise.",
                    instructions="""
                    - Plan technical implementation
                    - Provide effort estimates
                    - Review technical feasibility
                    """,
                    api_headers=api_headers,
                    temperature=0.3,
                    max_prompt_tokens=25000
                )

                client_manager = Agent(
                    name="Client Success Manager",
                    description="Experienced client manager focused on project delivery.",
                    instructions="""
                    - Ensure client satisfaction
                    - Manage expectations
                    - Handle feedback
                    """,
                    api_headers=api_headers,
                    temperature=0.6,
                    max_prompt_tokens=25000
                )

                # Create agency
                agency = Agency(
                    [
                        ceo, cto, product_manager, developer, client_manager,
                        [ceo, cto],
                        [ceo, product_manager],
                        [ceo, developer],
                        [ceo, client_manager],
                        [cto, developer],
                        [product_manager, developer],
                        [product_manager, client_manager]
                    ],
                    async_mode='threading',
                    shared_files='shared_files'
                )
                
                # Prepare project info
                project_info = {
                    "name": project_name,
                    "description": project_description,
                    "type": project_type,
                    "timeline": timeline,
                    "budget": budget_range,
                    "priority": priority,
                    "technical_requirements": tech_requirements,
                    "special_considerations": special_considerations,
                    "slider_val":slider_val,
                    "checkbox_val":checkbox_val
                }

                st.session_state.messages.append({"role": "user", "content": str(project_info)})
                # Create tabs and run analysis
                with st.spinner("AI Services Agency is analyzing your project..."):
                    try:
                        # Get analysis from each agent using agency.get_completion()
                        ceo_response = agency.get_completion(
                            message=f"""Analyze this project using the AnalyzeProjectRequirements tool:
                            Project Name: {project_name}
                            Project Description: {project_description}
                            Project Type: {project_type}
                            Budget Range: {budget_range}
                            
                            Use these exact values with the tool and wait for the analysis results.""",
                            recipient_agent=ceo
                        )
                        
                        cto_response = agency.get_completion(
                            message=f"""Review the project analysis and create technical specifications using the CreateTechnicalSpecification tool.
                            Choose the most appropriate:
                            - architecture_type (monolithic/microservices/serverless/hybrid)
                            - core_technologies (comma-separated list)
                            - scalability_requirements (high/medium/low)
                            
                            Base your choices on the project requirements and analysis.""",
                            recipient_agent=cto
                        )
                        
                        pm_response = agency.get_completion(
                            message=f"Analyze project management aspects: {str(project_info)}",
                            recipient_agent=product_manager,
                            additional_instructions="Focus on product-market fit and roadmap development, and coordinate with technical and marketing teams."
                        )

                        developer_response = agency.get_completion(
                            message=f"Analyze technical implementation based on CTO's specifications: {str(project_info)}",
                            recipient_agent=developer,
                            additional_instructions="Provide technical implementation details, optimal tech stack you would be using including the costs of cloud services (if any) and feasibility feedback, and coordinate with product manager and CTO to build the required products for the startup."
                        )
                        
                        client_response = agency.get_completion(
                            message=f"Analyze client success aspects: {str(project_info)}",
                            recipient_agent=client_manager,
                            additional_instructions="Provide detailed go-to-market strategy and customer acquisition plan, and coordinate with product manager."
                        )
                        
                        # Create tabs for different analyses
                        tabs = st.tabs([
                            "CEO's Project Analysis",
                            "CTO's Technical Specification",
                            "Product Manager's Plan",
                            "Developer's Implementation",
                            "Client Success Strategy"
                        ])
                        
                        with tabs[0]:
                            st.markdown("## CEO's Strategic Analysis")
                            st.markdown(ceo_response)
                            st.session_state.messages.append({"role": "assistant", "content": ceo_response})
                        
                        with tabs[1]:
                            st.markdown("## CTO's Technical Specification")
                            st.markdown(cto_response)
                            st.session_state.messages.append({"role": "assistant", "content": cto_response})
                        
                        with tabs[2]:
                            st.markdown("## Product Manager's Plan")
                            st.markdown(pm_response)
                            st.session_state.messages.append({"role": "assistant", "content": pm_response})
                        
                        with tabs[3]:
                            st.markdown("## Lead Developer's Development Plan")
                            st.markdown(developer_response)
                            st.session_state.messages.append({"role": "assistant", "content": developer_response})
                        
                        with tabs[4]:
                            st.markdown("## Client Success Strategy")
                            st.markdown(client_response)
                            st.session_state.messages.append({"role": "assistant", "content": client_response})

                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                        st.error("Please check your inputs and API key and try again.")

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.error("Please check your API key and try again.")

    # Add history management in sidebar
    with st.sidebar:
        st.subheader("Options")
        if st.checkbox("Show Analysis History"):
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        if st.button("Clear History"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()