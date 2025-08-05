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
```
├── app/                                  # [WIP] Deployment repo using LlamaDeploy
│   ├── backend/                          # Backend services
│   └── frontend/                         # Autogen Stock Analyst App (UI & interaction logic)
├── data/                                 # Source documents for RAG engine ingestion
│   ├── books/                            # Book documents
│   ├── context/                          # [WIP] Context data for memory recall
│   └── notes/                            # [WIP] Notes used for memory recall
├── images/                               # Image assets
├── notebooks/                            # Experimental notebooks and development code
│   ├── 1.01-jk-workflow.ipynb            # [WIP] Multi-agent workflow exploration via Event-driven design                              
│   ├── 1.02-jk-tracing_agents.ipynb      # LlamaTrace testing on individual agent workflows
│   └── 1.03-jk-digital_twin.ipynb        # Testing FunctionCallingAgent & ReflectiveAgent workflows
├── requirements.txt                      # Python dependencies
└── README.md                             # Project documentation
```
