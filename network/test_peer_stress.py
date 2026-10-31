"""
Brahmastra Mesh Network - Day 45 Peer Identity Stress & Performance Suite
Tests mass identity derivation, peer router edge cases, latency, and memory footprint.
"""

import time
import tracemalloc
import unittest
import secrets
from network.identity import NodeIdentity
from network.peer_router import PeerRouter

class TestPeerIdentityStress(unittest.TestCase):

    def setUp(self):
        self.local_peer = secrets.token_hex(32)
        self.router = PeerRouter(local_peer_id=self.local_peer)

    def test_01_mass_identity_and_edge_cases(self):
        """Stress test: Generate multiple cryptographic identities and verify edge cases."""
        print("\n[STRESS] Running mass identity generation & verification...")
        for _ in range(50):
            node = NodeIdentity()
            msg = secrets.token_bytes(64)
            sig = node.sign(msg)
            self.assertTrue(NodeIdentity.verify(node.get_public_bytes(), msg, sig))

        # Edge Case 1: Invalid Peer ID length rejection (< 64 hex characters)
        with self.assertRaises(ValueError):
            self.router.register_peer("invalid_short_peer_id", {"status": "ACTIVE"})

        # Edge Case 2: Unregistered route lookup
        unregistered_peer = secrets.token_hex(32)
        with self.assertRaises(LookupError):
            self.router.route_packet(unregistered_peer, b"TEST_DATA")
        print("[PASS] Mass cryptographic verification and edge case handling validated.")

    def test_02_memory_and_latency_audit(self):
        """Audit: Measure execution latency and heap memory consumption."""
        print("\n[AUDIT] Measuring identity derivation latency and memory footprint...")
        tracemalloc.start()
        start_time = time.perf_counter()

        # Batch register routes
        peer_ids = []
        for _ in range(100):
            pid = secrets.token_hex(32)
            peer_ids.append(pid)
            self.router.register_peer(pid, {"hop_count": 1, "protocol": "BRAHMASTRA_P2P"})

        elapsed_ms = (time.perf_counter() - start_time) * 1000
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_kb = peak_mem / 1024
        print(f"[METRICS] 100 Peer Routes Processed in: {elapsed_ms:.2f} ms")
        print(f"[METRICS] Peak Memory Allocation: {peak_kb:.2f} KB")

        # Threshold assertions (Performance Guardrails)
        self.assertLess(elapsed_ms, 250.0, "Latency exceeded 250ms threshold")
        self.assertLess(peak_kb, 1024.0, "Memory footprint exceeded 1MB threshold")
        self.assertEqual(self.router.total_known_peers(), 100)
        print("[PASS] Latency and memory footprint within strict boundaries.")

if __name__ == "__main__":
    unittest.main()
