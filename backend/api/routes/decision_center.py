from fastapi import APIRouter

router = APIRouter(
    prefix="/decision-center",
    tags=["AI Decision Center"]
)


@router.get("")
async def get_ai_decision_center():

    return {
        "success": True,
        "message": "AI Decision Center data retrieved successfully.",
        "data": {

            "kpis": [
                {
                    "id": 1,
                    "label": "Active AI Agents",
                    "value": "3 / 3 Nominal",
                    "desc": "Continuous orchestration",
                    "icon": "Cpu",
                    "type": "brand"
                },
                {
                    "id": 2,
                    "label": "Current Decisions",
                    "value": "1 Active Run",
                    "desc": "Evaluating NH-48 anomaly",
                    "icon": "ShieldAlert",
                    "type": "warning"
                },
                {
                    "id": 3,
                    "label": "Average Confidence",
                    "value": "94.2%",
                    "desc": "Safe margin threshold",
                    "icon": "TrendingUp",
                    "type": "success"
                },
                {
                    "id": 4,
                    "label": "Average Execution Time",
                    "value": "1.84s",
                    "desc": "Sub-second internal loops",
                    "icon": "Clock",
                    "type": "brand"
                },
                {
                    "id": 5,
                    "label": "Total Tokens Processed",
                    "value": "2.4M",
                    "desc": "Context efficient RAG windows",
                    "icon": "Database",
                    "type": "secondary"
                },
                {
                    "id": 6,
                    "label": "Successful Decisions",
                    "value": "142 Today",
                    "desc": "0% override fallback rate",
                    "icon": "CheckCircle2",
                    "type": "success"
                }
            ],

            "agents": [
                {
                    "id": "agent-1",
                    "name": "News Intelligence Agent",
                    "avatarColor": "blue",
                    "attention": "Reasoning",
                    "emotion": "Focused",
                    "confidence": "98%",
                    "execTime": "0.45s",
                    "tokens": "142k",
                    "latestDecision": "Ingestion of validated supply chain disruption report.",
                    "metrics": [
                        {
                            "label": "Current Task",
                            "value": "Parsing logistics article pipeline..."
                        },
                        {
                            "label": "Current Thought",
                            "value": "Cross-referencing NH-48 flooding alerts with structural routes."
                        },
                        {
                            "label": "Processing Queue",
                            "value": "2 incoming events pending"
                        },
                        {
                            "label": "Collected Sources",
                            "value": "Ministry Transport Link, Regional RSS Feed"
                        }
                    ]
                },
                {
                    "id": "agent-2",
                    "name": "Supply Chain Impact Agent",
                    "avatarColor": "amber",
                    "attention": "Thinking",
                    "emotion": "Analyzing",
                    "confidence": "93%",
                    "execTime": "0.62s",
                    "tokens": "280k",
                    "latestDecision": "Identified Limestone cargo payload variance exposure.",
                    "metrics": [
                        {
                            "label": "Current Task",
                            "value": "Calculating enterprise blast radius..."
                        },
                        {
                            "label": "Current Thought",
                            "value": "Mapping delay curves onto Western Grinding Complex buffer."
                        },
                        {
                            "label": "Affected Infrastructure",
                            "value": "Plant A (Critical), Supplier Node 4"
                        },
                        {
                            "label": "Knowledge Graph Match",
                            "value": "14 entity nodes connected"
                        }
                    ]
                },
                {
                    "id": "agent-3",
                    "name": "Mitigation Planning Agent",
                    "avatarColor": "green",
                    "attention": "Decision Ready",
                    "emotion": "Confident",
                    "confidence": "96%",
                    "execTime": "0.77s",
                    "tokens": "410k",
                    "latestDecision": "Formulated primary rail bypass loop protocol.",
                    "metrics": [
                        {
                            "label": "Current Task",
                            "value": "Evaluating cost-benefit distribution matrix..."
                        },
                        {
                            "label": "Current Thought",
                            "value": "Synthesizing inventory buffer from Southern Terminal terminals."
                        },
                        {
                            "label": "Alternative Logistics",
                            "value": "Emergency Rajasthan Quarry Core"
                        },
                        {
                            "label": "Inventory Transfer Plan",
                            "value": "1,200 T Limestone allocation shift"
                        }
                    ]
                }
            ],

            "wave_transmissions": [
                {
                    "id": 1,
                    "label": "Data Packet",
                    "from": "News Intel",
                    "to": "Impact Engine"
                },
                {
                    "id": 2,
                    "label": "Knowledge Update",
                    "from": "Impact Engine",
                    "to": "Mitigation Plan"
                },
                {
                    "id": 3,
                    "label": "Decision Sent",
                    "from": "Mitigation Plan",
                    "to": "System Pipeline"
                }
            ],

            "system_metrics": [
                {
                    "label": "Overall Agent Health",
                    "value": "100% Operational",
                    "type": "success"
                },
                {
                    "label": "Agent Synchronization",
                    "value": "12ms delta delay",
                    "type": "brand"
                },
                {
                    "label": "Memory Allocation Pool",
                    "value": "14.2 GB / 32 GB",
                    "type": "secondary"
                },
                {
                    "label": "Average System Latency",
                    "value": "45ms structural",
                    "type": "brand"
                },
                {
                    "label": "Knowledge Graph Nodes",
                    "value": "42,850 active connections",
                    "type": "brand"
                },
                {
                    "label": "LLM Multi-Cluster Status",
                    "value": "Nominal baseline deployment",
                    "type": "success"
                }
            ],

            "queue_items": [
                {
                    "id": "Q-1",
                    "label": "NH-48 structural detour validation pipeline",
                    "type": "reasoning"
                },
                {
                    "id": "Q-2",
                    "label": "Clinker inventory drawdown correlation analysis",
                    "type": "reasoning"
                },
                {
                    "id": "D-1",
                    "label": "Authorize route allocation variant shift 4B",
                    "type": "decision"
                },
                {
                    "id": "D-2",
                    "label": "Trigger alternative sourcing parameters contract terms",
                    "type": "decision"
                }
            ],

            "timeline_stages": [
                {
                    "title": "Input News",
                    "time": "14:32:10",
                    "agent": "News Intel Agent",
                    "duration": "120ms",
                    "status": "Completed",
                    "confidence": "99%"
                },
                {
                    "title": "Classification",
                    "time": "14:32:11",
                    "agent": "News Intel Agent",
                    "duration": "85ms",
                    "status": "Completed",
                    "confidence": "98%"
                },
                {
                    "title": "Knowledge Graph",
                    "time": "14:32:12",
                    "agent": "Impact Agent",
                    "duration": "240ms",
                    "status": "Completed",
                    "confidence": "95%"
                },
                {
                    "title": "Risk Analysis",
                    "time": "14:32:13",
                    "agent": "Impact Agent",
                    "duration": "190ms",
                    "status": "Completed",
                    "confidence": "94%"
                },
                {
                    "title": "Impact Analysis",
                    "time": "14:32:14",
                    "agent": "Impact Agent",
                    "duration": "310ms",
                    "status": "Completed",
                    "confidence": "93%"
                },
                {
                    "title": "Mitigation",
                    "time": "14:32:15",
                    "agent": "Mitigation Agent",
                    "duration": "420ms",
                    "status": "Active",
                    "confidence": "96%"
                },
                {
                    "title": "Executive Decision",
                    "time": "Pending",
                    "agent": "System Core Orchestration",
                    "duration": "---",
                    "status": "Queued",
                    "confidence": "---"
                }
            ]

        }
    }