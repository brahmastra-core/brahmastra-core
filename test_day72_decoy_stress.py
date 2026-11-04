"""
Brahmastra Core: Day 72 Stress Testing & Resource Verification
Module: Decoy Traffic Generator & Constant-Rate Pump
"""

import unittest
import time
import os
import resource
from decoy_traffic import DecoyTrafficGenerator, DECOY_PACKET_SIZE, DECOY_FLAG_HEADER
from decoy_traffic_core import ConstantRateTrafficPump, RelayDestinationProcessor

class TestDay72DecoyStress(unittest.TestCase):

 def test_01_payload_invariance_under_load(self):
 """Stress tests generation of 500 decoy packets to verify strict 4KB size invariance."""
 nodes = ["Node-A", "Node-B", "Node-C", "Node-D", "Node-E"]
 generator = DecoyTrafficGenerator(node_pool=nodes, packet_size=DECOY_PACKET_SIZE)
 
 for _ in range(500):
 decoy = generator.build_decoy_packet(hop_count=3)
 self.assertEqual(len(decoy.raw_bytes), 4096, "Size invariant violated!")
 self.assertTrue(decoy.raw_bytes.startswith(DECOY_FLAG_HEADER), "Decoy header missing!")
 self.assertEqual(len(decoy.target_route), 3, "Hop count mismatch!")

 def test_02_constant_rate_pump_throughput_latency(self):
 """Measures dispatch latency under a burst of 300 sequential slots."""
 nodes = ["Node-1", "Node-2", "Node-3", "Node-4"]
 pump = ConstantRateTrafficPump(node_pool=nodes, target_rate_hz=50.0)
 
 # Inject 100 real payloads among slots
 for i in range(100):
 pump.submit_real_packet(f"REAL_BURST_MSG_{i}".encode("utf-8"))

 total_slots = 300
 start_time = time.perf_counter()
 for _ in range(total_slots):
 pump.dispatch_next_slot()
 duration = time.perf_counter() - start_time

 avg_latency_ms = (duration / total_slots) * 1000
 print(f"\n[METRIC] Decoy Dispatch Latency per Packet: {avg_latency_ms:.4f} ms")
 self.assertLess(avg_latency_ms, 1.0, "Dispatch latency exceeded 1ms threshold!")
 self.assertEqual(pump.transmitted_count, 300)
 self.assertEqual(pump.real_transmitted, 100)
 self.assertEqual(pump.decoy_transmitted, 200)

 def test_03_silent_drop_integrity_under_burst(self):
 """Validates that 200 decoy packets are silently dropped without leaking to user-space."""
 processor = RelayDestinationProcessor()
 nodes = ["Node-Alpha", "Node-Beta", "Node-Gamma"]
 generator = DecoyTrafficGenerator(node_pool=nodes)

 for _ in range(200):
 decoy = generator.build_decoy_packet(hop_count=3)
 res = processor.process_incoming_packet(decoy.raw_bytes)
 self.assertIsNone(res, "Decoy packet leaked into user-space delivery!")

 self.assertEqual(processor.silent_dropped_count, 200)
 self.assertEqual(processor.delivered_count, 0)

 def test_04_memory_ceiling_under_80mb(self):
 """Strict verification that decoy processing remains well below the 80MB RAM limit."""
 usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 mem_mb = usage_kb / 1024.0
 print(f"[METRIC] Current Process Memory: {mem_mb:.2f} MB")
 self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

if __name__ == "__main__":
 unittest.main()
