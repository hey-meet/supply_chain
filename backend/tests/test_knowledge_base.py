# backend/tests/test_knowledge_base.py
from backend.data.manager import kb_manager

def test_knowledge_base_loading_and_query():
    """Ensure data files load correctly and query logic returns accurate structures."""
    assets = kb_manager.get_all_assets()
    assert "production_plants" in assets
    assert "suppliers" in assets
    
    # Test individual asset lookups
    plant = kb_manager.get_plant_by_id("PLNT-PUNE-01")
    assert plant is not None
    assert plant["name"] == "Pune Automotive Assembly Core"