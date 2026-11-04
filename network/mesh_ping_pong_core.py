"""
Brahmastra Mesh Network - Day 50 Multi-Node Ping-Pong Engine
Simulates a 5-node interconnected mesh topology, executing encrypted ping-pong round-trips
with 0% packet loss verification and telemetry metrics logging.
"""

import time
import json
import hashlib
from typing import Dict, List, Tuple
from network.identity import NodeIdentity
from network.session_manager import SessionKeyManager
from network.ping_pong import PingPongEngine, MeshPacket

class MeshSimulationNetwork:
 """Manages 5-node full-mesh ephemeral session keys and packet routing."""

 def __init__(self, node_count: int = 5) -> None:
 self.node_count = node_count
 self.nodes: Dict[str, NodeIdentity] = {}
 self.session_managers: Dict[str, SessionKeyManager] = {}
 self.engines: Dict[str, Dict[str, PingPongEngine]] = {}
 self.node_ids: List[str] = []

 self._initialize_mesh_nodes()
 self._establish_full_mesh_sessions()

 def _get_peer_id(self, identity: NodeIdentity) -> str:
 return str(getattr(identity, "peer_id", hashlib.sha256(identity.get_public_bytes()).hexdigest()))

 def _initialize_mesh_nodes(self) -> None:
 """Create simulated distinct node identities."""
 for _ in range(self.node_count):
 node = NodeIdentity()
 p_id = self._get_peer_id(node)
 self.nodes[p_id] = node
 self.session_managers[p_id] = SessionKeyManager(node)
 self.engines[p_id] = {}
 self.node_ids.append(p_id)

 def _establish_full_mesh_sessions(self) -> None:
 """Establish mutual handshakes between every pair of nodes."""
 for i in range(len(self.node_ids)):
 for j in range(i + 1, len(self.node_ids)):
 id_a = self.node_ids[i]
 id_b = self.node_ids[j]

 node_a = self.nodes[id_a]
 node_b = self.nodes[id_b]

 mgr_a = self.session_managers[id_a]
 mgr_b = self.session_managers[id_b]

 mgr_a.complete_mutual_handshake(node_b)
 mgr_b.complete_mutual_handshake(node_a)

 shared_key_ab = mgr_a.active_sessions[id_b]

 self.engines[id_a][id_b] = PingPongEngine(node_a, shared_key_ab, id_b)
 self.engines[id_b][id_a] = PingPongEngine(node_b, shared_key_ab, id_a)

 def run_all_pairs_ping_pong(self, rounds_per_pair: int = 2) -> Tuple[int, int, float]:
 """Execute bi-directional encrypted ping-pong across all node pairings."""
 total_packets = 0
 successful_packets = 0
 latencies: List[float] = []

 for id_src in self.node_ids:
 for id_dst in self.node_ids:
 if id_src == id_dst:
 continue

 engine_src = self.engines[id_src][id_dst]
 engine_dst = self.engines[id_dst][id_src]

 for _ in range(rounds_per_pair):
 total_packets += 1
 t_start = time.perf_counter()

 ping_pkt = engine_src.create_ping()
 pong_pkt = engine_dst.handle_packet(ping_pkt)

 if pong_pkt is not None:
 verified, _ = engine_src.verify_pong(pong_pkt)
 if verified:
 successful_packets += 1
 latencies.append((time.perf_counter() - t_start) * 1000)

 avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
 return total_packets, successful_packets, avg_latency

if __name__ == "__main__":
 print("[INIT] Bootstrapping 5-Node Interconnected Mesh Network...")
 mesh = MeshSimulationNetwork(node_count=5)
 print(f"[ACTIVE] 5 Nodes Online. Handshakes verified. Total Pairwise Links: 20 directional links.")

 total_sent, total_recv, avg_lat = mesh.run_all_pairs_ping_pong(rounds_per_pair=2)
 packet_loss = ((total_sent - total_recv) / total_sent) * 100

 print(f"[METRICS] Total Ping-Pong Cycles: {total_sent}")
 print(f"[METRICS] Successfully Delivered & Verified: {total_recv}")
 print(f"[METRICS] Packet Loss: {packet_loss:.2f}%")
 print(f"[METRICS] Average Round-Trip Latency: {avg_lat:.3f} ms")

 if packet_loss == 0.0:
 print("[PASS] Zero Packet Drops Confirmed across 5-node topology!")
