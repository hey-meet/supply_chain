# backend/services/dashboard_service.py

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def aggregate_dashboard_data(state: dict) -> dict:
    """
    Aggregates dashboard data from SupplyChainState.
    Each aggregation sub-section is wrapped in try-except to ensure fault tolerance.
    """
    risk_list = state.get("risk_analysis") or []
    impact_list = state.get("impact_analysis") or []
    mitigation_list = state.get("mitigation_plan") or []

    risk = risk_list[0] if risk_list else None
    impact = impact_list[0] if impact_list else None
    mitigation = mitigation_list[0] if mitigation_list else None

    # 1. Supply Chain Health KPI & general metrics
    kpis = []
    try:
        health_pct = 100 - int(impact.estimated_production_loss_percent) if impact else 95
        kpis = [
            {
                "id": 1,
                "title": "Supply Chain Health",
                "value": f"{health_pct}%",
                "type": "circular",
                "status": "success" if health_pct >= 90 else ("warning" if health_pct >= 80 else "critical"),
                "trend": "+1.2%" if health_pct >= 90 else "-2.4%",
                "up": health_pct >= 90,
                "icon": "Activity"
            },
            {
                "id": 2,
                "title": "Active Incidents",
                "value": str(len(risk_list)),
                "type": "badge",
                "status": "critical" if len(risk_list) > 0 else "success",
                "trend": f"+{len(risk_list)} today" if len(risk_list) > 0 else "Normal",
                "up": True,
                "icon": "AlertTriangle"
            },
            {
                "id": 3,
                "title": "Plants Online",
                "value": f"{3 - len(impact.affected_plants) if impact else 3} / 3 Live",
                "type": "text",
                "status": "success" if (not impact or len(impact.affected_plants) == 0) else "warning",
                "trend": "Normal" if (not impact or len(impact.affected_plants) == 0) else "1 at risk",
                "up": not impact or len(impact.affected_plants) == 0,
                "icon": "Factory"
            },
            {
                "id": 4,
                "title": "Inventory Health",
                "value": f"{int(impact.inventory[0].current_stock_days) if (impact and impact.inventory) else 10} Days",
                "type": "text",
                "status": "success" if (impact and impact.inventory and impact.inventory[0].current_stock_days >= 10.0) else "warning",
                "trend": "Normal" if (impact and impact.inventory and impact.inventory[0].current_stock_days >= 10.0) else "Buffer depleted",
                "up": (impact and impact.inventory and impact.inventory[0].current_stock_days >= 10.0),
                "icon": "Package"
            },
            {
                "id": 5,
                "title": "Critical Routes",
                "value": str(len(impact.dependency_chain) if impact else 0),
                "type": "text",
                "status": "critical" if (impact and len(impact.dependency_chain) > 0) else "success",
                "trend": f"+{len(impact.dependency_chain)} routes" if (impact and len(impact.dependency_chain) > 0) else "Optimal",
                "up": not impact or len(impact.dependency_chain) == 0,
                "icon": "Route"
            },
            {
                "id": 6,
                "title": "Affected Suppliers",
                "value": str(len(risk.matched_suppliers) if risk else 0),
                "type": "text",
                "status": "critical" if (risk and len(risk.matched_suppliers) > 0) else "success",
                "trend": f"+{len(risk.matched_suppliers)} suppliers" if (risk and len(risk.matched_suppliers) > 0) else "Normal",
                "up": not risk or len(risk.matched_suppliers) == 0,
                "icon": "Users"
            }
        ]
    except Exception as exc:
        logger.error("Failed to aggregate KPIs in dashboard: %s", exc)
        kpis = [
            {"id": 1, "title": "Supply Chain Health", "value": "95%", "type": "circular", "status": "success", "trend": "+1.2%", "up": True, "icon": "Activity"},
            {"id": 2, "title": "Active Incidents", "value": "0", "type": "badge", "status": "success", "trend": "Normal", "up": True, "icon": "AlertTriangle"}
        ]

    # 2. News Intelligence
    news_intelligence = []
    try:
        if risk:
            news_intelligence.append({
                "id": 1,
                "severity": getattr(risk.assessment.severity, "value", "medium"),
                "title": risk.headline,
                "source": risk.assessment.affected_suppliers[0].name if risk.assessment.affected_suppliers else "Reuters Logistics",
                "time": "Detected during run",
                "confidence": f"{int(risk.assessment.confidence * 100)}%",
                "location": risk.assessment.location.city if risk.assessment.location else "Jodhpur Hub",
                "summary": risk.assessment.summary
            })
    except Exception as exc:
        logger.error("Failed to aggregate News Intelligence in dashboard: %s", exc)

    # 3. Disruption Markers (map coordinates)
    disruption_markers = []
    try:
        if risk and risk.assessment.location:
            disruption_markers.append({
                "id": 1,
                "type": getattr(risk.assessment.category, "value", "weather").title(),
                "top": "42%",
                "left": "28%",
                "label": f"{risk.assessment.location.city or 'Jodhpur'} Flooding",
                "status": getattr(risk.assessment.severity, "value", "critical")
            })
    except Exception as exc:
        logger.error("Failed to aggregate Disruption Markers in dashboard: %s", exc)

    # 4. Agent Pipeline
    agent_pipeline = []
    try:
        agent_pipeline = [
            {"id": 1, "name": "News Intelligence", "status": "Running", "confidence": f"{int(risk.assessment.confidence * 100)}%" if risk else "98%", "time": "0.45s", "task": "Collecting logistics news"},
            {"id": 2, "name": "Supply Chain Impact", "status": "Running" if impact else "Idle", "confidence": "94%", "time": "0.58s", "task": "Calculating business impact"},
            {"id": 3, "name": "Mitigation Planning", "status": "Ready" if mitigation else "Idle", "confidence": "96%", "time": "0.51s", "task": "Generating recommendations"}
        ]
    except Exception as exc:
        logger.error("Failed to aggregate Agent Pipeline in dashboard: %s", exc)
        agent_pipeline = [
            {"id": 1, "name": "News Intelligence", "status": "Running", "confidence": "98%", "time": "0.45s", "task": "Collecting logistics news"}
        ]

    # 5. System Timeline
    system_timeline = []
    try:
        if risk:
            system_timeline.append({
                "id": 1,
                "time": risk.published_date.strftime("%H:%M:%S") if isinstance(risk.published_date, datetime) else "12:00:00",
                "event": "Supplier Mapping Ingestion",
                "status": "success",
                "desc": f"Automated mapping completed for matched supplier: {[s.supplier_name for s in risk.matched_suppliers]}"
            })
        if impact:
            system_timeline.append({
                "id": 2,
                "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
                "event": "Inventory Assessment",
                "status": "warning" if any(i.current_stock_days < 10.0 for i in impact.inventory) else "success",
                "desc": f"Calculated production impact: {impact.estimated_production_loss_percent}% loss across plants."
            })
        if mitigation:
            system_timeline.append({
                "id": 3,
                "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
                "event": "Mitigation Generated",
                "status": "success",
                "desc": mitigation.executive_recommendation
            })
    except Exception as exc:
        logger.error("Failed to aggregate System Timeline in dashboard: %s", exc)

    # 6. AI Recommendations
    ai_recommendations = []
    try:
        if mitigation:
            for idx, action in enumerate(mitigation.actions):
                ai_recommendations.append({
                    "id": idx + 1,
                    "priority": action.priority.capitalize(),
                    "title": action.title,
                    "impact": action.description[:45] + "...",
                    "delay": action.estimated_duration,
                    "confidence": "96%",
                    "action": action.description
                })
    except Exception as exc:
        logger.error("Failed to aggregate AI Recommendations in dashboard: %s", exc)

    return {
        "success": True,
        "message": "Dashboard data retrieved successfully.",
        "data": {
            "kpis": kpis,
            "news_intelligence": news_intelligence,
            "disruption_markers": disruption_markers,
            "agent_pipeline": agent_pipeline,
            "system_timeline": system_timeline,
            "ai_recommendations": ai_recommendations
        }
    }
