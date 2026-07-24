# backend/services/graph_service.py

import time
import logging
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from backend.graphs.supply_chain_graph import supply_chain_graph

logger = logging.getLogger(__name__)

class PipelineCache(BaseModel):
    workflow_state: dict = Field(default_factory=dict)
    last_query: str | None = None
    last_updated: str | None = None
    is_initialized: bool = False
    graph_execution_time_seconds: float = 0.0

class GraphService:
    def __init__(self):
        self._cache = PipelineCache()

    def get_cache(self) -> PipelineCache:
        return self._cache

    def execute_pipeline(self, query: str) -> PipelineCache:
        logger.info("Executing LangGraph pipeline for query: %r", query)
        start_time = time.perf_counter()
        
        try:
            # Invoke LangGraph workflow
            result = supply_chain_graph.invoke({"query": query})
        except Exception as exc:
            logger.error("LangGraph execution failed: %s", exc)
            raise exc
            
        execution_time = time.perf_counter() - start_time
        logger.info("LangGraph execution completed in %.4f seconds", execution_time)
        
        # Update structured cache
        self._cache = PipelineCache(
            workflow_state=result,
            last_query=query,
            last_updated=datetime.now(timezone.utc).isoformat(),
            is_initialized=True,
            graph_execution_time_seconds=execution_time
        )
        return self._cache

# Global singleton
graph_service = GraphService()
