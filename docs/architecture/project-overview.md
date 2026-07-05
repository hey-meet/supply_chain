# Autonomous Supply Chain Disruption Monitoring Agent for Cement Manufacturing

## Executive Summary

This project aims to build an autonomous multi-agent AI system capable of continuously monitoring global logistics and supply chain disruptions, analyzing their impact on a cement manufacturing network, and generating actionable mitigation plans before production is affected.

Instead of waiting for supply chain failures to occur, the system proactively monitors external events, understands the organization's internal supply chain, predicts business impact, and recommends corrective actions.

The project follows the internship specifications for developing an Agentic AI application using specialized AI agents, structured business reasoning, knowledge graphs, and executive reporting.

---

# Executive Problem Statement

Modern cement manufacturing depends on a highly interconnected supply chain consisting of raw material suppliers, transportation networks, warehouses, production plants, and regional distribution centers.

Critical raw materials include:

- Limestone
- Coal
- Gypsum
- Fly Ash
- Diesel
- Packaging Materials

Any disruption such as:

- Heavy rainfall
- Floods
- Road closures
- Railway strikes
- Port congestion
- Fuel price increase
- Coal price increase
- Supplier shutdown
- Government regulations
- Natural disasters

can interrupt the movement of raw materials, delay production, increase operational costs, and reduce customer deliveries.

Supply chain managers cannot manually monitor global news 24/7 while simultaneously evaluating how each disruption affects suppliers, transportation routes, inventories, and production plants.

This project solves that problem using autonomous AI agents.

---

# Project Objective

Develop an autonomous multi-agent AI platform capable of:

- Monitoring global logistics and supply chain news
- Detecting disruptions relevant to cement manufacturing
- Understanding the organization's complete supply chain
- Calculating operational impact
- Identifying affected plants and suppliers
- Predicting inventory shortages
- Preventing production interruptions
- Recommending mitigation strategies
- Generating executive-level disruption reports

---

# Core Idea

Instead of reacting after disruptions occur, the AI continuously watches the outside world.

Whenever an important logistics event occurs, the AI immediately answers business questions such as:

- Which production plant is affected?
- Which raw material is at risk?
- Which supplier is impacted?
- Which transportation route is blocked?
- How many production days remain?
- Which inventory requires redistribution?
- Which backup supplier should be activated?
- What actions should management take immediately?

The goal is to create a proactive supply chain resilience platform.

---

# Industry

Cement Manufacturing

Example Company

**BuildCem Industries Pvt. Ltd.** *(Fictional Company)*

A fictional company is used to simulate an enterprise-scale cement manufacturing supply chain without relying on proprietary industrial data.

---

# Business Workflow

```
Global News
      │
      ▼
News Intelligence Agent
      │
      ▼
Supply Chain Impact Agent
      │
      ▼
Mitigation Planning Agent
      │
      ▼
Executive Dashboard
```

---

# Company Supply Chain Network

```
Raw Material Suppliers
        │
        ▼
Regional Warehouses
        │
        ▼
Transportation Network
        │
        ▼
Plant A
Plant B
Plant C
        │
        ▼
Distribution Centers
        │
        ▼
Customers
```

Each production plant maintains:

- Current Inventory
- Daily Consumption
- Safety Stock
- Production Capacity
- Incoming Shipments
- Outgoing Shipments

---

# AI Agents

## 1. News Intelligence Agent

### Responsibilities

Continuously monitors:

- Logistics news
- Commodity prices
- Weather updates
- Government regulations
- Transportation disruptions
- Global supply chain events

### Risk Categories

- Flood
- Road Closure
- Railway Strike
- Port Congestion
- Fuel Price Increase
- Coal Price Increase
- Supplier Shutdown
- Political Conflict
- Safe

### Output

- Risk Type
- Severity
- Location
- Confidence Score
- Executive Summary

---

## 2. Supply Chain Impact Agent

This agent understands the organization's complete supply chain network.

### Knowledge Base

- Production Plants
- Suppliers
- Warehouses
- Transportation Routes
- Inventory
- Daily Consumption
- Lead Time
- Safety Stock
- Production Capacity

### Responsibilities

Determine:

- Affected Suppliers
- Affected Plants
- Inventory Risk
- Production Risk
- Remaining Operational Days
- Business Blast Radius

### Output

- Affected Plants
- Affected Suppliers
- Affected Routes
- Inventory Status
- Production Impact
- Business Impact

---

## 3. Mitigation Planning Agent

Responsible for generating business recommendations.

### Responsibilities

Recommend:

- Backup Suppliers
- Inventory Transfers
- Alternative Transportation Routes
- Procurement Priorities
- Production Adjustments
- Estimated Cost Impact
- Expected Delivery Delays

### Output

- Immediate Actions
- Alternative Routes
- Inventory Redistribution Plan
- Cost Estimation
- Expected Delay
- Priority Level

---

# Enterprise Knowledge Base

The platform maintains structured business data.

## Plants

- Plant A
- Plant B
- Plant C

## Suppliers

- Coal Supplier
- Limestone Supplier
- Gypsum Supplier
- Fly Ash Supplier

## Inventory

- Current Stock
- Safety Stock
- Daily Consumption
- Remaining Days

## Transportation

- Road
- Rail
- Port

## Warehouses

- Regional Storage
- Capacity
- Location

---

# End-to-End AI Workflow

```
Global News

      │

      ▼

News Intelligence Agent

      │

Classify Disruption

      │

      ▼

Supply Chain Impact Agent

      │

Identify Affected Suppliers

      │

Analyze Inventory

      │

Calculate Production Risk

      │

Determine Blast Radius

      │

      ▼

Mitigation Planning Agent

      │

Generate Action Plan

      │

      ▼

Executive Dashboard
```

---

# Example Scenario

## Incoming News

Heavy rainfall causes highway closure between the limestone quarry and Plant A.

---

## Agent 1

Detects:

- Flood
- Highway Closure
- High Severity

---

## Agent 2

Analyzes:

- Limestone supplier affected
- Plant A has only 2 days of limestone inventory
- Production interruption expected after Day 2

---

## Agent 3

Recommends:

- Transfer limestone from Plant C
- Activate alternate supplier
- Use railway transportation
- Increase procurement priority
- Prevent production shutdown

---

# Dashboard Modules

## Executive Overview

Overall Supply Chain Health

---

## Live Logistics News

Real-time disruption monitoring

---

## Supply Chain Network

Interactive graph showing:

Suppliers → Warehouses → Plants → Distribution Centers

---

## Plant Monitoring

- Production Status
- Plant Capacity
- Inventory Level
- Risk Status

---

## Inventory Dashboard

- Coal
- Limestone
- Gypsum
- Fly Ash
- Diesel

---

## Transportation Dashboard

- Road Status
- Railway Status
- Port Status

---

## AI Recommendations

- Inventory Transfer
- Backup Supplier
- Route Optimization
- Procurement Planning

---

## Executive Disruption Action Plan

AI-generated structured mitigation report.

---

# Technology Stack

| Component | Technology |
|------------|------------|
| Agent Framework | LangGraph |
| Backend | FastAPI |
| Frontend | React + Vite |
| News Search | Tavily Search API |
| Knowledge Graph | NetworkX |
| Database | SQLite + JSON |
| Validation | Pydantic |
| Visualization | React Flow |

---

# Expected Final Output

The completed platform will autonomously:

1. Continuously monitor global logistics news.
2. Detect disruptions affecting cement manufacturing.
3. Understand the complete supply chain network.
4. Identify affected suppliers and production plants.
5. Predict inventory shortages.
6. Estimate production impact.
7. Recommend inventory redistribution.
8. Suggest backup suppliers.
9. Recommend alternative transportation routes.
10. Generate executive-level disruption action plans through an interactive dashboard.

---

# Success Criteria

The project will be considered successful if it can:

- Detect supply chain disruptions from real-world news.
- Correctly identify impacted suppliers and plants.
- Calculate the operational blast radius.
- Recommend realistic mitigation strategies.
- Prevent production interruptions through proactive planning.
- Present all findings in an executive-friendly dashboard.

This project demonstrates how Agentic AI can transform traditional supply chain management into an intelligent, autonomous, and proactive decision-support system for modern cement manufacturing enterprises.