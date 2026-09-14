import pytest
from packages.memory.knowledge_graph import PersonalKnowledgeGraph

def test_knowledge_graph_structure():
    kg = PersonalKnowledgeGraph()
    summary = kg.get_graph_summary()
    assert summary["total_nodes"] >= 5
    assert summary["total_edges"] >= 4

    user_relations = kg.query_relations_for_node("user")
    rel_names = [r["relation"] for r in user_relations]
    assert "PREFERS" in rel_names
    assert "WORKS_WITH" in rel_names
