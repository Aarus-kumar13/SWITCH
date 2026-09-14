import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("switch.memory.knowledge_graph")

class KnowledgeNode:
    def __init__(self, id: str, node_type: str, properties: Optional[Dict[str, Any]] = None):
        self.id = id
        self.node_type = node_type  # "User", "Tool", "Project", "Language", "Workflow"
        self.properties = properties or {}


class KnowledgeEdge:
    def __init__(self, source_id: str, relation: str, target_id: str, confidence: float = 1.0):
        self.source_id = source_id
        self.relation = relation  # "PREFERS", "USES", "WORKS_WITH", "HAS_WORKFLOW"
        self.target_id = target_id
        self.confidence = confidence


class PersonalKnowledgeGraph:
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []
        self._initialize_default_graph()

    def _initialize_default_graph(self):
        # User node
        self.add_node("user", "User", {"name": "Primary User"})
        # Preferred Tools
        self.add_node("vscode", "Tool", {"name": "VS Code"})
        self.add_node("python", "Language", {"name": "Python"})
        self.add_node("typescript", "Language", {"name": "TypeScript"})
        self.add_node("react", "Framework", {"name": "React"})

        self.add_edge("user", "PREFERS", "vscode")
        self.add_edge("user", "WORKS_WITH", "python")
        self.add_edge("user", "WORKS_WITH", "typescript")
        self.add_edge("user", "WORKS_WITH", "react")

    def add_node(self, node_id: str, node_type: str, properties: Optional[Dict[str, Any]] = None) -> KnowledgeNode:
        node = KnowledgeNode(node_id, node_type, properties)
        self.nodes[node_id] = node
        return node

    def add_edge(self, source_id: str, relation: str, target_id: str, confidence: float = 1.0) -> KnowledgeEdge:
        edge = KnowledgeEdge(source_id, relation, target_id, confidence)
        self.edges.append(edge)
        return edge

    def query_relations_for_node(self, node_id: str) -> List[Dict[str, Any]]:
        results = []
        for edge in self.edges:
            if edge.source_id == node_id:
                target_node = self.nodes.get(edge.target_id)
                results.append({
                    "relation": edge.relation,
                    "target_id": edge.target_id,
                    "target_type": target_node.node_type if target_node else "Unknown",
                    "properties": target_node.properties if target_node else {},
                    "confidence": edge.confidence,
                })
        return results

    def get_graph_summary(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "user_preferences": [r for r in self.query_relations_for_node("user")],
        }
