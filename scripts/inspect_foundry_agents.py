import os
from dotenv import load_dotenv
load_dotenv(override=True)
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

pc = AIProjectClient(endpoint=os.environ['AI_FOUNDRY_PROJECT_ENDPOINT'], credential=DefaultAzureCredential())
for name, aid in [('RISK', os.environ['RISK_ANALYSER_AGENT_ID']),
                  ('COMPLIANCE', os.environ['COMPLIANCE_REPORT_AGENT_ID']),
                  ('FRAUD', os.environ['FRAUD_ALERT_AGENT_ID'])]:
    a = pc.agents.get_agent(aid)
    print('==' * 20, name, aid)
    print('name:', a.name)
    print('instructions:\n', (a.instructions or '')[:1500])
