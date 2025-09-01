# Simple Deployable Repository - with Llama Deploy 
Experimetation with Llama Deploy, Dockerfiles and Docker Compose.

---
## Repository Structure
```.
.
├── core/                                  # Core services for deployment
│   ├── deploy_core.py                     # Launches Control Plane and Message Queue
│   ├── Dockerfile                         # Builds image and runs deploy_core.py
│   └── requirements.txt                   # Python dependencies for core services
├── workflow/                              # Workflow service registration
│   ├── deploy_workflow.py                 # Registers workflow with Control Plane
│   ├── Dockerfile                         # Builds image and runs deploy_workflow.py
│   └── requirements.txt                   # Python dependencies for workflow service
├── frontend/                              # Frontend or testing utilities
│   └── test.py                            # Test script to run workflow as HTTP service
├── docker-compose.yml                     # Orchestrates services via private Docker network

```

---
## **Setup Instructions**  

Follow these steps in the specified order to run the deployment successfully:

### **1. Spin up backend core and workflow scripts**  
```bash
docker compose up --build
```

### **2. Run tests**  
```bash
cd frontend
python test.py
```