# Who wouldn't love fascinating things?
An Agentic AI exploration repository - Run mostly with the awesome LlamaIndex

![Image](images/potter_q.png)

---
## **Roadmap**
1. Exploration of LlamaIndex Events, Workflows, FunctionCalling Agent and ReActAgent abstractions.✅
2. Experimentation with various Agent Workflow constructs - Inspiration from Introspective Agent etc.
3. Deploying workflows with LlamaDeploy.
4. Exploration of Multi-Agent Workflows - LongRAG, Multi-strategy, Self-discover workflows etc. 
5. Customising Multi-Agent Workflow for Digital Twinning in Job Search Strategy. 

---
## **Related Articles**
**Medium Article:** https://medium.com/@jinkett99/part-iii-lets-explore-llamaindex-events-workflows-and-agents-490584516c2d

---
## **Setup Instructions**  

Follow these steps in the specified order to run the scripts successfully:

### **1. Clone the Repository**  
```bash
git clone https://github.com/jinkett99/fascinating-things.git
cd great-things
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

---
## **Content**
.
├── app                                   <- [In work] Deployment Repository (LlamaDeploy)
│   ├── backend
│   ├── frontend                          <- Code book for autogen stock analyst app
├── data                                  <- Document folders for RAG engine ingestion
│   ├── books                             <- Books
│   ├── context                           <- [In work] Context for memory recall
│   ├── notes                             <- [In work] Notes for memory recall
├── images                                <- Images
├── notebooks                             <- Experimental notebooks, development codes
│   ├── 1.01-jk-workflow.ipynb            <- [In work] Exploration of Events and Multi-Agent Workflows                              
│   ├── 1.02-jk-tracing_agents.ipynb      <- Test LlamaTrace functionalities with individual Agent Workflows
│   ├── 1.03-jk-digital_twin.ipynb        <- Test modify FunctionCallingAgent, Reflective Agent Workflow
├── requirements.txt                      <- Dependencies
├── README.md