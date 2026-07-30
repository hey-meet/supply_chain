# backend/api/routes/decision_center.py

import time
import logging
import json
import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from backend.services.graph_service import graph_service
from backend.services.response_transformer import transform_decision_center, transform_assistant_response
from backend.services.llm_client import LLMClient
from backend.prompts.prompt_manager import prompt_manager

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/decision-center",
    tags=["AI Decision Center"]
)


class AssistantActionRequest(BaseModel):
    action: str = Field(..., description="Action ID key (e.g. explain_critical_disruptions)")
    page_context: str = Field(default="incident_center", description="Active page context code (e.g. plants_inventory)")
    entity_id: str | None = Field(default=None, description="Optional ID of active or selected entity being viewed")


ACTION_MAPPING = {
    "explain_critical_disruptions": "Explain Today's Critical Disruptions",
    "explain_ai_decision": "Explain AI Decision",
    "explain_executive_report": "Explain Executive Report",
    "analyze_plant_risks": "Analyze Plant Risks",
    "analyze_inventory_risks": "Analyze Inventory Risks",
    "explain_route_disruption": "Explain Route Disruption",
    "explain_supplier_impact": "Explain Supplier Impact",
    "explain_knowledge_graph_dependencies": "Explain Knowledge Graph Dependencies",
    "explain_mitigation_strategy": "Explain Mitigation Strategy",
    "executive_summary": "Executive Summary",
    "root_cause_analysis": "Root Cause Analysis",
    "why_critical": "Why was this incident classified as Critical?",
    "affected_plants": "Which plants are affected?",
    "affected_suppliers": "Which suppliers are impacted?",
    "digital_twin_analysis": "Digital Twin Impact Analysis",
}


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        import enum
        if isinstance(obj, enum.Enum):
            return obj.value
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        if hasattr(obj, "dict"):
            try:
                return obj.dict()
            except Exception:
                pass
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)


@router.get("")
async def get_ai_decision_center():
    start_time = time.perf_counter()
    cache = graph_service.get_cache()
    
    if not cache.is_initialized:
        api_time = time.perf_counter() - start_time
        return {
            "success": False,
            "message": "Analysis pending. Please execute a query first.",
            "data": {},
            "metrics": {
                "api_response_time_seconds": round(api_time, 4)
            }
        }
        
    transform_start = time.perf_counter()
    response = transform_decision_center(cache.workflow_state)
    transform_time = time.perf_counter() - transform_start
    
    api_time = time.perf_counter() - start_time
    logger.info(
        "Decision Center Endpoint Performance: Transform: %.4fs, API: %.4fs",
        transform_time,
        api_time
    )
    
    if response.get("success") and "data" in response:
        response["data"]["metrics"] = {
            "transform_time_seconds": round(transform_time, 4),
            "api_response_time_seconds": round(api_time, 4)
        }
        
    return response


@router.post("/action")
async def execute_assistant_action(payload: AssistantActionRequest):
    start_time = time.perf_counter()
    action_key = payload.action
    
    if action_key not in ACTION_MAPPING:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": f"Unsupported action key: {action_key}",
                "cache_status": "uninitialized"
            }
        )
        
    cache = graph_service.get_cache()
    if not cache.is_initialized:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "No active analysis found. Please run a supply chain disruption query or scan first to initialize the executive context.",
                "cache_status": "uninitialized"
            }
        )
        
    # Serialize the cached workflow state
    state = cache.workflow_state
    workflow_state_json = json.dumps(state, cls=CustomEncoder, indent=2)
    
    # Render prompt using PromptManager
    prompt = prompt_manager.render(
        template_name="assistant_action.txt",
        variables={
            "workflow_state_json": workflow_state_json,
            "action_id": action_key,
            "action_name": ACTION_MAPPING[action_key],
            "page_context": payload.page_context
        }
    )
    
    # Invoke LLM Client
    try:
        llm = LLMClient()
        raw_response = llm.generate(prompt)
    except Exception as exc:
        logger.exception("AI Assistant action execution failed during LLM call: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"AI reasoning service failed: {exc}"
            }
        )
        
    # Transform response
    response = transform_assistant_response(raw_response, state)
    
    api_time = time.perf_counter() - start_time
    if response.get("success") and "data" in response:
        response["data"]["metrics"] = {
            "api_response_time_seconds": round(api_time, 4)
        }
        
    return response