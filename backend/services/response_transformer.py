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

    filtered_news = state.get("filtered_news")
    original_body = ""
    if filtered_news and filtered_news.articles:
        matching_article = next((a for a in filtered_news.articles if a.title == risk.headline), None)
        if matching_article:
            original_body = matching_article.content
    if not original_body:
        original_body = risk.assessment.summary

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
        "description": risk.assessment.summary,
        "originalHeadline": risk.headline,
        "originalBody": original_body
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
            "reliability": incident_meta["confidence"],
            "time": "Detected during run",
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

    classified_events = []
    risk_list = state.get("risk_analysis") or []
    for r_idx, r in enumerate(risk_list):
        category_name = getattr(r.assessment.category, "value", "weather").replace("_", " ").title()
        severity_name = getattr(r.assessment.severity, "value", "medium").upper()
        classified_events.append({
            "id": r_idx + 1,
            "time": r.published_date.strftime("%H:%M:%S") if isinstance(r.published_date, datetime) else "12:00:00",
            "type": f"{category_name} Disruption ({severity_name})",
            "detail": f"{r.headline} - {r.assessment.summary[:100]}..."
        })

    status = {
        "global_regions": [
            {"name": "Asia Pacific (APAC)", "status": "success", "sources": "128", "coverage": "99.8%", "event": "Nominal operational logs"},
            {"name": "Europe & MEA", "status": "success", "sources": "92", "coverage": "99.4%", "event": "Nominal logistics flow"},
            {"name": "Americas Corridor", "status": "success", "sources": "146", "coverage": "99.9%", "event": "Nominal route check"}
        ],
        "india_regions": [
            {"name": "Western Sourcing Block", "status": "warning" if len(news_feed) > 0 else "success", "sources": "64", "coverage": "98.7%", "event": news_feed[0]["headline"] if len(news_feed) > 0 else "Nominal output"},
            {"name": "Central Transit Segment", "status": "success", "sources": "48", "coverage": "99.2%", "event": "Nominal tracking active"},
            {"name": "Southern Port Terminals", "status": "success", "sources": "54", "coverage": "99.6%", "event": "Nominal logistics flow"}
        ],
        "system_services": [
            {"name": "NewsIngestionAgent", "status": "success"},
            {"name": "TavilySearchAPI", "status": "success"},
            {"name": "RiskGradeAgent", "status": "success"},
            {"name": "OrchestratorNode", "status": "success"}
        ]
    }

    analytics = {
        "most_active_sources": [
            {"name": "Reuters Logistics", "articles": "4"},
            {"name": "India Transit Wire", "articles": "3"},
            {"name": "Global Sourcing Hub", "articles": "2"}
        ],
        "refresh_metrics": {
            "global_crawl_time": "0.45s",
            "polling_frequency": "5m standard",
            "success_rate": "100.0%"
        },
        "collection_latency": {
            "ingestion_latency": "1.2s",
            "fastest_pipeline": "0.15s (Filter)",
            "slowest_edge": "0.85s (LLM)"
        },
        "coverage_summary": {
            "countries_monitored": "12",
            "indian_states_mapped": "28",
            "reliability_rating": "99.4%"
        }
    }

    return {
        "success": True,
        "message": "News Intelligence data retrieved successfully.",
        "data": {
            "kpis": kpis,
            "news_feed": news_feed,
            "classified_events": classified_events,
            "status": status,
            "analytics": analytics,
            "pipeline": [
                {"id": 1, "name": "Collect", "status": "Active", "count": f"{len(news_feed)} alert(s)", "time": "0.2s", "task": "Scan online corridors", "active": True, "icon": "Database"},
                {"id": 2, "name": "Classify", "status": "Active", "count": "100% parsed", "time": "0.3s", "task": "Extract target parameters", "active": True, "icon": "Layers"}
            ]
        }
    }

def transform_news_from_scan(news_feed: list[dict]) -> dict:
    """
    Transforms scanned news feed items into News Intelligence view payload.
    """
    # Calculate KPIs
    kpis = [
        {"id": 1, "title": "Processed Articles", "value": str(len(news_feed)), "trend": "Active session ingestion", "colorClass": "blue", "icon": "Radio"},
        {"id": 2, "title": "Validated Alerts", "value": str(len([n for n in news_feed if n["severity"] in ("CRITICAL", "HIGH", "Critical", "High")])), "trend": "Requires operational trace", "colorClass": "red", "icon": "AlertOctagon"},
        {"id": 3, "title": "System Crawler", "value": "Online", "trend": "Tavily stream active", "colorClass": "green", "icon": "CheckCircle"}
    ]
    
    # Extract classified events from scan
    classified_events = []
    for idx, item in enumerate(news_feed):
        category_name = item.get("category", "weather").replace("_", " ").title()
        severity_name = item.get("severity", "MEDIUM").upper()
        classified_events.append({
            "id": idx + 1,
            "time": "12:00:00",
            "type": f"{category_name} Disruption ({severity_name})",
            "detail": f"{item['headline']} - {item['summary'][:100]}..."
        })
        
    status = {
        "global_regions": [
            {"name": "Asia Pacific (APAC)", "status": "success", "sources": "128", "coverage": "99.8%", "event": "Nominal operational logs"},
            {"name": "Europe & MEA", "status": "success", "sources": "92", "coverage": "99.4%", "event": "Nominal logistics flow"},
            {"name": "Americas Corridor", "status": "success", "sources": "146", "coverage": "99.9%", "event": "Nominal route check"}
        ],
        "india_regions": [
            {"name": "Western Sourcing Block", "status": "warning" if len(news_feed) > 0 else "success", "sources": "64", "coverage": "98.7%", "event": news_feed[0]["headline"] if len(news_feed) > 0 else "Nominal output"},
            {"name": "Central Transit Segment", "status": "success", "sources": "48", "coverage": "99.2%", "event": "Nominal tracking active"},
            {"name": "Southern Port Terminals", "status": "success", "sources": "54", "coverage": "99.6%", "event": "Nominal logistics flow"}
        ],
        "system_services": [
            {"name": "NewsIngestionAgent", "status": "success"},
            {"name": "TavilySearchAPI", "status": "success"},
            {"name": "RiskGradeAgent", "status": "success"},
            {"name": "OrchestratorNode", "status": "success"}
        ]
    }
    
    analytics = {
        "most_active_sources": [
            {"name": "Reuters Logistics", "articles": "4"},
            {"name": "India Transit Wire", "articles": "3"},
            {"name": "Global Sourcing Hub", "articles": "2"}
        ],
        "refresh_metrics": {
            "global_crawl_time": "0.45s",
            "polling_frequency": "5m standard",
            "success_rate": "100.0%"
        },
        "collection_latency": {
            "ingestion_latency": "1.2s",
            "fastest_pipeline": "0.15s (Filter)",
            "slowest_edge": "0.85s (LLM)"
        },
        "coverage_summary": {
            "countries_monitored": "12",
            "indian_states_mapped": "28",
            "reliability_rating": "99.4%"
        }
    }
    
    return {
        "success": True,
        "message": "News Intelligence data retrieved successfully.",
        "data": {
            "kpis": kpis,
            "news_feed": news_feed,
            "classified_events": classified_events,
            "status": status,
            "analytics": analytics,
            "last_scan": datetime.now(timezone.utc).strftime("%I:%M %p"),
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
    mitigation_list = state.get("mitigation_plan") or []
    risk_list = state.get("risk_analysis") or []

    impact = impact_list[0] if impact_list else None
    mitigation = mitigation_list[0] if mitigation_list else None
    risk = risk_list[0] if risk_list else None

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

    limestone_days = 8.8
    coal_days = 19.0
    gypsum_days = 8.2
    if impact and impact.inventory:
        lim_inv = next((i for i in impact.inventory if i.material == "Limestone"), None)
        if lim_inv:
            limestone_days = round(lim_inv.current_stock_days, 1)
        coal_inv = next((i for i in impact.inventory if i.material == "Coal"), None)
        if coal_inv:
            coal_days = round(coal_inv.current_stock_days, 1)
        gyp_inv = next((i for i in impact.inventory if i.material == "Gypsum"), None)
        if gyp_inv:
            gypsum_days = round(gyp_inv.current_stock_days, 1)

    limestone_stock = int(limestone_days * 8333)
    coal_stock = int(coal_days * 1500)
    gypsum_stock = int(gypsum_days * 400)

    # production_trend
    production_trend = []
    affected_plant_a = next((p for p in impact.affected_plants if p.plant_id == "PLT-001"), None)
    loss_pct_a = affected_plant_a.production_loss_percent if affected_plant_a else 0.0
    affected_plant_b = next((p for p in impact.affected_plants if p.plant_id == "PLT-002"), None)
    loss_pct_b = affected_plant_b.production_loss_percent if affected_plant_b else 0.0

    for hr in ["08:00", "10:00", "12:00", "14:00", "16:00"]:
        production_trend.append({
            "name": hr,
            "PlantA": int(350 * (1 - loss_pct_a / 100)),
            "PlantB": int(460 * (1 - loss_pct_b / 100))
        })

    # inventory_consumption
    inventory_consumption = [
        {"name": "Limestone", "Current": limestone_stock, "Safety": 40000},
        {"name": "Coal", "Current": coal_stock, "Safety": 10500},
        {"name": "Gypsum", "Current": gypsum_stock, "Safety": 1600}
    ]

    # capacity_utilization
    capacity_utilization = [
        {"name": p["name"], "value": p["utilization"], "fill": "#B15A52" if idx==0 else ("#708C72" if idx==1 else "#3E556B")}
        for idx, p in enumerate(plants)
    ]

    # material_availability
    material_availability = [
        {"name": "Limestone", "value": limestone_days},
        {"name": "Coal", "value": coal_days},
        {"name": "Gypsum", "value": gypsum_days}
    ]

    # ai_insights
    ai_insights = []
    if mitigation:
        for idx, action in enumerate(mitigation.actions):
            ai_insights.append({
                "priority": action.priority.upper(),
                "agent": "Mitigation Planning Agent",
                "title": action.title,
                "impact": action.description[:40] + "...",
                "delay": action.estimated_duration,
                "action": action.description
            })

    return {
        "success": True,
        "message": "Plants & Inventory data retrieved successfully.",
        "data": {
            "kpis": kpis,
            "plants": plants,
            "inventory": inventory_items,
            "production_trend": production_trend,
            "inventory_consumption": inventory_consumption,
            "capacity_utilization": capacity_utilization,
            "material_availability": material_availability,
            "ai_insights": ai_insights
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

    # Helper function to load data JSONs dynamically
    import json
    from pathlib import Path
    
    def load_db_json(relative_path: str) -> dict:
        data_dir = Path(__file__).resolve().parent.parent / "data"
        full_path = data_dir / relative_path
        if not full_path.exists():
            logger.warning("Data file not found: %s", full_path)
            return {}
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Load dynamic configurations
    suppliers_list = load_db_json("suppliers/suppliers.json").get("suppliers", [])
    materials_list = load_db_json("materials/materials.json").get("materials", [])
    plants_list = load_db_json("plants/plants.json").get("plants", [])
    dcs_list = load_db_json("distribution/distribution_centers.json").get("distribution_centers", [])

    # Turn lists into dict mappings for easy reference
    supplier_nodes_info = {}
    for s in suppliers_list:
        supplier_nodes_info[s["supplier_id"]] = {
            "name": s["supplier_name"],
            "location": f"{s['city']}, {s['state']}",
            "material": " & ".join([m.split("-")[-1] for m in s.get("materials", [])]), 
            "capacity": f"{int(s['daily_supply_capacity_tons']):,} Tons/day" if s.get("daily_supply_capacity_tons") else "N/A",
            "reliability": f"{s['reliability_score']}%" if s.get("reliability_score") else "N/A",
            "lead_time": f"{s['lead_time_days']} Days" if s.get("lead_time_days") else "N/A",
            "transport": s.get("preferred_transport", "Road"),
            "icon": "Layers"
        }

    material_nodes_info = {}
    for m in materials_list:
        if m["material_id"] not in ["MAT-LMS-01", "MAT-GYP-03", "MAT-COL-02", "MAT-FLA-04"]:
            continue
        material_nodes_info[m["material_id"]] = {
            "name": f"{m['material_name']} Feedstock",
            "location": m.get("storage_method", "Storage Silo"),
            "material": m["material_name"],
            "criticality": m["criticality"].capitalize(),
            "monthly_req": f"{int(m.get('minimum_storage_days', 10) * 10000):,} Tons",
            "icon": "Layers"
        }
    if "MAT-LMS-01" in material_nodes_info:
        material_nodes_info["MAT-LMS-01"]["monthly_req"] = "250,000 Tons"
    if "MAT-GYP-03" in material_nodes_info:
        material_nodes_info["MAT-GYP-03"]["monthly_req"] = "12,000 Tons"
    if "MAT-COL-02" in material_nodes_info:
        material_nodes_info["MAT-COL-02"]["monthly_req"] = "45,000 Tons"
    if "MAT-FLA-04" in material_nodes_info:
        material_nodes_info["MAT-FLA-04"]["monthly_req"] = "35,000 Tons"

    plant_nodes_info = {}
    for p in plants_list:
        plant_nodes_info[p["plant_id"]] = {
            "name": p["plant_name"],
            "location": f"{p['city']}, {p['state']}",
            "material": "Clinker Kiln Core",
            "capacity": f"{int(p['production_capacity_tpd']):,} Tons/day" if p.get("production_capacity_tpd") else "N/A",
            "utilization": f"{int((p.get('current_daily_production_tpd', 1000) / p.get('production_capacity_tpd', 1200)) * 100)}%",
            "lines": f"{len(p.get('production_lines', []))} Active Kilns",
            "icon": "Factory"
        }

    dc_nodes_info = {}
    for d in dcs_list:
        dc_nodes_info[d["distribution_center_id"]] = {
            "name": d["distribution_center_name"],
            "location": f"{d['city']}, {d['state']}",
            "material": "Packed Cement Bags",
            "capacity": f"{int(d.get('daily_dispatch_capacity', {}).get('value', 0)):,} Tons/day",
            "regions": ", ".join(d.get("supported_regions", [])[:2]),
            "icon": "Package"
        }

    customer_nodes_info = {
        "CUST-NCR": {"name": "Northern Demand Hub", "location": "NCR & Punjab Region", "material": "Cement Commercial Demand", "capacity": "10,500 Tons/day Demand", "regions": "Haryana, Punjab, Delhi", "icon": "Globe"},
        "CUST-WEST": {"name": "Western Demand Hub", "location": "Gujarat & Mumbai Region", "material": "Cement Commercial Demand", "capacity": "14,000 Tons/day Demand", "regions": "Gujarat, Maharashtra", "icon": "Globe"},
        "CUST-SOUTH": {"name": "Southern Demand Hub", "location": "Bengaluru & Chennai Region", "material": "Cement Commercial Demand", "capacity": "9,500 Tons/day Demand", "regions": "Karnataka, Tamil Nadu, AP", "icon": "Globe"}
    }

    # Evaluate dynamic simulation states
    matched_supplier_ids = []
    if risk:
        matched_supplier_ids = [s.supplier_id for s in risk.matched_suppliers] if risk.matched_suppliers else []
        if risk.assessment.affected_suppliers:
            for s in risk.assessment.affected_suppliers:
                # Match by name if ID is missing in affected supplier models
                for sid, info in supplier_nodes_info.items():
                    if s.name.lower() in info["name"].lower() and sid not in matched_supplier_ids:
                        matched_supplier_ids.append(sid)

    affected_materials = []
    if risk and risk.assessment.affected_materials:
        affected_materials = [m.lower() for m in risk.assessment.affected_materials]

    affected_plants = []
    if impact and impact.affected_plants:
        affected_plants = [p.plant_id for p in impact.affected_plants]

    alternate_suppliers = []
    if mitigation and mitigation.alternate_suppliers:
        alternate_suppliers = [s.supplier_id for s in mitigation.alternate_suppliers]

    nodes = []

    # 1. Suppliers
    for idx, (sid, info) in enumerate(supplier_nodes_info.items()):
        health = "success"
        status = "Nominal Operations"
        if sid in matched_supplier_ids:
            health = "critical"
            status = "Logistics Obstructed"
        elif sid in alternate_suppliers:
            health = "success"
            status = "Emergency Capacity Engaged"

        nodes.append({
            "id": sid,
            "type": "twinNode",
            "position": {"x": 50, "y": 50 + idx * 130},
            "data": {
                "name": info["name"],
                "location": info["location"],
                "node_type": "supplier",
                "material": info["material"],
                "capacity": info["capacity"],
                "reliability": info["reliability"],
                "lead_time": info["lead_time"],
                "transport": info["transport"],
                "health": health,
                "status": status,
                "icon": info["icon"]
            }
        })

    # 2. Materials
    for idx, (mid, info) in enumerate(material_nodes_info.items()):
        health = "success"
        status = "Stock Buffer Optimal"

        is_affected = False
        if mid == "MAT-LMS-01" and any("lime" in m for m in affected_materials):
            is_affected = True
        elif mid == "MAT-GYP-03" and any("gyp" in m for m in affected_materials):
            is_affected = True
        elif mid == "MAT-COL-02" and any("coal" in m for m in affected_materials):
            is_affected = True
        elif mid == "MAT-FLA-04" and any("ash" in m for m in affected_materials):
            is_affected = True

        if is_affected:
            health = "warning"
            status = "Inventory Drawdown Alert"

        nodes.append({
            "id": mid,
            "type": "twinNode",
            "position": {"x": 320, "y": 80 + idx * 130},
            "data": {
                "name": info["name"],
                "location": info["location"],
                "node_type": "material",
                "material": info["material"],
                "criticality": info["criticality"],
                "monthly_req": info["monthly_req"],
                "health": health,
                "status": status,
                "icon": info["icon"]
            }
        })

    # 3. Plants
    for idx, (pid, info) in enumerate(plant_nodes_info.items()):
        health = "success"
        status = "Optimal Output"
        if pid in affected_plants:
            health = "warning"
            loss_pct = 15.0
            if impact and impact.affected_plants:
                loss_pct = next((p.production_loss_percent for p in impact.affected_plants if p.plant_id == pid), 15.0)
            status = f"Disrupted: {loss_pct}% Output Drop"
            if alternate_suppliers:
                status = "Alternate Sourcing Bypass Active"

        nodes.append({
            "id": pid,
            "type": "twinNode",
            "position": {"x": 590, "y": 120 + idx * 140},
            "data": {
                "name": info["name"],
                "location": info["location"],
                "node_type": "plant",
                "material": info["material"],
                "capacity": info["capacity"],
                "utilization": info["utilization"],
                "lines": info["lines"],
                "health": health,
                "status": status,
                "icon": info["icon"]
            }
        })

    # 4. Distribution Centers
    for idx, (dcid, info) in enumerate(dc_nodes_info.items()):
        health = "success"
        status = "Nominal Dispatch"
        connected_plant = "PLT-001" if dcid == "DBC-001" else ("PLT-002" if dcid == "DBC-002" else "PLT-003")
        if connected_plant in affected_plants:
            status = "Reduced Upstream Supply Stream"

        nodes.append({
            "id": dcid,
            "type": "twinNode",
            "position": {"x": 860, "y": 120 + idx * 140},
            "data": {
                "name": info["name"],
                "location": info["location"],
                "node_type": "distribution_center",
                "material": info["material"],
                "capacity": info["capacity"],
                "regions": info["regions"],
                "health": health,
                "status": status,
                "icon": info["icon"]
            }
        })

    # 5. Customers
    for idx, (cid, info) in enumerate(customer_nodes_info.items()):
        nodes.append({
            "id": cid,
            "type": "twinNode",
            "position": {"x": 1130, "y": 120 + idx * 140},
            "data": {
                "name": info["name"],
                "location": info["location"],
                "node_type": "customer",
                "material": info["material"],
                "capacity": info["capacity"],
                "regions": info["regions"],
                "health": "success",
                "status": "Nominal Demand Met",
                "icon": info["icon"]
            }
        })

    # Compile Edges dynamically with dynamic state mapping
    edges = []

    # A. Supplier -> Material
    supplier_material_links = [
        ("SUP-001", "MAT-LMS-01", "primary"),
        ("SUP-001", "MAT-COL-02", "primary"),
        ("SUP-002", "MAT-LMS-01", "backup"),
        ("SUP-002", "MAT-GYP-03", "primary"),
        ("SUP-003", "MAT-COL-02", "primary"),
        ("SUP-003", "MAT-FLA-04", "primary"),
        ("SUP-004", "MAT-GYP-03", "backup"),
        ("SUP-004", "MAT-FLA-04", "primary"),
        ("SUP-005", "MAT-FLA-04", "backup")
    ]
    for s_id, m_id, role in supplier_material_links:
        edge_id = f"e-{s_id}-{m_id}"
        is_disrupted = (s_id in matched_supplier_ids)
        is_mitigating = (s_id in alternate_suppliers)
        
        cname = "edge-flow-inactive"
        animated = False
        
        if not is_disrupted:
            if role == "primary":
                cname = "edge-flow-limestone edge-healthy" if m_id == "MAT-LMS-01" else ("edge-flow-coal edge-healthy" if m_id == "MAT-COL-02" else "edge-flow-gypsum edge-healthy")
                animated = True
            elif is_mitigating:
                cname = "edge-recovered"
                animated = True
        else:
            cname = "edge-critical"
            animated = False

        edges.append({
            "id": edge_id,
            "source": s_id,
            "target": m_id,
            "className": cname,
            "animated": animated,
            "data": {
                "name": f"Sourcing Vector ({role.capitalize()})",
                "mode": "Industrial Conveyor / Internal Yard",
                "distance": "1.2 km Yard Transfer",
                "time": "Immediate Transit",
                "capacity": "25,000 Tons/day",
                "reliability": "99.8%",
                "cost": "Included in standard contract",
                "status": "Nominal Sourcing" if not is_disrupted else "Vector Blocked due to Supplier Disruption"
            }
        })

    # B. Material -> Plant (Logistics corridors)
    routes_definitions = {
        "e-MAT-LMS-01-PLT-001": {
            "source": "MAT-LMS-01", "target": "PLT-001", "mode": "Rail", 
            "name": "Rajasthan Limestone Rail Corridor (NH-62 Segment)", 
            "distance": "260 km", "time": "5.5 Hours", "capacity": "15,000 Tons/day", 
            "reliability": "94.5%", "cost": "$650/Ton", "material": "Limestone", "type": "primary"
        },
        "e-MAT-LMS-01-PLT-001-BYPASS": {
            "source": "MAT-LMS-01", "target": "PLT-001", "mode": "Road", 
            "name": "NH-48 Emergency Sourcing Bypass Corridor", 
            "distance": "380 km (Detour)", "time": "8.5 Hours", "capacity": "8,000 Tons/day", 
            "reliability": "96.0% (Secured)", "cost": "$820/Ton", "material": "Limestone", "type": "bypass"
        },
        "e-MAT-GYP-03-PLT-001": {
            "source": "MAT-GYP-03", "target": "PLT-001", "mode": "Road", 
            "name": "Indore-Chittorgarh Highway Route (NH-27)", 
            "distance": "390 km", "time": "8.0 Hours", "capacity": "4,000 Tons/day", 
            "reliability": "91.2%", "cost": "$780/Ton", "material": "Gypsum", "type": "primary"
        },
        "e-MAT-GYP-03-PLT-002": {
            "source": "MAT-GYP-03", "target": "PLT-002", "mode": "Road", 
            "name": "Jabalpur-Satna Gypsum Freight Corridor (NH-30)", 
            "distance": "170 km", "time": "3.5 Hours", "capacity": "10,000 Tons/day", 
            "reliability": "95.0%", "cost": "$450/Ton", "material": "Gypsum", "type": "primary"
        },
        "e-MAT-COL-02-PLT-002": {
            "source": "MAT-COL-02", "target": "PLT-002", "mode": "Rail", 
            "name": "Singrauli Coal Belt Rail Corridor", 
            "distance": "360 km", "time": "10.5 Hours", "capacity": "12,000 Tons/day", 
            "reliability": "96.8%", "cost": "$510/Ton", "material": "Coal", "type": "primary"
        },
        "e-MAT-FLA-04-PLT-003": {
            "source": "MAT-FLA-04", "target": "PLT-003", "mode": "Road", 
            "name": "Vidarbha-Hospet Blending Feed Route (NH-50)", 
            "distance": "280 km", "time": "6.0 Hours", "capacity": "4,000 Tons/day", 
            "reliability": "88.5%", "cost": "$700/Ton", "material": "Fly Ash", "type": "primary"
        }
    }

    for edge_id, r in routes_definitions.items():
        is_bypass = (r["type"] == "bypass")
        is_primary_disrupted = False
        if r["material"] == "Limestone" and "SUP-001" in matched_supplier_ids:
            is_primary_disrupted = True
        elif r["material"] == "Coal" and "SUP-003" in matched_supplier_ids:
            is_primary_disrupted = True

        cname = "edge-flow-inactive"
        animated = False
        status = "NOMINAL"
        incident_msg = ""
        mitigation_msg = ""

        if is_bypass:
            if is_primary_disrupted and alternate_suppliers:
                cname = "edge-recovered"
                animated = True
                status = "ACTIVE DETOUR / REDIRECTED"
                mitigation_msg = "AI Rerouting triggered via NH-48 Expressway bypass to cover Limestone delivery drops."
            else:
                cname = "edge-flow-inactive"
                animated = False
                status = "INACTIVE BACKUP"
        else:
            if is_primary_disrupted:
                cname = "edge-critical"
                animated = False
                status = "OBSTRUCTED / CLOSED"
                incident_msg = f"Obstructed by active event: {risk.headline}" if risk else "Obstructed"
                mitigation_msg = "Alternative rail/road routing recommended by Mitigation Planning Agent."
            else:
                animated = True
                status = "NOMINAL"
                if r["material"] == "Limestone":
                    cname = "edge-flow-limestone edge-healthy"
                elif r["material"] == "Gypsum":
                    cname = "edge-flow-gypsum edge-healthy"
                elif r["material"] == "Coal":
                    cname = "edge-flow-coal edge-healthy"
                elif r["material"] == "Fly Ash":
                    cname = "edge-flow-flyash edge-healthy"

        edges.append({
            "id": edge_id,
            "source": r["source"],
            "target": r["target"],
            "className": cname,
            "animated": animated,
            "data": {
                "name": r["name"],
                "mode": r["mode"],
                "distance": r["distance"],
                "time": r["time"],
                "capacity": r["capacity"],
                "reliability": r["reliability"],
                "cost": r["cost"],
                "status": status,
                "incident": incident_msg,
                "mitigation": mitigation_msg
            }
        })

    # C. Plant -> Distribution Center (DC Corridors)
    plant_dc_links = [
        ("PLT-001", "DBC-001", "NE-4 Delhi-Mumbai Expressway freight vector", "520 km", "9.5 Hours", "15,000 Tons/day", "98.5%", "$1,100/Ton"),
        ("PLT-002", "DBC-002", "Satna-Ahmedabad Corridor Freight line", "920 km", "17.5 Hours", "12,000 Tons/day", "94.0%", "$1,950/Ton"),
        ("PLT-003", "DBC-003", "NH-44 Peninsular Corridor vector", "290 km", "6.0 Hours", "10,000 Tons/day", "96.5%", "$720/Ton")
    ]
    for p_id, dc_id, name, dist, time_str, cap, rel, cost in plant_dc_links:
        edge_id = f"e-{p_id}-{dc_id}"
        cname = "edge-flow-cement edge-healthy"
        animated = True
        status = "NOMINAL"
        if p_id in affected_plants:
            status = "UPSTREAM PRODUCTION DROP LIMITATION"
            cname = "edge-flow-cement edge-warning-dashed"
            
        edges.append({
            "id": edge_id,
            "source": p_id,
            "target": dc_id,
            "className": cname,
            "animated": animated,
            "data": {
                "name": name,
                "mode": "Road / Bulker Fleet",
                "distance": dist,
                "time": time_str,
                "capacity": cap,
                "reliability": rel,
                "cost": cost,
                "status": status
            }
        })

    # D. DC -> Customer (Last-mile demand segments)
    dc_cust_links = [
        ("DBC-001", "CUST-NCR", "National Capital Region Bulk Supply", "45 km", "1.5 Hours", "12,000 Tons/day", "99.2%", "$150/Ton"),
        ("DBC-002", "CUST-WEST", "West-Central Industrial Supply", "120 km", "3.5 Hours", "15,000 Tons/day", "97.8%", "$350/Ton"),
        ("DBC-003", "CUST-SOUTH", "Peninsular Commercial Hub Supply", "80 km", "2.5 Hours", "10,000 Tons/day", "98.5%", "$280/Ton")
    ]
    for dc_id, c_id, name, dist, time_str, cap, rel, cost in dc_cust_links:
        edge_id = f"e-{dc_id}-{c_id}"
        edges.append({
            "id": edge_id,
            "source": dc_id,
            "target": c_id,
            "className": "edge-flow-demand edge-healthy",
            "animated": True,
            "data": {
                "name": name,
                "mode": "Local Logistics Dumper Trucks",
                "distance": dist,
                "time": time_str,
                "capacity": cap,
                "reliability": rel,
                "cost": cost,
                "status": "NOMINAL"
            }
        })

    # AI Decision Overlay values
    ai_decision_overlay = {
        "active": True if risk else False,
        "hazard_detected": risk.assessment.summary if risk else "No hazards active.",
        "silo_impact": f"Production buffer exposure identified. Inventory drawdown at {[p.plant_name for p in impact.affected_plants] if impact else 'plants'}." if (impact and impact.affected_plants) else "Silo buffer holding within standard operating ranges.",
        "mitigation_selected": mitigation.executive_recommendation if mitigation else "Continuous nominal scanning active."
    }

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

    affected_count = len(matched_supplier_ids)
    alternate_count = len(alternate_suppliers)
    recovery_est = mitigation.recovery_estimate if mitigation else "2.5 Hours"
    
    bottom_metrics = {
        "network_transfers": f"{alternate_count} Bypass Routes Engaged" if alternate_count > 0 else "0 Bypass Active (Standard)",
        "materials_in_transit": "1,450 Tons Bulk Cargo" if affected_count > 0 else "3,500 Tons Nominal Flow",
        "inventory_redistribution": "2 Rail Corridors Engaged" if alternate_count > 0 else "0 Corridor Bypass",
        "delayed_shipments": f"{affected_count} Freight Vectors Blocked" if affected_count > 0 else "0 Shipments Delayed",
        "network_recovery_time": f"{recovery_est} Calculated",
        "continuity_index": "94.8% System Load Stability" if affected_count > 0 else "100.0% Nominal Performance"
    }

    kpis = [
        {"id": 1, "title": "Node Status Ratio", "value": f"{18 - affected_count} / 18 Healthy", "trend": "Active validation", "status": "success" if affected_count == 0 else "warning", "icon": "CheckCircle2"},
        {"id": 2, "title": "Redundancy Coverage", "value": "100%" if alternate_count > 0 else "N/A", "trend": "Alternative routes mapped", "status": "success", "icon": "Layers"},
    ]

    network_health_cards = [
        {"id": 1, "label": "Material Sourcing Stability", "val": "100%" if affected_count == 0 else "80%", "pct": 100 if affected_count == 0 else 80, "status": "success" if affected_count == 0 else "warning", "desc": "Sourcing nodes continuity check."},
        {"id": 2, "label": "Transit Routing Latency", "val": "+0m" if affected_count == 0 else recovery_est, "pct": 100 if affected_count == 0 else 40, "status": "success" if affected_count == 0 else "critical", "desc": "Live fleet vector delays."}
    ]

    return {
        "success": True,
        "message": "Supply Chain Network data retrieved successfully.",
        "data": {
            "nodes": nodes,
            "edges": edges,
            "ai_action_plans": ai_action_plans,
            "bottom_metrics": bottom_metrics,
            "kpis": kpis,
            "network_health_cards": network_health_cards,
            "ai_decision_overlay": ai_decision_overlay
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

    wave_transmissions = []
    if risk:
        wave_transmissions.append({"id": "pkt-1", "label": "News Ingest Alert", "from": "NewsAgent", "to": "RiskAgent"})
    if impact:
        wave_transmissions.append({"id": "pkt-2", "label": "Impact Analysis Routing", "from": "RiskAgent", "to": "ImpactAgent"})
    if mitigation:
        wave_transmissions.append({"id": "pkt-3", "label": "Mitigation Strategy Deploy", "from": "ImpactAgent", "to": "MitigationAgent"})

    system_metrics = [
        {"label": "Active AI Threads", "value": f"{len(agents)} Mapped Agents", "type": "brand"},
        {"label": "Knowledge Resolution", "value": "Continuous Synced", "type": "success"}
    ]
    if risk:
        system_metrics.append({"label": "LLM Classification Accuracy", "value": f"{int(risk.assessment.confidence * 100)}%", "type": "success"})

    queue_items = []
    if state.get("search_results"):
        queue_items.append({"id": "Q-INGEST-01", "type": "ingest", "label": f"Ingested news feeds from search API."})
    if state.get("filtered_news"):
        queue_items.append({"id": "Q-FILTER-02", "type": "filter", "label": f"Filtered to {len(state['filtered_news'].articles)} relevant alerts."})
    if risk:
        queue_items.append({"id": "Q-CLASSIFY-03", "type": "classify", "label": f"Classified disruption category as {getattr(risk.assessment.category, 'value', 'weather').title()}."})
    if impact:
        queue_items.append({"id": "Q-IMPACT-04", "type": "impact", "label": f"Simulated plant production loss at {impact.estimated_production_loss_percent}%."})
    if mitigation:
        queue_items.append({"id": "Q-MITIGATE-05", "type": "mitigate", "label": "Bypass sourcing loops generated."})

    timeline_stages = [
        {"title": "News Extraction", "status": "Success", "time": "0.1s ago", "duration": "0.45s", "agent": "News Intelligence Agent", "confidence": "98%"},
        {"title": "Risk Grading", "status": "Success" if risk else "Pending", "time": "Just now" if risk else "--", "duration": "0.52s", "agent": "Risk Agent", "confidence": f"{int(risk.assessment.confidence * 100)}%" if risk else "N/A"},
        {"title": "Impact Mapping", "status": "Success" if impact else "Pending", "time": "Just now" if impact else "--", "duration": "0.58s", "agent": "Impact Agent", "confidence": "94%" if impact else "N/A"},
        {"title": "Mitigation Planning", "status": "Success" if mitigation else "Pending", "time": "Just now" if mitigation else "--", "duration": "0.51s", "agent": "Mitigation Agent", "confidence": "96%" if mitigation else "N/A"}
    ]

    latest_prescription = None
    if mitigation:
        latest_prescription = {
            "priority": risk.assessment.severity.value.upper() if risk else "CRITICAL",
            "impact": f"Avoid {', '.join([p.plant_name for p in impact.affected_plants]) if (impact and impact.affected_plants) else 'Plant'} shutdown",
            "delay": mitigation.recovery_estimate,
            "cost": mitigation.estimated_cost or "Low spot variance",
            "confidence": "96%",
            "action": mitigation.executive_recommendation
        }

    return {
        "success": True,
        "message": "AI Decision Center data retrieved successfully.",
        "data": {
            "kpis": [
                {"id": 1, "label": "Active AI Agents", "value": f"{len(agents)} / 3 Active", "desc": "Continuous orchestration", "icon": "Cpu", "type": "brand"},
                {"id": 2, "label": "Average Confidence", "value": "95%", "desc": "Context threshold check", "icon": "TrendingUp", "type": "success"}
            ],
            "agents": agents,
            "wave_transmissions": wave_transmissions,
            "system_metrics": system_metrics,
            "queue_items": queue_items,
            "timeline_stages": timeline_stages,
            "latest_prescription": latest_prescription
        }
    }

def transform_reports(state: dict) -> dict:
    """
    Transforms SupplyChainState into markdown Executive Reports page format.
    """
    risk_list = state.get("risk_analysis") or []
    impact_list = state.get("impact_analysis") or []
    mitigation_list = state.get("mitigation_plan") or []

    risk = risk_list[0] if risk_list else None
    impact = impact_list[0] if impact_list else None
    mitigation = mitigation_list[0] if mitigation_list else None

    if not risk:
        return {"success": False, "message": "Reports pending.", "data": {}}

    news_id_short = risk.news_id.split("/")[-1][:8] if "/" in risk.news_id else "GEN-1042"
    location = risk.assessment.location
    city = location.city if location and location.city else "Rajasthan Region"
    state_name = location.state if location and location.state else "Rajasthan"
    country = location.country if location and location.country else "India"
    
    severity_val = getattr(risk.assessment.severity, "value", "medium").capitalize()
    business_impact = getattr(risk.assessment.business_impact, "value", "minor")
    priority = "P1 - High Blockade" if business_impact == "severe" else "P2 - Moderate Alert"
    date_str = risk.published_date.strftime("%Y-%m-%d") if isinstance(risk.published_date, datetime) else "2026-07-23"
    time_str = risk.published_date.strftime("%H:%M:%S") if isinstance(risk.published_date, datetime) else "12:00:00"

    # Calculate stock days
    limestone_days = 8.8
    if impact and impact.inventory:
        lim_inv = next((i for i in impact.inventory if i.material == "Limestone"), None)
        if lim_inv:
            limestone_days = round(lim_inv.current_stock_days, 1)

    # Compile dynamic report
    report_history = [
        {
            "id": f"REP-2026-{news_id_short}",
            "title": "STRATEGIC RISK & MITIGATION REPORT",
            "date": date_str,
            "incident": risk.headline,
            "severity": severity_val,
            "status": "APPROVED",
            "author": "Strategic Operations Orchestration Agent",
            "version": "v1.2.4",
            "readingTime": "3 min read",
            "confidence": f"{int(risk.assessment.confidence * 100)}%",
            "priority": priority,
            "summary": risk.assessment.summary,
            "diagnostic": {
                "incident_id": f"INC-2026-{news_id_short}",
                "severity": f"{severity_val} / Tier 1 Risk",
                "location": f"{city}, {state_name}",
                "date": date_str,
                "phase": "Mitigation Active",
                "vector": mitigation.transportation_plan[0].mode if mitigation and mitigation.transportation_plan else "NH-48 Fleet Loop Bypass"
            },
            "business_impact": {
                "operational": f"Limestone bulk cargo haulage vector completely obstructed. Inbound pipeline latency scales by {mitigation.recovery_estimate if mitigation else '+36 hours'} until structural water recedes.",
                "financial": f"Estimated structural loss exposure capped at {mitigation.estimated_cost if mitigation else '$42,500'} without intervention.",
                "production": f"Raw mill buffer drawdown down to {limestone_days} days.",
                "continuity": "Alternate inter-modal nodes retain 94% network resilience capacity."
            },
            "affected_plants": [
                {
                    "name": p.plant_name,
                    "status": "Critical Risk Exposure" if p.production_loss_percent > 10 else "Nominal Baseline",
                    "buffer": f"Buffer: {limestone_days} Days Remaining"
                }
                for p in (impact.affected_plants if impact else [])
            ],
            "sourcing_vector": [
                {
                    "hub": risk.assessment.affected_suppliers[0].name if risk.assessment.affected_suppliers else "Marwar Mining & Minerals",
                    "material": "Limestone Bulk",
                    "impact": "Complete Sourcing Obstruction",
                    "alternate": mitigation.alternate_suppliers[0].supplier_name if (mitigation and mitigation.alternate_suppliers) else "Emergency Sourcing"
                }
            ],
            "silo_inventory": {
                "stock": f"{int(limestone_days * 8333)} T",
                "safety": "40,000 T",
                "horizon": f"{limestone_days} Days",
                "material": "Limestone"
            },
            "financial_analysis": {
                "baseline_loss": mitigation.estimated_cost or "$42,500",
                "recovery_cost": "$8,400",
                "mitigation_cost": "$4,820",
                "net_saved": "+$29,280"
            },
            "logistics_latency": {
                "latency": "+45 mins cycle",
                "recovery_window": "4.5 Hours Post-Drain",
                "deliveries": "2 Freight Vectors"
            },
            "mitigation_bullets": [
                action.description for action in (mitigation.actions if mitigation else [])
            ],
            "generatedBy": "Strategic Operations Orchestration Agent",
            "creationTime": f"{date_str} {time_str}"
        }
    ]

    report_meta = {
        "id": report_history[0]["id"],
        "generatedBy": report_history[0]["generatedBy"],
        "creationTime": report_history[0]["creationTime"],
        "version": report_history[0]["version"],
        "confidence": report_history[0]["confidence"],
        "status": report_history[0]["status"],
        "priority": report_history[0]["priority"],
        "readingTime": report_history[0]["readingTime"]
    }

    kpis = [
        {"id": 1, "title": "Total Reports Compiled", "value": "1 Compiled", "status": "success", "desc": "Automatic documentation"},
        {"id": 2, "title": "Average Confidence", "value": report_meta["confidence"], "status": "success", "desc": "Threshold validation safe"},
    ]

    quality_metrics = [
        {"label": "Diagnostic Completeness", "score": 96},
        {"label": "Policy/Budget Alignment", "score": 98},
        {"label": "Actionability Precision", "score": 95}
    ]

    timeline_activity = [
        {"id": 1, "event": "Pipeline Ingestion Complete", "time": time_str, "desc": "News intelligence data analyzed and parsed."},
        {"id": 2, "event": "Strategic Summary Compiled", "time": time_str, "desc": "Report generated by Strategic Operations Orchestration Agent."}
    ]

    return {
        "success": True,
        "message": "Executive Reports data retrieved successfully.",
        "data": {
            "report_meta": report_meta,
            "kpis": kpis,
            "quality_metrics": quality_metrics,
            "timeline_activity": timeline_activity,
            "report_history": report_history
        }
    }
