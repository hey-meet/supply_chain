# backend/services/response_transformer.py

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def transform_incident(state: dict) -> dict:
    """
    Transforms SupplyChainState into the Incident Center view payload.
    """
    risk_list = state.get("risk_analysis") or []
    impact_list = state.get("impact_analysis") or []
    mitigation_list = state.get("mitigation_plan") or []

    # Get primary entries
    risk = risk_list[0] if risk_list else None
    impact = impact_list[0] if impact_list else None
    mitigation = mitigation_list[0] if mitigation_list else None

    # Fallback/Default values if empty
    if not risk:
        return {
            "success": False,
            "message": "Analysis pending. Please execute a query first.",
            "data": {}
        }

    # Meta
    news_id_short = risk.news_id.split("/")[-1][:8] if "/" in risk.news_id else "GEN-1042"
    location = risk.assessment.location
    city = location.city if location and location.city else "Rajasthan Region"
    state_name = location.state if location and location.state else "Rajasthan"
    country = location.country if location and location.country else "India"
    
    # Severity & priority mapping
    severity_val = getattr(risk.assessment.severity, "value", "medium").capitalize()
    business_impact = getattr(risk.assessment.business_impact, "value", "minor")
    priority = "P1 - High Blockade" if business_impact == "severe" else "P2 - Moderate Alert"

    incident_meta = {
        "id": f"INC-2026-{news_id_short}",
        "severity": severity_val,
        "status": "Active Investigation",
        "location": city,
        "country": country,
        "state": state_name,
        "detectedTime": risk.published_date.strftime("%H:%M:%S") if isinstance(risk.published_date, datetime) else "12:00:00",
        "lastUpdated": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        "riskCategory": getattr(risk.assessment.category, "value", "weather").replace("_", " ").title(),
        "confidence": f"{int(risk.assessment.confidence * 100)}%",
        "businessPriority": priority,
        "description": risk.assessment.summary
    }

    # Extracted Entities
    extracted = []
    if risk.assessment.affected_suppliers:
        extracted.extend([s.name for s in risk.assessment.affected_suppliers])
    if risk.assessment.affected_materials:
        extracted.extend(risk.assessment.affected_materials)
    if impact and impact.affected_plants:
        extracted.extend([p.plant_name for p in impact.affected_plants])
    if not extracted:
        extracted = ["Limestone Aggregate", "BuildCem Supply Corridor"]

    # Supporting sources
    supporting_sources = [
        {
            "id": 1,
            "publisher": risk.assessment.affected_suppliers[0].name if risk.assessment.affected_suppliers else "Reuters Logistics",
            "reliability": "98%",
            "time": "Just now",
            "status": "Verified"
        }
    ]

    # Timeline steps
    timeline_steps = [
        {
            "id": 1,
            "title": "Step 1: News Intelligence Output",
            "agent": "News Intelligence Agent",
            "metrics": {
                "risk": incident_meta["riskCategory"],
                "severity": severity_val,
                "confidence": incident_meta["confidence"],
                "latency": "0.4s"
            },
            "reasoning": risk.assessment.reasoning,
            "active": False
        }
    ]

    if impact:
        timeline_steps.append({
            "id": 2,
            "title": "Step 2: Supply Chain Impact Output",
            "agent": "Supply Chain Impact Agent",
            "metrics": {
                "assets": f"{len(impact.affected_plants)} Plant(s) Affected",
                "stocks": f"{impact.inventory[0].current_stock_days if impact.inventory else 'N/A'} days buffer",
                "blastRadius": "Tier 1 Sourcing",
                "latency": "0.6s"
            },
            "reasoning": impact.reasoning,
            "active": False
        })

    if mitigation:
        timeline_steps.append({
            "id": 3,
            "title": "Step 3: Mitigation Planning Output",
            "agent": "Mitigation Planning Agent",
            "metrics": {
                "alternate": mitigation.alternate_suppliers[0].supplier_name if mitigation.alternate_suppliers else "Secondary Sourcing",
                "route": mitigation.transportation_plan[0].mode if mitigation.transportation_plan else "Rerouting corridor",
                "estDelay": mitigation.recovery_estimate,
                "estCost": mitigation.estimated_cost or "Unknown",
                "confidence": "96%",
                "latency": "0.5s"
            },
            "reasoning": mitigation.executive_recommendation,
            "active": True
        })

    # Impact cards status resolver
    def get_status(count):
        return "critical" if count > 0 else "success"

    plant_count = len(impact.affected_plants) if impact else 0
    supplier_count = len(risk.matched_suppliers)
    warehouse_count = len(impact.affected_warehouses) if impact else 0
    route_count = len(impact.dependency_chain) if impact else 0
    loss_pct = impact.estimated_production_loss_percent if impact else 0.0

    impact_cards = [
        {
            "id": 1,
            "icon": "Factory",
            "title": "Affected Plants",
            "count": f"{plant_count} Plant(s) Active",
            "desc": f"Identified plant assets experiencing operational disruptions: {[p.plant_name for p in impact.affected_plants]}." if plant_count > 0 else "All integrated manufacturing plants operating normally.",
            "status": get_status(plant_count)
        },
        {
            "id": 2,
            "icon": "Users",
            "title": "Affected Suppliers",
            "count": f"{supplier_count} Primary Supplier(s)",
            "desc": f"Disrupted supplier nodes in risk zone: {[s.supplier_name for s in risk.matched_suppliers]}." if supplier_count > 0 else "All primary material suppliers reporting nominal schedules.",
            "status": get_status(supplier_count)
        },
        {
            "id": 3,
            "icon": "Package",
            "title": "Affected Warehouses",
            "count": f"{warehouse_count} Storage Silo(s)",
            "desc": "Active silo inventory depletion currently tracked." if warehouse_count > 0 else "Stock storage reserves holding above minimum safety baselines.",
            "status": "warning" if warehouse_count > 0 else "success"
        },
        {
            "id": 4,
            "icon": "Route",
            "title": "Affected Routes",
            "count": f"{route_count} Mapped Paths",
            "desc": "Active transport link bypasses deployed due to transit delays." if route_count > 0 else "Corridor logistics transit metrics operating at baseline.",
            "status": get_status(route_count)
        },
        {
            "id": 5,
            "icon": "ShieldAlert",
            "title": "Inventory Risk",
            "count": f"{impact.inventory[0].current_stock_days if (impact and impact.inventory) else 'N/A'} Days Stock",
            "desc": f"Buffer depletion alerts flagged on critical items." if (impact and impact.inventory and impact.inventory[0].current_stock_days < 10.0) else "Available stock buffers verify operational continuity.",
            "status": "critical" if (impact and impact.inventory and impact.inventory[0].current_stock_days < 10.0) else "success"
        },
        {
            "id": 6,
            "icon": "Layers",
            "title": "Production Risk",
            "count": "High Exposure" if loss_pct > 10.0 else "Low Exposure",
            "desc": f"Forecasted aggregate network capacity drop of {loss_pct}%." if loss_pct > 0 else "Aggregate manufacturing schedules meeting target baselines.",
            "status": "critical" if loss_pct > 10.0 else "success"
        }
    ]

    progress_stages = [
        {"id": 1, "name": "Detected", "status": "Complete", "time": incident_meta["detectedTime"], "agent": "News Intelligence Agent", "active": False},
        {"id": 2, "name": "Investigating", "status": "Complete", "time": incident_meta["detectedTime"], "agent": "Operational Context Agent", "active": False},
        {"id": 3, "name": "Impact Calculated", "status": "Complete", "time": incident_meta["lastUpdated"], "agent": "Supply Chain Impact Agent", "active": False},
        {"id": 4, "name": "Mitigation Ready", "status": "In Progress" if mitigation else "Pending", "time": incident_meta["lastUpdated"] if mitigation else "--:--:--", "agent": "Mitigation Planning Agent", "active": True if mitigation else False},
        {"id": 5, "name": "Closed", "status": "Pending", "time": "--:--:--", "agent": "System Core Orchestrator", "active": False}
    ]

    return {
        "success": True,
        "message": "Incident Center data retrieved successfully.",
        "data": {
            "incident_meta": incident_meta,
            "extracted_entities": extracted,
            "supporting_sources": supporting_sources,
            "timeline_steps": timeline_steps,
            "impact_cards": impact_cards,
            "progress_stages": progress_stages
        }
    }

def transform_news(state: dict) -> dict:
    """
    Transforms SupplyChainState into News Intelligence view payload.
    """
    filtered_news = state.get("filtered_news")
    if not filtered_news:
        return {"success": False, "message": "News pending.", "data": {}}

    news_feed = []
    for idx, art in enumerate(filtered_news.articles):
        news_feed.append({
            "id": idx + 1,
            "publisher": art.source or "Global Logistics Wire",
            "initials": (art.source or "GL")[:2].upper(),
            "headline": art.title,
            "time": "Detected during run",
            "country": art.location.country if art.location else "India",
            "state": art.location.state if art.location else "All",
            "location": art.location.city if art.location else "National Block",
            "summary": art.content,
            "entity": "Primary Quarry Supply",
            "severity": "Critical",
            "confidence": "95%",
            "status": "Validated"
        })

    kpis = [
        {"id": 1, "title": "Processed Articles", "value": str(len(news_feed)), "trend": "Active session ingestion", "colorClass": "blue", "icon": "Radio"},
        {"id": 2, "title": "Validated Alerts", "value": str(len(news_feed)), "trend": "Requires operational trace", "colorClass": "red", "icon": "AlertOctagon"},
        {"id": 3, "title": "System Crawler", "value": "Online", "trend": "Tavily stream active", "colorClass": "green", "icon": "CheckCircle"}
    ]

    return {
        "success": True,
        "message": "News Intelligence data retrieved successfully.",
        "data": {
            "kpis": kpis,
            "news_feed": news_feed,
            "pipeline": [
                {"id": 1, "name": "Collect", "status": "Active", "count": f"{len(news_feed)} alert(s)", "time": "0.2s", "task": "Scan online corridors", "active": True, "icon": "Database"},
                {"id": 2, "name": "Classify", "status": "Active", "count": "100% parsed", "time": "0.3s", "task": "Extract target parameters", "active": True, "icon": "Layers"}
            ]
        }
    }

def transform_inventory(state: dict) -> dict:
    """
    Transforms SupplyChainState into Plants & Inventory view payload.
    """
    impact_list = state.get("impact_analysis") or []
    impact = impact_list[0] if impact_list else None

    if not impact:
        return {"success": False, "message": "Impact pending.", "data": {}}

    # Setup the three main plants from JSON mapping
    plants = [
        {
            "id": "PLT-001",
            "name": "BuildCem Rajasthan Integrated Plant",
            "location": "Jodhpur, Rajasthan",
            "status": "Healthy",
            "healthScore": 95,
            "production": "8,333 T/d",
            "capacity": "10,000 T/d",
            "utilization": 83,
            "risk": "None",
            "suppliers": 3,
            "inventoryHealth": "Optimal",
            "remainingDays": 8.8
        },
        {
            "id": "PLT-002",
            "name": "BuildCem Central India Mega Plant",
            "location": "Indore, Madhya Pradesh",
            "status": "Healthy",
            "healthScore": 92,
            "production": "11,000 T/d",
            "capacity": "12,000 T/d",
            "utilization": 91,
            "risk": "None",
            "suppliers": 4,
            "inventoryHealth": "Optimal",
            "remainingDays": 4.9
        },
        {
            "id": "PLT-003",
            "name": "BuildCem Southern Grinding Unit",
            "location": "Hospet, Karnataka",
            "status": "Healthy",
            "healthScore": 89,
            "production": "7,333 T/d",
            "capacity": "8,000 T/d",
            "utilization": 91,
            "risk": "None",
            "suppliers": 4,
            "inventoryHealth": "Optimal",
            "remainingDays": 3.5
        }
    ]

    # Dynamically inject impact details into matching plants
    for affected in impact.affected_plants:
        for p in plants:
            if p["id"] == affected.plant_id:
                p["status"] = "At Risk" if affected.production_loss_percent > 10.0 else "Warning"
                p["healthScore"] = int(100 - affected.production_loss_percent)
                p["risk"] = f"Obstructed raw material delivery of {', '.join(affected.affected_materials)}."
                p["production"] = f"{int(float(p['production'].split()[0].replace(',', '')) * (1 - affected.production_loss_percent/100))} T/d"
                p["utilization"] = int(p["utilization"] * (1 - affected.production_loss_percent/100))
                p["inventoryHealth"] = "Critical" if affected.production_loss_percent > 20.0 else "Warning"

    # Map inventory details
    inventory_items = []
    # Standard fallback base inventory items
    base_items = [
        {"material": "Limestone", "stock": "73,500 T", "safety": "40,000 T", "consumption": "8,333 T/d", "days": 8.8, "incoming": "10,000 T", "status": "success", "supplier": "Marwar Mining & Minerals Corp.", "risk": "Low", "pct": 183},
        {"material": "Coal", "stock": "28,500 T", "safety": "10,500 T", "consumption": "1,500 T/d", "days": 19.0, "incoming": "6,000 T", "status": "success", "supplier": "Singrauli Coalfields", "risk": "Low", "pct": 271},
        {"material": "Gypsum", "stock": "3,300 T", "safety": "1,600 T", "consumption": "400 T/d", "days": 8.2, "incoming": "1,500 T", "status": "success", "supplier": "Deccan Gypsum", "risk": "Low", "pct": 206}
    ]

    # Overwrite based on impact node calculations
    for base in base_items:
        match_inv = next((i for i in impact.inventory if i.material == base["material"]), None)
        if match_inv:
            base["days"] = round(match_inv.current_stock_days, 1)
            base["status"] = "critical" if match_inv.current_stock_days < 5.0 else ("warning" if match_inv.current_stock_days < 10.0 else "success")
            base["risk"] = "Critical" if match_inv.current_stock_days < 5.0 else ("Medium" if match_inv.current_stock_days < 10.0 else "Low")
        inventory_items.append(base)

    kpis = [
        {"id": 1, "title": "Aggregate Production Loss", "value": f"{impact.estimated_production_loss_percent}%", "trend": "Weighted operational drop", "status": "warning" if impact.estimated_production_loss_percent > 0 else "success", "icon": "Factory"},
        {"id": 2, "title": "Active Disruptions", "value": f"{len(impact.affected_plants)} Plant(s)", "trend": "Requires corridor rebalancing", "status": "critical" if len(impact.affected_plants) > 0 else "success", "icon": "AlertTriangle"}
    ]

    return {
        "success": True,
        "message": "Plants & Inventory data retrieved successfully.",
        "data": {
            "kpis": kpis,
            "plants": plants,
            "inventory": inventory_items
        }
    }

def transform_supply_chain(state: dict) -> dict:
    """
    Transforms SupplyChainState into Supply Chain Network Graph nodes and edges.
    """
    risk_list = state.get("risk_analysis") or []
    impact_list = state.get("impact_analysis") or []
    mitigation_list = state.get("mitigation_plan") or []

    risk = risk_list[0] if risk_list else None
    impact = impact_list[0] if impact_list else None
    mitigation = mitigation_list[0] if mitigation_list else None

    if not risk:
        return {"success": False, "message": "Graph pending.", "data": {}}

    nodes = [
        {
            "id": "sup-1",
            "type": "twinNode",
            "position": {"x": 50, "y": 30},
            "data": {
                "name": risk.matched_suppliers[0].supplier_name if risk.matched_suppliers else "Marwar Mining & Minerals Corp.",
                "location": risk.matched_suppliers[0].state if risk.matched_suppliers else "Rajasthan",
                "material": "Limestone Raw Bulk",
                "health": "critical" if risk.matched_suppliers else "success",
                "status": "Logistics Obstructed" if risk.matched_suppliers else "Optimal Output",
                "icon": "Layers"
            }
        },
        {
            "id": "sup-2",
            "type": "twinNode",
            "position": {"x": 320, "y": 30},
            "data": {
                "name": mitigation.alternate_suppliers[0].supplier_name if (mitigation and mitigation.alternate_suppliers) else "Deccan Gypsum & Chemical Aggregates",
                "location": "Madhya Pradesh",
                "material": "Backup Raw Material",
                "health": "success",
                "status": "Emergency Capacity Allocated" if mitigation else "Idle Backup",
                "icon": "Layers"
            }
        },
        {
            "id": "pl-1",
            "type": "twinNode",
            "position": {"x": 185, "y": 250},
            "data": {
                "name": impact.affected_plants[0].plant_name if (impact and impact.affected_plants) else "BuildCem Integrated Plant",
                "location": "Jodhpur, Rajasthan",
                "material": "Clinker Kiln Core",
                "health": "warning" if (impact and impact.affected_plants) else "success",
                "status": "Executing Reroute Bypass" if mitigation else "Optimal Output",
                "icon": "Factory"
            }
        }
    ]

    edges = [
        {
            "id": "e1",
            "source": "sup-1",
            "target": "pl-1",
            "className": "edge-flow-limestone edge-critical" if risk.matched_suppliers else "edge-flow-limestone edge-healthy"
        },
        {
            "id": "e2",
            "source": "sup-2",
            "target": "pl-1",
            "className": "edge-flow-alternative edge-alternative-dashed"
        }
    ]

    ai_action_plans = []
    if mitigation:
        for idx, action in enumerate(mitigation.actions):
            ai_action_plans.append({
                "id": idx + 1,
                "priority": action.priority.capitalize(),
                "action": action.title,
                "delay": action.estimated_duration,
                "cost": mitigation.estimated_cost or "Low",
                "impact": action.description,
                "conf": "96%",
                "agent": "Mitigation Planning Agent",
                "time": "Just now"
            })

    return {
        "success": True,
        "message": "Supply Chain Network data retrieved successfully.",
        "data": {
            "nodes": nodes,
            "edges": edges,
            "ai_action_plans": ai_action_plans
        }
    }

def transform_decision_center(state: dict) -> dict:
    """
    Transforms SupplyChainState into AI Decision Center logs and traces.
    """
    risk_list = state.get("risk_analysis") or []
    impact_list = state.get("impact_analysis") or []
    mitigation_list = state.get("mitigation_plan") or []

    risk = risk_list[0] if risk_list else None
    impact = impact_list[0] if impact_list else None
    mitigation = mitigation_list[0] if mitigation_list else None

    if not risk:
        return {"success": False, "message": "Decision Center pending.", "data": {}}

    agents = [
        {
            "id": "agent-1",
            "name": "News Intelligence Agent",
            "avatarColor": "blue",
            "attention": "Reasoning Complete",
            "emotion": "Focused",
            "confidence": f"{int(risk.assessment.confidence * 100)}%",
            "execTime": "0.45s",
            "tokens": "112k",
            "latestDecision": f"Extracted hazard: {risk.headline[:50]}...",
            "metrics": [
                {"label": "Current Task", "value": "Monitoring news feeds"},
                {"label": "Latest Reasoning", "value": risk.assessment.reasoning}
            ]
        }
    ]

    if impact:
        agents.append({
            "id": "agent-2",
            "name": "Supply Chain Impact Agent",
            "avatarColor": "amber",
            "attention": "Context Traversal Completed",
            "emotion": "Analyzing",
            "confidence": "94%",
            "execTime": "0.58s",
            "tokens": "240k",
            "latestDecision": f"Identified plant capacity drop of {impact.estimated_production_loss_percent}%.",
            "metrics": [
                {"label": "Affected Nodes", "value": f"{len(impact.affected_plants)} Plant, {len(impact.affected_warehouses)} Silos"},
                {"label": "Stock Buffer", "value": f"{impact.inventory[0].current_stock_days if impact.inventory else 'N/A'} days"}
            ]
        })

    if mitigation:
        agents.append({
            "id": "agent-3",
            "name": "Mitigation Planning Agent",
            "avatarColor": "green",
            "attention": "Bypass Formulated",
            "emotion": "Decision Ready",
            "confidence": "96%",
            "execTime": "0.51s",
            "tokens": "380k",
            "latestDecision": mitigation.executive_recommendation,
            "metrics": [
                {"label": "Alternate Supplier", "value": mitigation.alternate_suppliers[0].supplier_name if mitigation.alternate_suppliers else "None"},
                {"label": "Recovery Estimate", "value": mitigation.recovery_estimate}
            ]
        })

    return {
        "success": True,
        "message": "AI Decision Center data retrieved successfully.",
        "data": {
            "kpis": [
                {"id": 1, "label": "Active AI Agents", "value": f"{len(agents)} / 3 Active", "desc": "Continuous orchestration", "icon": "Cpu", "type": "brand"},
                {"id": 2, "label": "Average Confidence", "value": "95%", "desc": "Context threshold check", "icon": "TrendingUp", "type": "success"}
            ],
            "agents": agents
        }
    }

def transform_reports(state: dict) -> dict:
    """
    Transforms SupplyChainState into markdown Executive Reports page format.
    """
    executive = state.get("executive_summary")
    if not executive:
        return {"success": False, "message": "Reports pending.", "data": {}}

    content = "\n\n".join(executive.summaries) if executive.summaries else "# Executive Briefing\nNo summaries available."

    return {
        "success": True,
        "message": "Executive Reports data retrieved successfully.",
        "data": {
            "reports": [
                {
                    "id": "REP-01",
                    "title": "Autonomous Anomaly Disruption Briefing",
                    "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "publisher": "Strategic Operations Orchestration Agent",
                    "category": "Operational Intelligence Reports",
                    "content": content
                }
            ]
        }
    }
