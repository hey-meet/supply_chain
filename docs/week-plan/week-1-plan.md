# Week 1 Development Plan

## Theme

Web Search Integration and Supply Chain Disruption Classification

---

# Week Objective

The primary objective of Week 1 is to establish the project's technical foundation by integrating real-time logistics news retrieval and implementing the first AI agent responsible for disruption classification.

During this phase, the system will begin collecting external supply chain intelligence (OSINT), allowing future agents to analyze business impact and recommend mitigation strategies.

---

# Engineering Goals

- Initialize the backend development environment.
- Configure project dependencies.
- Integrate Tavily Search API.
- Fetch real-time logistics and supply chain news.
- Design the News Intelligence Agent.
- Build the initial disruption classification pipeline.
- Define structured Pydantic output models.
- Prepare the backend architecture for multi-agent workflows.

---

# Functional Scope

The system should be capable of:

- Searching global logistics news.
- Searching transportation disruptions.
- Searching commodity price updates.
- Searching weather events affecting logistics.
- Searching government policy updates affecting transportation.

The retrieved news should then be classified into business-relevant disruption categories.

---

# Disruption Categories

The AI should classify articles into categories such as:

- Flood
- Heavy Rainfall
- Road Closure
- Railway Strike
- Port Congestion
- Fuel Price Increase
- Coal Price Increase
- Supplier Shutdown
- Political Conflict
- Natural Disaster
- Safe / No Risk

Each classification should include:

- Risk Type
- Severity
- Location
- Confidence Score
- Executive Summary

---

# Week 1 Deliverables

## Backend

- Python environment configured
- FastAPI initialized
- Project folder structure finalized
- Tavily API integrated

---

## AI

First AI Agent:

### News Intelligence Agent

Responsibilities:

- Search logistics news
- Read articles
- Extract important information
- Identify disruption category
- Assign severity
- Produce structured JSON output

---

## Models

Create initial Pydantic schemas for:

- News Article
- Classified Risk
- News Summary

---

## Testing

Verify that:

- News retrieval works correctly.
- AI classification produces valid structured output.
- Different logistics events are correctly categorized.

---

# Expected Input

Example:

> Heavy rainfall causes highway closure between limestone quarry and Plant A.

---

# Expected Output

```json
{
  "risk_type": "Flood",
  "severity": "High",
  "location": "Gujarat",
  "confidence": 0.95,
  "summary": "Heavy rainfall has disrupted the primary transportation route supplying limestone to Plant A."
}
```

---

# Week 1 Success Criteria

Week 1 will be considered complete if the system can:

- Retrieve real-world logistics news.
- Classify disruptions using an LLM.
- Produce structured JSON responses.
- Prepare the backend architecture for the multi-agent workflow planned in Week 2 and Week 3.

---

# Next Phase Preview

Week 2 focuses on building the internal supply chain knowledge graph for the cement manufacturing network.

The classified disruption generated in Week 1 will become the input for the Supply Chain Impact Agent developed during the following phase.