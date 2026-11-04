"""
Brahmastra Mesh Network - Day 51 Stress & Benchmark Suite
Validates 5-node ping-pong protocol against edge cases, tampered ciphertext,
rapid packet bursts, latency constraints, and memory consumption.
"""

import unittest
import tracemalloc
import hashlib
from network.identity import NodeIdentity
from network.session_manager import SessionKeyManager
from network.ping_pong import PingPongEngine, MeshPacket
from network.mesh_ping_pong_core import MeshSimulationNetwork

def get_peer_id(identity: NodeIdentity) -> str:
 return str(getattr(identity, "peer_id", hashlib.sha256(identity.get_public_bytes()).hexdigest()))

class TestMeshPingPongStressSuite(unittest.TestCase):
 """Stress testing suite for 5-node ping-pong mesh communication."""

 def setUp(self) -> None:
 tracemalloc.start()
 self.mesh = MeshSimulationNetwork(node_count=5)

 def tearDown(self) -> None:
 tracemalloc.stop()

 def test_01_burst_traffic_zero_loss(self) -> None:
 """Verify zero packet drops across all directional links under burst conditions."""
 rounds = 5 # 5 * 20 = 100 ping-pong rounds
 total_sent, total_recv, _ = self.mesh.run_all_pairs_ping_pong(rounds_per_pair=rounds)
 
 self.assertEqual(total_sent, 100, "Expected exactly 100 total packets transmitted")
 self.assertEqual(total_recv, 100, "Packet drop detected! Expected 100% successful round-trips")

 def test_02_tampered_ciphertext_rejection(self) -> None:
 """Verify integrity checks reject modified payloads without crashing nodes."""
 node_a = NodeIdentity()
 node_b = NodeIdentity()
 mgr_a = SessionKeyManager(node_a)
 mgr_b = SessionKeyManager(node_b)

 mgr_a.complete_mutual_handshake(node_b)
 mgr_b.complete_mutual_handshake(node_a)

 p_id_b = get_peer_id(node_b)
 p_id_a = get_peer_id(node_a)
 key = mgr_a.active_sessions[p_id_b]

 engine_a = PingPongEngine(node_a, key, p_id_b)
 engine_b = PingPongEngine(node_b, key, p_id_a)

 valid_pkt = engine_a.create_ping()

 # Flip bytes in ciphertext to simulate MITM tampering
 corrupted_ct = bytearray(valid_pkt.ciphertext)
 corrupted_ct[0] ^= 0xFF
 corrupted_pkt = MeshPacket(
 source_peer_id=valid_pkt.source_peer_id,
 target_peer_id=valid_pkt.target_peer_id,
 nonce=valid_pkt.nonce,
 ciphertext=bytes(corrupted_ct)
 )

 with self.assertRaises(PermissionError, msg="Corrupted datagram must raise integrity check failure"):
 engine_b.handle_packet(corrupted_pkt)

 def test_03_latency_and_memory_benchmarks(self) -> None:
 """Ensure RTT latency remains under 5ms and memory allocation stays under 5MB."""
 _, _, avg_latency_ms = self.mesh.run_all_pairs_ping_pong(rounds_per_pair=2)
 current_mem, peak_mem = tracemalloc.get_traced_memory()
 peak_mb = peak_mem / (1024 * 1024)

 self.assertLess(avg_latency_ms, 5.0, f"Average RTT latency {avg_latency_ms:.3f}ms exceeded 5.0ms threshold")
 self.assertLess(peak_mb, 5.0, f"Peak memory usage {peak_mb:.2f}MB exceeded 5.0MB limit")

if __name__ == "__main__":
 unittest.main()
