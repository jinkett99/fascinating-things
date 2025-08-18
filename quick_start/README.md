## Quick Start for Simple Llama-Deploy Deployment Workflow
- Define deployment in quick_start.yml file: Deployment name, speciify port for control plane, service definition (function_agent_workflow).
- Run API server (control plane with message queue?): "python -m llama_deploy.apiserver"
- From another shell, create/run the deployment: "llamactl deploy quick_start.yml"
- Spin up Chainlit frontend: "chainlit run app.py"