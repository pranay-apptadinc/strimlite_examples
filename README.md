
### Five specialized AI agents 

- **CEO Agent**: Strategic leader and final decision maker
  - Analyzes startup ideas using structured evaluation
  - Makes strategic decisions across product, technical, marketing, and financial domains
  - Uses AnalyzeStartupTool and MakeStrategicDecision tools

- **CTO Agent**: Technical architecture and feasibility expert
  - Evaluates technical requirements and feasibility
  - Provides architecture decisions
  - Uses QueryTechnicalRequirements and EvaluateTechnicalFeasibility tools

- **Product Manager Agent**: Product strategy specialist
  - Defines product strategy and roadmap
  - Coordinates between technical and marketing teams
  - Focuses on product-market fit

- **Developer Agent**: Technical implementation expert
  - Provides detailed technical implementation guidance
  - Suggests optimal tech stack and cloud solutions
  - Estimates development costs and timelines

- **Client Success Agent**: Marketing strategy leader
  - Develops go-to-market strategies
  - Plans customer acquisition approaches
  - Coordinates with product team

### Custom Tools

The agency uses specialized tools built with OpenAI Schema for structured analysis:
- **Analysis Tools**: AnalyzeProjectRequirements for market evaluation and analysis of startup idea
- **Technical Tools**: CreateTechnicalSpecification for technical assessment

### 🔄 Asynchronous Communication

The agency operates in async mode, enabling:
- Parallel processing of analyses from different agents
- Efficient multi-agent collaboration
- Real-time communication between agents
- Non-blocking operations for better performance

### 🔗 Agent Communication Flows
- CEO ↔️ All Agents (Strategic Oversight)
- CTO ↔️ Developer (Technical Implementation)
- Product Manager ↔️ Marketing Manager (Go-to-Market Strategy)
- Product Manager ↔️ Developer (Feature Implementation)
- (and more!)




python3 -m venv venv
 
source venv/bin/activate
 
pip install -r requirements.txt

streamlit run agency.py


streamlit run agency.py -- --api_base_path "http://example-api.com"


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

knowledge center for our software company

this project is a knowledge center for our software company. all our employees can login and read a detail plan for business category wise like Pharmaceutical ,HCLS- Health Insurance
Admin Can add All Detail Plan Day bay day from one admin form. user can read a this document and give a rating . this system also have a Tech radar  and have a custome ui and zoom and filter options .

 
Node js (Nest Framwork ) for api , Angular latest for UI , PostgresSQL for database , Digitalocen private server for hosting.
