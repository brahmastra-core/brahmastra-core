"""
Brahmastra Core: Day 87 - Self-Healing Routing Stress Testing & Edge Cases
"""

import unittest
import time
import resource
import os
import hashlib
from self_healing_core import SelfHealingCoreEngine, NodeMetadata, Packet

class TestDay87SelfHealingStress(unittest.TestCase):

 def setUp(self):
 self.nodes = {
 "Node-A": NodeMetadata("Node-A"),
 "Node-B": NodeMetadata("Node-B"),
 "Node-C": NodeMetadata("Node-C"),
 "Node-D": NodeMetadata("Node-D"),
 "Node-E": NodeMetadata("Node-E"),
 "Node-F": NodeMetadata("Node-F")
 }
 self.engine = SelfHealingCoreEngine(node_pool=self.nodes)

 def test_01_concurrent_multiple_node_failures(self):
 """Edge Case: Simultaneously drop both Node-B and Node-C."""
 self.nodes["Node-B"].is_alive = False
 self.nodes["Node-C"].is_alive = False

 raw_data = os.urandom(2048)
 pkt = Packet(
 packet_id="pkt-stress-multi",
 payload=raw_data,
 payload_hash=hashlib.sha256(raw_data).hexdigest()
 )

 success, path, _ = self.engine.send_packet(pkt)
 self.assertTrue(success)
 self.assertNotIn("Node-B", path)
 self.assertNotIn("Node-C", path)
 self.assertIn("Node-E", path)
 self.assertIn("Node-F", path)
 self.assertEqual(path, ["Node-A", "Node-E", "Node-F", "Node-D"])

 def test_02_standby_exhaustion_graceful_handling(self):
 """Edge Case: When standbys are exhausted, system must raise clean error without crash."""
 self.nodes["Node-E"].is_alive = False
 self.nodes["Node-F"].is_alive = False
 self.nodes["Node-C"].is_alive = False

 pkt = Packet(
 packet_id="pkt-exhaustion",
 payload=b"test",
 payload_hash=hashlib.sha256(b"test").hexdigest()
 )

 with self.assertRaises(RuntimeError) as context:
 self.engine.send_packet(pkt)
 self.assertIn("No standby nodes available", str(context.exception))

 def test_03_zero_packet_loss_under_burst_churn(self):
 """Verifies zero packet loss and latency bounds across 500 burst transmissions."""
 start_time = time.perf_counter()

 for i in range(500):
 # Toggle Node-C state
 self.nodes["Node-C"].is_alive = (i % 2 == 0)
 self.nodes["Node-E"].is_alive = True

 data = os.urandom((i * 7) % 1024 + 64)
 pkt = Packet(
 packet_id=f"burst-pkt-{i}",
 payload=data,
 payload_hash=hashlib.sha256(data).hexdigest()
 )
 success, path, _ = self.engine.send_packet(pkt)
 self.assertTrue(success)

 total_elapsed_ms = (time.perf_counter() - start_time) * 1000
 avg_latency_ms = total_elapsed_ms / 500
 print(f"\n[METRIC] Mean Failover Routing Latency: {avg_latency_ms:.4f} ms")
 self.assertLess(avg_latency_ms, 1.0, "Average latency exceeded 1.0ms limit!")

 def test_04_memory_and_latency_thresholds(self):
 """Ensures total memory footprint remains strictly beneath 80MB RAM."""
 usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 mem_mb = usage_kb / 1024.0
 print(f"[METRIC] Self-Healing Pipeline Memory Footprint: {mem_mb:.2f} MB")
 self.assertLess(mem_mb, 80.0, "Memory limit exceeded 80MB threshold!")

if __name__ == "__main__":
 unittest.main()
