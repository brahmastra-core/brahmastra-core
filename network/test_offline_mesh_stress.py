"""
Brahmastra Mesh Network - Day 57 Offline Local Mesh Stress & Benchmark Suite
Validates malformed beacon resilience, self-echo prevention, high-volume socket flood,
processing latency, and memory footprint constraints.
"""

import unittest
import tracemalloc
import time
import secrets
import json
from network.offline_mesh_router import OfflineMeshRouter, TransportMedium
from network.offline_mesh_engine import OfflineMeshEngine

class TestOfflineMeshStressSuite(unittest.TestCase):
 """Stress tests and edge case verification for zero-internet offline mesh."""

 def setUp(self) -> None:
 tracemalloc.start()
 self.node_id = secrets.token_bytes(32)
 self.router = OfflineMeshRouter(self.node_id, bind_port=9700)

 def tearDown(self) -> None:
 tracemalloc.stop()

 def test_01_malformed_beacon_and_protocol_rejection(self) -> None:
 """Verify router safely drops corrupted JSON and foreign protocol beacons without crashing."""
 # Malformed raw bytes
 corrupted_payload = b"\x00\xff\xfeMALFORMED_GARBAGE_DATA"
 res1 = self.router.handle_incoming_beacon(corrupted_payload, "192.168.1.50")
 self.assertFalse(res1, "Router must safely reject non-JSON byte payloads")

 # Valid JSON but spoofed / wrong protocol header
 invalid_protocol = json.dumps({
 "protocol": "FOREIGN_ATTACK_MESH_V9",
 "node_id": secrets.token_bytes(32).hex(),
 "port": 9701
 }).encode("utf-8")
 res2 = self.router.handle_incoming_beacon(invalid_protocol, "192.168.1.51")
 self.assertFalse(res2, "Router must reject unknown protocol signatures")

 def test_02_self_echo_prevention(self) -> None:
 """Ensure node rejects its own looped-back broadcast beacons."""
 own_beacon = self.router.craft_discovery_beacon()
 res = self.router.handle_incoming_beacon(own_beacon, "127.0.0.1", TransportMedium.UDP_BROADCAST)
 self.assertFalse(res, "Node must reject registering itself as an offline peer")
 self.assertEqual(len(self.router.local_peers), 0, "Local peers table must remain empty after self-echo")

 def test_03_high_volume_local_socket_stress(self) -> None:
 """Test high-throughput packet flood between local nodes without packet drop or deadlock."""
 target_port = 9710
 receiver = OfflineMeshEngine(secrets.token_bytes(32), port=target_port)
 sender = OfflineMeshEngine(secrets.token_bytes(32), port=9711)

 packet_count = 100
 sent_hashes = []

 t_start = time.perf_counter()
 for i in range(packet_count):
 pkt_payload = f"ENCRYPTED_PACKET_{i}_{secrets.token_hex(8)}".encode("utf-8")
 sent_hashes.append(pkt_payload)
 sender.send_offline_packet("127.0.0.1", target_port, pkt_payload)

 # Allow socket listener loop to ingest
 time.sleep(0.15)
 latency_ms = (time.perf_counter() - t_start) * 1000

 received_count = len(receiver.received_packets)
 receiver.close()
 sender.close()

 self.assertGreaterEqual(received_count, packet_count * 0.95, f"High packet drop during local stress: received {received_count}/{packet_count}")
 self.assertLess(latency_ms, 500.0, f"Stress processing latency {latency_ms:.2f}ms exceeded 500ms limit")

 def test_04_memory_footprint_benchmark(self) -> None:
 """Validate offline mesh cache and socket operations retain < 5.0 MB RAM."""
 # Populate router with 300 synthetic discovered peers across mediums
 for i in range(300):
 pid = secrets.token_bytes(32)
 med = TransportMedium.WIFI_DIRECT if i % 2 == 0 else TransportMedium.BLE
 self.router.handle_incoming_beacon(
 json.dumps({"protocol": "BRAHMASTRA_OFFLINE_MESH_V1", "node_id": pid.hex(), "port": 9000 + (i % 500)}).encode("utf-8"),
 f"192.168.1.{i % 250}",
 med
 )

 current_mem, peak_mem = tracemalloc.get_traced_memory()
 peak_mb = peak_mem / (1024 * 1024)

 self.assertLess(peak_mb, 5.0, f"Peak memory usage {peak_mb:.2f}MB exceeded 5.0MB limit")

if __name__ == "__main__":
 unittest.main()
