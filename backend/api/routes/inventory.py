from fastapi import APIRouter

router = APIRouter(
    prefix="/inventory",
    tags=["Plants & Inventory"],
)


@router.get("")
async def get_plants_inventory():

    return {
        "success": True,
        "message": "Plants & Inventory data retrieved successfully.",
        "data": {

            "kpis": [
                {
                    "id": 1,
                    "title": "Total Production Today",
                    "value": "14,850 T",
                    "trend": "+4.2% vs baseline",
                    "status": "success",
                    "icon": "Factory"
                },
                {
                    "id": 2,
                    "title": "Inventory Health",
                    "value": "84%",
                    "trend": "-1.5% weekly slip",
                    "status": "warning",
                    "icon": "Package"
                },
                {
                    "id": 3,
                    "title": "Plants Online",
                    "value": "6 / 7",
                    "trend": "1 High Risk Obstructed",
                    "status": "success",
                    "icon": "CheckCircle2"
                },
                {
                    "id": 4,
                    "title": "Materials at Risk",
                    "value": "2 Items",
                    "trend": "Safety stock violated",
                    "status": "critical",
                    "icon": "AlertTriangle"
                }
            ],

            "plants": [
                {
                    "id": "PLT-A",
                    "name": "Plant A - Western Grinding Complex",
                    "location": "Gujarat East",
                    "status": "At Risk",
                    "healthScore": 68,
                    "production": "4,200 T/d",
                    "capacity": "5,000 T/d",
                    "utilization": 84,
                    "risk": "Limestone supply vector obstruction via NH-48 flooding.",
                    "suppliers": 4,
                    "inventoryHealth": "Critical",
                    "remainingDays": 1.5
                },
                {
                    "id": "PLT-B",
                    "name": "Plant B - Central Kiln Facility",
                    "location": "Madhya Pradesh",
                    "status": "Healthy",
                    "healthScore": 94,
                    "production": "6,100 T/d",
                    "capacity": "6,500 T/d",
                    "utilization": 93,
                    "risk": "None. Off-peak power grid schedules nominal.",
                    "suppliers": 6,
                    "inventoryHealth": "Optimal",
                    "remainingDays": 14
                },
                {
                    "id": "PLT-C",
                    "name": "Plant C - Southern Port Terminal",
                    "location": "Tamil Nadu",
                    "status": "Healthy",
                    "healthScore": 91,
                    "production": "4,550 T/d",
                    "capacity": "5,000 T/d",
                    "utilization": 91,
                    "risk": "Minor diesel overhead variance via terminal port wait lanes.",
                    "suppliers": 5,
                    "inventoryHealth": "Stable",
                    "remainingDays": 10
                }
            ],

            "inventory": [
                {
                    "material": "Limestone",
                    "stock": "6,200 T",
                    "safety": "15,000 T",
                    "consumption": "4,000 T/d",
                    "days": 1.5,
                    "incoming": "8,500 T",
                    "status": "critical",
                    "supplier": "Valsad Quarry Hub",
                    "risk": "Critical",
                    "pct": 41
                },
                {
                    "material": "Coal",
                    "stock": "14,500 T",
                    "safety": "12,000 T",
                    "consumption": "1,200 T/d",
                    "days": 12,
                    "incoming": "5,000 T",
                    "status": "warning",
                    "supplier": "International Trade",
                    "risk": "Medium",
                    "pct": 120
                },
                {
                    "material": "Fly Ash",
                    "stock": "9,800 T",
                    "safety": "8,000 T",
                    "consumption": "1,500 T/d",
                    "days": 6.5,
                    "incoming": "3,000 T",
                    "status": "success",
                    "supplier": "NTPC Cluster Node",
                    "risk": "Low",
                    "pct": 122
                },
                {
                    "material": "Gypsum",
                    "stock": "4,100 T",
                    "safety": "3,500 T",
                    "consumption": "450 T/d",
                    "days": 9.1,
                    "incoming": "1,200 T",
                    "status": "success",
                    "supplier": "Border Transit Check",
                    "risk": "Low",
                    "pct": 117
                },
                {
                    "material": "Diesel",
                    "stock": "85,000 L",
                    "safety": "90,000 L",
                    "consumption": "10,000 L/d",
                    "days": 8.5,
                    "incoming": "45,000 L",
                    "status": "warning",
                    "supplier": "Ministry Petroleum Link",
                    "risk": "Medium",
                    "pct": 94
                },
                {
                    "material": "Packaging Material",
                    "stock": "240k Units",
                    "safety": "200k Units",
                    "consumption": "35k/d",
                    "days": 6.8,
                    "incoming": "150k Units",
                    "status": "success",
                    "supplier": "Zone East Pack Co",
                    "risk": "Low",
                    "pct": 120
                }
            ],

            "ai_insights": [
                {
                    "priority": "Critical",
                    "impact": "Avoid Plant A shutdown completely",
                    "confidence": "97%",
                    "delay": "2 hours net",
                    "agent": "Mitigation Planning Agent",
                    "action": "Transfer 1,200 T Limestone from Plant C reserves via rail segment bypass loops.",
                    "title": "Transfer Limestone from Plant C"
                },
                {
                    "priority": "High",
                    "impact": "Bypass broken logistics corridors on NH-48",
                    "confidence": "94%",
                    "delay": "+45 mins cycle",
                    "agent": "Sourcing Optimization Engine",
                    "action": "Activate alternative solid fuel contract terms with emergency Rajasthan Quarry suppliers.",
                    "title": "Activate Emergency Backup Supplier"
                },
                {
                    "priority": "Medium",
                    "impact": "Hedging spot energy margin variance scales",
                    "confidence": "91%",
                    "delay": "None",
                    "agent": "Procurement Balance Module",
                    "action": "Increase Coal procurement schedules across secondary rail loops to balance clinker burn runs.",
                    "title": "Increase Coal Procurement"
                }
            ],

            "production_trend": [
                {"name":"08:00","PlantA":380,"PlantB":590,"PlantC":420},
                {"name":"10:00","PlantA":400,"PlantB":600,"PlantC":450},
                {"name":"12:00","PlantA":420,"PlantB":610,"PlantC":455},
                {"name":"14:00","PlantA":350,"PlantB":610,"PlantC":450}
            ],

            "inventory_consumption": [
                {"name":"Limestone","Current":6200,"Safety":15000},
                {"name":"Coal","Current":14500,"Safety":12000},
                {"name":"Fly Ash","Current":9800,"Safety":8000},
                {"name":"Gypsum","Current":4100,"Safety":3500}
            ],

            "capacity_utilization": [
                {"name":"Plant A","value":84,"fill":"#B15A52"},
                {"name":"Plant B","value":93,"fill":"#708C72"},
                {"name":"Plant C","value":91,"fill":"#3E556B"}
            ],

            "material_availability": [
                {"name":"Healthy Nodes","value":4},
                {"name":"Warning Nodes","value":1},
                {"name":"Critical Risks","value":1}
            ]
        }
    }