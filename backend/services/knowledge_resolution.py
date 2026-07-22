# Week 3 Day 1: Entity Resolution for KnowledgeBaseManager
def resolve_supply_chain_entity(entity_name: str):
    # Mapping raw incident tags to established infrastructure nodes
    mapping = {"factory_alpha": "Plant-01", "shanghai_port": "Node-Edge-4"}
    return mapping.get(entity_name.lower(), "Unknown Entity")
