from fastapi import APIRouter

router = APIRouter(
    prefix="/incident",
    tags=["Incident Center"]
)


@router.get("")
async def get_incident_center():

    return {
        "success": True,
        "message": "Incident Center data retrieved successfully.",
        "data": {

            "incident_meta": {
                "id": "INC-2026-8941",
                "severity": "Critical",
                "status": "Active Investigation",
                "location": "Valsad Corridor",
                "country": "India",
                "state": "Gujarat",
                "detectedTime": "13:50:42",
                "lastUpdated": "14:02:11",
                "riskCategory": "Logistics Interruption",
                "confidence": "99%",
                "businessPriority": "P1 - High Blockade",
                "description": "Heavy rainfall has triggered sudden structural flash flooding and land displacement, causing a major highway closure on National Highway 48 and completely stopping limestone aggregate transportation vectors to Plant A."
            },

            "extracted_entities": [
                "Limestone Aggregate",
                "Plant A Grinding Kiln",
                "National Highway 48",
                "Heavy Rainfall Corridor",
                "Gujarat Logistics Fleet",
                "Valsad Quarry Hub"
            ],

            "supporting_sources": [
                {
                    "id": 1,
                    "publisher": "Reuters Logistics",
                    "reliability": "98%",
                    "time": "3 mins ago",
                    "status": "Verified"
                },
                {
                    "id": 2,
                    "publisher": "NOAA Flash Advisory",
                    "reliability": "99%",
                    "time": "8 mins ago",
                    "status": "Verified"
                },
                {
                    "id": 3,
                    "publisher": "NHAI Highway Patrol",
                    "reliability": "97%",
                    "time": "11 mins ago",
                    "status": "Verified"
                },
                {
                    "id": 4,
                    "publisher": "Gujarat State Telemetry",
                    "reliability": "94%",
                    "time": "14 mins ago",
                    "status": "Cross-Referenced"
                },
                {
                    "id": 5,
                    "publisher": "Siam Fleet Dispatch",
                    "reliability": "91%",
                    "time": "18 mins ago",
                    "status": "Cross-Referenced"
                }
            ],

            "timeline_steps": [
                {
                    "id": 1,
                    "title": "Step 1: News Intelligence Output",
                    "agent": "News Intelligence Agent",
                    "metrics": {
                        "risk": "Logistics Failure",
                        "severity": "Critical",
                        "confidence": "99%",
                        "latency": "0.4s"
                    },
                    "reasoning": "Natural language models cross-referenced standard wire logs against industrial telemetry arrays, establishing automated confirmation of complete route blockade at the specified transit coordinates.",
                    "active": False
                },
                {
                    "id": 2,
                    "title": "Step 2: Supply Chain Impact Output",
                    "agent": "Supply Chain Impact Agent",
                    "metrics": {
                        "assets": "Plant A Kiln, Quarry Hub 4",
                        "stocks": "Silo buffer at 36 hrs",
                        "blastRadius": "Tier 1 Sourcing Network",
                        "latency": "0.9s"
                    },
                    "reasoning": "Mathematical linear models simulate kiln feed degradation. Outbound clinker production runs into immediate inventory deficit within 36 hours if raw limestone distribution remains fully obstructed.",
                    "active": False
                },
                {
                    "id": 3,
                    "title": "Step 3: Mitigation Planning Output",
                    "agent": "Mitigation Planning Agent",
                    "metrics": {
                        "alternate": "Quarry Hub 7 (Rajasthan)",
                        "route": "Bypass State Line 14",
                        "estDelay": "+2.5 Hours",
                        "estCost": "+$14,200",
                        "confidence": "97%",
                        "latency": "0.7s"
                    },
                    "reasoning": "AI multi-variable engines generated prescriptive operational alternatives. Rerouting class-8 fleets to alternative corridors maintains raw inputs, safely avoiding a costly, unscheduled manufacturing halt.",
                    "active": True
                }
            ],

            "impact_cards": [
                {
                    "id": 1,
                    "icon": "Factory",
                    "title": "Affected Plants",
                    "count": "1 Plant Active",
                    "desc": "Plant A grinding production line facing immediate input loss.",
                    "status": "critical"
                },
                {
                    "id": 2,
                    "icon": "Users",
                    "title": "Affected Suppliers",
                    "count": "1 Primary Hub",
                    "desc": "Valsad core aggregate operations isolated from transport loop.",
                    "status": "critical"
                },
                {
                    "id": 3,
                    "icon": "Package",
                    "title": "Affected Warehouses",
                    "count": "2 Storage Silos",
                    "desc": "Buffer stockpiles decreasing significantly below standard safe baselines.",
                    "status": "warning"
                },
                {
                    "id": 4,
                    "icon": "Route",
                    "title": "Affected Routes",
                    "count": "1 Primary Vector",
                    "desc": "National Highway 48 fully obstructed across multi-mile sector.",
                    "status": "critical"
                },
                {
                    "id": 5,
                    "icon": "ShieldAlert",
                    "title": "Inventory Risk",
                    "count": "36 Hour Window",
                    "desc": "Critical depletion threshold tracked on secondary blending units.",
                    "status": "critical"
                },
                {
                    "id": 6,
                    "icon": "Layers",
                    "title": "Production Risk",
                    "count": "High Exposure",
                    "desc": "Failure to mitigate threatens downstream clinker deliveries.",
                    "status": "critical"
                },
                {
                    "id": 7,
                    "icon": "Activity",
                    "title": "Business Continuity",
                    "count": "82% Stability",
                    "desc": "Platform response active. Safeguards executing correctly.",
                    "status": "warning"
                },
                {
                    "id": 8,
                    "icon": "DollarSign",
                    "title": "Financial Impact",
                    "count": "$48,500 Est.",
                    "desc": "Calculated overhead variance across operational rerouting phases.",
                    "status": "warning"
                },
                {
                    "id": 9,
                    "icon": "Clock",
                    "title": "Expected Delay",
                    "count": "2.5 Hours Net",
                    "desc": "Incremental cycle time added via alternative transit loops.",
                    "status": "warning"
                }
            ],

            "progress_stages": [
                {
                    "id": 1,
                    "name": "Detected",
                    "status": "Complete",
                    "time": "13:50:42",
                    "agent": "News Intelligence Agent",
                    "active": False
                },
                {
                    "id": 2,
                    "name": "Investigating",
                    "status": "Complete",
                    "time": "13:52:19",
                    "agent": "Operational Context Agent",
                    "active": False
                },
                {
                    "id": 3,
                    "name": "Impact Calculated",
                    "status": "Complete",
                    "time": "13:55:00",
                    "agent": "Supply Chain Impact Agent",
                    "active": False
                },
                {
                    "id": 4,
                    "name": "Mitigation Ready",
                    "status": "In Progress",
                    "time": "14:01:45",
                    "agent": "Mitigation Planning Agent",
                    "active": True
                },
                {
                    "id": 5,
                    "name": "Closed",
                    "status": "Pending",
                    "time": "--:--:--",
                    "agent": "System Core Orchestrator",
                    "active": False
                }
            ]
        }
    }