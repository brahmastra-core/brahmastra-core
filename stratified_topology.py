"""
Brahmastra Core: Stratified Topology Engine
Day 73: Architecture & Interface Design
"""

from enum import IntEnum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import secrets

class LayerType(IntEnum):
 INGRESS = 1
 MIX = 2
 EGRESS = 3

@dataclass
class StratumNode:
 node_id: str
 layer: LayerType
 endpoint: str
 capacity_weight: float = 1.0

class StratifiedTopologyEngine:
 """
 Task 1 & Task 2: Architecture and Routing Interface for Stratified Topology.
 Guarantees strict Layer 1 -> Layer 2 -> Layer 3 paths without cycles.
 """
 def __init__(self):
 self.strata: Dict[LayerType, List[StratumNode]] = {
 LayerType.INGRESS: [],
 LayerType.MIX: [],
 LayerType.EGRESS: []
 }
 self.routing_table: Dict[str, List[str]] = {}

 def register_node(self, node: StratumNode) -> None:
 """Registers a node into its assigned stratum layer."""
 self.strata[node.layer].append(node)
 self._rebuild_routing_tables()

 def _rebuild_routing_tables(self) -> None:
 """
 Task 2: Sets strict forward-only routing rules:
 Layer 1 strictly maps next-hops to Layer 2.
 Layer 2 strictly maps next-hops to Layer 3.
 Layer 3 terminates (empty next-hop list).
 """
 self.routing_table.clear()
 
 # Layer 1 -> Layer 2
 l2_node_ids = [n.node_id for n in self.strata[LayerType.MIX]]
 for l1_node in self.strata[LayerType.INGRESS]:
 self.routing_table[l1_node.node_id] = list(l2_node_ids)

 # Layer 2 -> Layer 3
 l3_node_ids = [n.node_id for n in self.strata[LayerType.EGRESS]]
 for l2_node in self.strata[LayerType.MIX]:
 self.routing_table[l2_node.node_id] = list(l3_node_ids)

 # Layer 3 -> Exit (terminal)
 for l3_node in self.strata[LayerType.EGRESS]:
 self.routing_table[l3_node.node_id] = []

 def get_valid_next_hops(self, current_node_id: str) -> List[str]:
 return self.routing_table.get(current_node_id, [])

 def build_stratified_path(self) -> List[StratumNode]:
 """
 Constructs a verified 3-hop stratified circuit (L1 -> L2 -> L3).
 """
 if not (self.strata[LayerType.INGRESS] and self.strata[LayerType.MIX] and self.strata[LayerType.EGRESS]):
 raise ValueError("Incomplete topology: every stratum layer must have at least one active node!")

 n1 = secrets.choice(self.strata[LayerType.INGRESS])
 n2 = secrets.choice(self.strata[LayerType.MIX])
 n3 = secrets.choice(self.strata[LayerType.EGRESS])

 return [n1, n2, n3]

if __name__ == "__main__":
 print("=== Testing Stratified Topology Interface (Day 73) ===")
 topo = StratifiedTopologyEngine()

 # Register Nodes across the 3 layers
 topo.register_node(StratumNode("Node-Ingress-1", LayerType.INGRESS, "10.0.1.1:9001"))
 topo.register_node(StratumNode("Node-Ingress-2", LayerType.INGRESS, "10.0.1.2:9001"))

 topo.register_node(StratumNode("Node-Mix-1", LayerType.MIX, "10.0.2.1:9002"))
 topo.register_node(StratumNode("Node-Mix-2", LayerType.MIX, "10.0.2.2:9002"))
 topo.register_node(StratumNode("Node-Mix-3", LayerType.MIX, "10.0.2.3:9002"))

 topo.register_node(StratumNode("Node-Egress-1", LayerType.EGRESS, "10.0.3.1:9003"))
 topo.register_node(StratumNode("Node-Egress-2", LayerType.EGRESS, "10.0.3.2:9003"))

 # Test Stratified Path Generation
 path = topo.build_stratified_path()
 path_str = " -> ".join([f"{n.node_id} (L{n.layer.value})" for n in path])
 print(f"[PASS] Task 1: Stratified Circuit Generated: {path_str}")

 # Verify Strict Layer Transition Invariant
 assert path[0].layer == LayerType.INGRESS, "Hop 0 is not Ingress!"
 assert path[1].layer == LayerType.MIX, "Hop 1 is not Mix!"
 assert path[2].layer == LayerType.EGRESS, "Hop 2 is not Egress!"
 print(f"[PASS] Task 2: Path Invariant Verified (L1 -> L2 -> L3)")

 # Verify Routing Table Boundaries
 l1_hops = topo.get_valid_next_hops("Node-Ingress-1")
 l2_hops = topo.get_valid_next_hops("Node-Mix-1")
 l3_hops = topo.get_valid_next_hops("Node-Egress-1")

 print(f"[PASS] Task 2: Ingress Valid Next Hops : {l1_hops}")
 print(f"[PASS] Task 2: Mix Valid Next Hops : {l2_hops}")
 print(f"[PASS] Task 2: Egress Terminal Hops : {l3_hops}")

 assert all(h.startswith("Node-Mix") for h in l1_hops), "Ingress leaked outside Layer 2!"
 assert all(h.startswith("Node-Egress") for h in l2_hops), "Mix leaked outside Layer 3!"
 assert len(l3_hops) == 0, "Egress node must be terminal!"
 print("=== Day 73 Architecture & Interface: READY ===")
