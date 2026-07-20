from fastapi import APIRouter

router = APIRouter(
    prefix="/supply-chain",
    tags=["Supply Chain Network"]
)


@router.get("")
async def get_supply_chain_network():

    return {
        "success": True,
        "message": "Supply Chain Network data retrieved successfully.",
        "data": {

            "kpis": [
                {
                    "id": 1,
                    "title": "Network Health",
                    "value": "94.8%",
                    "trend": "Optimal Range",
                    "status": "success",
                    "icon": "Activity"
                },
                {
                    "id": 2,
                    "title": "Connected Suppliers",
                    "value": "42 Nodes",
                    "trend": "+2 Activated",
                    "status": "success",
                    "icon": "Layers"
                },
                {
                    "id": 3,
                    "title": "Operational Plants",
                    "value": "6 / 7 Live",
                    "trend": "1 High Alert",
                    "status": "warning",
                    "icon": "Factory"
                },
                {
                    "id": 4,
                    "title": "Active Warehouses",
                    "value": "18 Hubs",
                    "trend": "84% Capacity",
                    "status": "success",
                    "icon": "Package"
                },
                {
                    "id": 5,
                    "title": "Critical Routes",
                    "value": "3 Blocks",
                    "trend": "Mitigation Ready",
                    "status": "critical",
                    "icon": "Route"
                },
                {
                    "id": 6,
                    "title": "Current Material Flow",
                    "value": "4,850 T/h",
                    "trend": "+12% vs Baseline",
                    "status": "success",
                    "icon": "Truck"
                }
            ],

            "network_health_cards": [
                {
                    "id": 1,
                    "label": "Supplier Status",
                    "val": "38 Online / 4 Affected",
                    "pct": 90,
                    "desc": "Valsad Quarry cluster experiencing transport restrictions.",
                    "status": "warning"
                },
                {
                    "id": 2,
                    "label": "Route Network",
                    "val": "88% Fluidity Rate",
                    "pct": 88,
                    "desc": "NH-48 closed near border post; bypass options deployed.",
                    "status": "warning"
                },
                {
                    "id": 3,
                    "label": "Warehouse Status",
                    "val": "12 Silos Stable / 1 Critical",
                    "pct": 94,
                    "desc": "Plant A limestone reserves at 36-hour safety buffer thresholds.",
                    "status": "critical"
                },
                {
                    "id": 4,
                    "label": "Overall AI Twin Score",
                    "val": "96.2 System Health",
                    "pct": 96,
                    "desc": "Autonomous anomaly tracking engines operational.",
                    "status": "success"
                }
            ],

            "nodes": [
                {
                    "id": "sup-1",
                    "type": "twinNode",
                    "position": {
                        "x": 50,
                        "y": 30
                    },
                    "data": {
                        "name": "Valsad Quarry Hub",
                        "location": "Gujarat",
                        "material": "Limestone Raw Bulk",
                        "health": "critical",
                        "status": "Logistics Obstructed",
                        "icon": "Layers"
                    }
                },
                {
                    "id": "sup-2",
                    "type": "twinNode",
                    "position": {
                        "x": 320,
                        "y": 30
                    },
                    "data": {
                        "name": "Jodhpur Actives",
                        "location": "Rajasthan",
                        "material": "Alternative Limestone",
                        "health": "success",
                        "status": "Emergency Capacity",
                        "icon": "Layers"
                    }
                },
                {
                    "id": "wh-1",
                    "type": "twinNode",
                    "position": {
                        "x": 185,
                        "y": 160
                    },
                    "data": {
                        "name": "Central Silo Matrix A",
                        "location": "Plant A Proximity",
                        "material": "Aggregate Storage",
                        "health": "warning",
                        "status": "Low Buffer Stock",
                        "icon": "Package"
                    }
                },
                {
                    "id": "pl-1",
                    "type": "twinNode",
                    "position": {
                        "x": 185,
                        "y": 290
                    },
                    "data": {
                        "name": "Plant A Grinding Mill",
                        "location": "Gujarat East",
                        "material": "Clinker Processing",
                        "health": "warning",
                        "status": "Rerouting Inbound",
                        "icon": "Factory"
                    }
                },
                {
                    "id": "dc-1",
                    "type": "twinNode",
                    "position": {
                        "x": 50,
                        "y": 420
                    },
                    "data": {
                        "name": "Mumbai Logistics Base",
                        "location": "Maharashtra",
                        "material": "Finished Product Cement",
                        "health": "success",
                        "status": "Optimal Output",
                        "icon": "Truck"
                    }
                },
                {
                    "id": "dc-2",
                    "type": "twinNode",
                    "position": {
                        "x": 320,
                        "y": 420
                    },
                    "data": {
                        "name": "Surat Terminal Node",
                        "location": "Gujarat South",
                        "material": "Bulk Matrix Packets",
                        "health": "success",
                        "status": "Optimal Output",
                        "icon": "Truck"
                    }
                }
            ],

            "edges": [
                {
                    "id": "e1",
                    "source": "sup-1",
                    "target": "wh-1",
                    "className": "edge-flow-limestone edge-critical"
                },
                {
                    "id": "e2",
                    "source": "sup-2",
                    "target": "wh-1",
                    "className": "edge-flow-alternative edge-alternative-dashed"
                },
                {
                    "id": "e3",
                    "source": "wh-1",
                    "target": "pl-1",
                    "className": "edge-flow-mix edge-transfer-blue"
                },
                {
                    "id": "e4",
                    "source": "pl-1",
                    "target": "dc-1",
                    "className": "edge-flow-finished edge-healthy"
                },
                {
                    "id": "e5",
                    "source": "pl-1",
                    "target": "dc-2",
                    "className": "edge-flow-finished edge-healthy"
                }
            ],

            "ai_action_plans": [
                {
                    "id": 1,
                    "priority": "Critical",
                    "action": "Transfer Inventory from Plant C",
                    "delay": "None",
                    "cost": "$4,200",
                    "impact": "Secures next 24 hours blending operations",
                    "conf": "98%",
                    "agent": "Inventory Balancer",
                    "time": "14:30"
                },
                {
                    "id": 2,
                    "priority": "High",
                    "action": "Activate Backup Supplier Hub 7",
                    "delay": "+2.5 Hours",
                    "cost": "$14,200",
                    "impact": "Bypasses broken logistics lines on NH-48",
                    "conf": "97%",
                    "agent": "Sourcing Engine",
                    "time": "14:45"
                },
                {
                    "id": 3,
                    "priority": "Medium",
                    "action": "Switch Transport Vector to Rail",
                    "delay": "+4.0 Hours",
                    "cost": "-$2,100",
                    "impact": "Mitigates prolonged highway congestion risk",
                    "conf": "92%",
                    "agent": "Logistics Route Agent",
                    "time": "16:00"
                }
            ]
        }
    }