"""
Brahmastra Mesh Network - Day 53 Kademlia Discovery & Node Synchronization Engine
Simulates bootstrap node joining, iterative FIND_NODE discovery, and routing table convergence.
"""

import time
import secrets
from typing import Dict, List, Tuple
from network.routing_table import Contact, RoutingTable

class KademliaNode:
 """Represents an active P2P node participating in Kademlia discovery."""

 def __init__(self, node_id: bytes, ip: str, port: int) -> None:
 self.contact = Contact(node_id=node_id, ip=ip, port=port)
 self.routing_table = RoutingTable(node_id)

 @property
 def node_id(self) -> bytes:
 return self.contact.node_id

 def handle_find_node(self, target_id: bytes, count: int = 5) -> List[Contact]:
 """RPC responder: returns k-closest known contacts to target_id."""
 return self.routing_table.find_closest_nodes(target_id, count=count)

 def bootstrap_into_network(self, known_bootstrap: 'KademliaNode') -> Tuple[int, float]:
 """
 Executes node join synchronization:
 1. Adds bootstrap node to local routing table.
 2. Queries bootstrap node for peers closest to self.node_id.
 3. Updates routing table with discovered peers and informs them.
 """
 t_start = time.perf_counter()

 # Step 1: Register bootstrap node locally
 self.routing_table.add_contact(known_bootstrap.contact)
 known_bootstrap.routing_table.add_contact(self.contact)

 # Step 2: Query bootstrap for closest nodes to self
 closest_peers = known_bootstrap.handle_find_node(self.node_id, count=10)

 # Step 3: Populate routing table and register with each discovered node
 discovered_count = 0
 for peer in closest_peers:
 if peer.node_id != self.node_id:
 if self.routing_table.add_contact(peer):
 discovered_count += 1

 elapsed_ms = (time.perf_counter() - t_start) * 1000
 return discovered_count, elapsed_ms

if __name__ == "__main__":
 print("[INIT] Setting up existing 5-node active Kademlia DHT cluster...")
 bootstrap_node = KademliaNode(secrets.token_bytes(32), "127.0.0.1", 8000)
 existing_nodes: List[KademliaNode] = [bootstrap_node]

 # Pre-populate 4 existing mesh nodes connected to bootstrap
 for i in range(1, 5):
 node = KademliaNode(secrets.token_bytes(32), "127.0.0.1", 8000 + i)
 bootstrap_node.routing_table.add_contact(node.contact)
 node.routing_table.add_contact(bootstrap_node.contact)
 existing_nodes.append(node)

 print(f"[STATUS] Bootstrap cluster initialized with {len(existing_nodes)} active nodes.")

 # Instantiate a brand new node with zero network state
 new_node_id = secrets.token_bytes(32)
 new_node = KademliaNode(new_node_id, "127.0.0.1", 9999)
 print(f"[JOIN] New Node {new_node_id.hex()[:16]}... attempting discovery via Bootstrap Node...")

 peers_found, discovery_time = new_node.bootstrap_into_network(bootstrap_node)

 print(f"[DISCOVERY] Discovered Peers: {peers_found}")
 print(f"[METRICS] Convergence Latency: {discovery_time:.3f} ms")
 
 # Verify closest peers resolution from new node
 closest = new_node.routing_table.find_closest_nodes(new_node_id, count=3)
 print(f"[VERIFY] Top closest peers recorded in new node's routing table:")
 for idx, c in enumerate(closest, 1):
 dist = new_node.routing_table.distance(c.node_id, new_node_id)
 print(f" {idx}. Peer Port: {c.port} | XOR Distance: {dist}")

 if peers_found > 0:
 print("[PASS] New Node successfully discovered and synchronized with active cluster!")
