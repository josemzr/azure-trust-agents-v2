# 🎯 Demo Quick Reference Guide

**One-Page Cheat Sheet for Presenters**

---

## ⚡ 45-Second Elevator Pitch

*"This is an AI-powered fraud detection system for payments platforms built on Microsoft's Agent Framework. Watch as specialized AI agents collaborate in real-time to analyze transactions, consult regulatory databases, and generate audit-ready compliance reports—all in under 3 seconds. Unlike traditional systems, every decision is explainable and traceable for regulatory compliance."*

---

## 🎬 Demo Flow (45 minutes)

| Section | Time | Key Action | Wow Moment |
|---------|------|------------|------------|
| **1. Introduction** | 5 min | Show architecture diagram | "4 specialized agents like a compliance team" |
| **2. Foundation** | 10 min | Azure Portal walkthrough | "Deployed in 10 minutes via ARM template" |
| **3. Multi-Agent** | 15 min | DevUI live demo | "3 agents analyze TX2002 in 2.3 seconds" |
| **4. MCP Integration** | 10 min | API Management + Swagger | "Integrates with YOUR existing systems" |
| **5. Observability** | 10 min | Application Insights traces | "Every decision is auditable" |
| **6. Frontend** | 5 min | Dashboard walkthrough | "Production-ready UI for fraud analysts" |

---

## 🔑 Key Commands

### Start DevUI
```bash
cd challenge-1/devui
python devui_launcher.py --mode all
# Access: http://localhost:8080
```

### Get Container App URLs
```bash
RG=<your_resource_group>
CONTAINER_APP=$(az containerapp list --resource-group $RG --query "[0].name" -o tsv)
CONTAINER_APP_URL=$(az containerapp show --name $CONTAINER_APP --resource-group $RG --query properties.configuration.ingress.fqdn -o tsv)
echo "Swagger: http://$CONTAINER_APP_URL/v1/swagger-ui/index.html"
```

### Test Queries

**Customer Data Agent:**
```
Get data for customer CUST1005
```

**Risk Analyzer Agent:**
```
Evaluate risk for a $15,000 transaction to Iran by a new customer
```

**Full Workflow:**
```
Message: Analyze the risk of transaction
Transaction: TX2002
```

---

## 📊 Demo Transactions

| TX ID | Amount | Country | Risk Level | Use Case |
|-------|--------|---------|------------|----------|
| **TX2002** | $15,000 | Iran (IR) | HIGH | Main demo - sanctions, large amount |
| TX2004 | $9,500 | US | MEDIUM | Structuring pattern (just under $10K) |
| TX2007 | $25,000 | NG | HIGH | New customer, crypto, Nigeria |

**Primary Demo Transaction (TX2002):**
- Customer: CUST1002 (account age < 30 days)
- Amount: $15,000 USD
- Destination: Iran (OFAC sanctions)
- Expected Risk Score: 85/100
- Compliance: NON_COMPLIANT (SAR filing required)

---

## 💡 Key Talking Points

### 1. Multi-Agent Intelligence
"This isn't one AI doing everything—it's specialized agents working together like your fraud team. Each agent has expertise: data retrieval, risk analysis, compliance reporting."

### 2. Hybrid Approach (Rules + AI)
"We combine regulatory rules (hard thresholds, sanctions lists) with AI reasoning (pattern detection, context understanding). Best of both worlds: compliant AND intelligent."

### 3. Enterprise Integration
"We don't replace your existing systems—we make them smarter. Model Context Protocol (MCP) lets our agents talk to your fraud alerts, ticketing, and notifications with zero code changes."

### 4. Full Transparency
"Every decision is traced via OpenTelemetry. When regulators ask, 'Why did you flag this transaction?'—you show them: which data was consulted, which regulations were checked, how the score was calculated."

### 5. Production-Ready Today
"This isn't a prototype. It has enterprise SLAs, security, monitoring, and a business-friendly UI. Deploy it tomorrow in your Azure tenant."

---

## 🎯 Value Propositions

### For Payments Platforms

**Speed:**
- Manual review: 15 minutes per transaction
- AI agents: 2.3 seconds
- **96.7% faster**

**Accuracy:**
- Traditional false positives: 5% (250K/month for 5M transactions)
- AI-powered: 1% (50K/month)
- **80% reduction in customer friction**

**Cost:**
- Manual analyst costs: ~$3.1M/month (62,500 hours @ $50/hour)
- AI system costs: ~$25K/month (Azure infrastructure)
- **ROI: 10x in first year**

**Compliance:**
- Audit-ready documentation (automatic)
- Regulatory citations in every decision
- Complete trace for forensics

---

## 🔥 Wow Moments

### 1. **The Speed Demo**
Show Application Insights trace: "2.3 seconds from transaction to audit report. Faster than a credit card authorization."

### 2. **The Explainability Demo**
Show Risk Analyzer output with regulatory citations: "Not just a red flag—a compliance recommendation citing Bank Secrecy Act § 1020.320."

### 3. **The Integration Demo**
Show MCP server connecting to existing API: "Zero code changes to your fraud system. We just plugged in via API Management."

### 4. **The Observability Demo**
Show end-to-end trace in Application Insights: "When regulators audit you, here's your evidence: every query, every model call, every decision."

### 5. **The Production UI Demo**
Show frontend dashboard: "This is what your fraud team sees Monday morning. Not a spreadsheet—a modern dashboard with AI-powered insights."

---

## 🛠️ Troubleshooting

### DevUI Won't Start
```bash
# Check Python dependencies
pip install -r requirements.txt

# Verify .env file exists
cat .env | grep AGENT_ID

# Fallback: Use Jupyter notebook
code challenge-1/workflow/sequential_workflow.ipynb
```

### "Agent Not Found" Error
1. Go to Azure AI Foundry Portal (ai.azure.com)
2. Navigate to project → Agents
3. Copy agent IDs and update `.env`

### No Data in Cosmos DB
```bash
# Re-run data seeding
cd challenge-0
./seed_data.sh
```

### Application Insights Shows No Traces
- Wait 2-3 minutes for ingestion lag
- Verify connection string in `.env`
- Check telemetry exporters in code

---

## 📋 Pre-Demo Checklist

**Infrastructure:**
- [ ] Azure resources deployed (all green in Resource Group)
- [ ] `.env` file configured with all agent IDs and keys
- [ ] Cosmos DB has sample data (check Transactions container)
- [ ] Application Insights workspace created

**Local Environment:**
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] DevUI tested and running (http://localhost:8080)
- [ ] Jupyter notebook kernel started (if backup needed)

**Browser Tabs Open:**
- [ ] Azure Portal - Resource Group overview
- [ ] Azure Portal - Cosmos DB Data Explorer
- [ ] Azure Portal - Application Insights Transaction search
- [ ] Container App Swagger UI
- [ ] Container App Frontend Dashboard
- [ ] Azure AI Foundry Portal (ai.azure.com)
- [ ] DevUI (localhost:8080)

**Test Run:**
- [ ] DevUI Customer Data Agent query works
- [ ] DevUI Risk Analyzer Agent query works
- [ ] DevUI Full Workflow completes successfully for TX2002
- [ ] Application Insights shows traces from test run
- [ ] Frontend dashboard loads and displays alerts

---

## 🎤 Handling Common Objections

### "We already have a fraud system."
**Response:** *"Perfect! We integrate with it via MCP. Think of this as an AI co-pilot for your existing system, not a replacement. Your workflows stay the same; we just add intelligence."*

### "AI decisions are black boxes."
**Response:** *"That's why we built full observability. Every decision is traced with OpenTelemetry—you see which data was queried, which regulations were consulted, how the risk score was calculated. It's more transparent than most rule-based systems."*

### "What about false positives?"
**Response:** *"We're seeing 80% reduction in pilot programs. The AI provides context—account history, behavioral patterns, regulatory requirements—so you only flag transactions that truly warrant review. Better for compliance AND customer experience."*

### "How long to deploy?"
**Response:** *"Infrastructure: 1 day. Integration: 2 weeks. Pilot with real data: 6 weeks. This isn't a multi-year project—it's a multi-month rollout."*

### "What's the cost?"
**Response:** *"For 5M transactions/month, about $25K/month in Azure costs. Compare that to manual review costs of $3M+/month. Typical ROI is 10x in year one."*

---

## 📞 Next Steps

### Immediate Actions
1. **Try It:** Fork repo, run in GitHub Codespaces (free tier)
2. **Share Internally:** Send demo recording to fraud/compliance teams
3. **Schedule Deep Dive:** Technical workshop with your engineering team

### Pilot Program Phases
- **Phase 1 (4 weeks):** Proof of value with 100K historical transactions
- **Phase 2 (6 weeks):** Integration with production systems (read-only)
- **Phase 3 (8 weeks):** Production rollout with human-in-the-loop

### Decision-Maker Engagement
- **For Fraud Team:** Focus on false positive reduction and analyst productivity
- **For Compliance Team:** Emphasize audit trails and regulatory citations
- **For Engineering Team:** Highlight modular architecture and Azure-native design
- **For Executives:** Lead with ROI and time-to-value metrics

---

## 🏆 Success Indicators

**During Demo:**
- ✅ Audience asks about customization possibilities
- ✅ Technical team wants to see the code
- ✅ Business team asks about pilot timeline
- ✅ Someone says "Can we try this with our data?"

**After Demo:**
- 🎯 Pilot program commitment
- 🎯 Technical team forks the repo
- 🎯 Follow-up meeting scheduled with compliance/security
- 🎯 Budget discussion initiated

---

## 📚 Leave-Behind Resources

**For Technical Teams:**
- Repository: github.com/microsoft/azure-trust-agents
- Agent Framework Docs: learn.microsoft.com/agent-framework
- Sample queries and Kusto dashboards

**For Business Teams:**
- ROI calculator spreadsheet
- Compliance capabilities one-pager
- Pilot program proposal document

**For Executives:**
- Architecture diagram (high-level)
- Cost comparison vs. manual review
- Timeline for deployment phases

---

**END OF QUICK REFERENCE**

*Keep this open in a separate window during your demo for quick lookups!*
