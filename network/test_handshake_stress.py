"""
Brahmastra Mesh Network - Day 48 Handshake Stress & Latency Audit Suite
Tests mass handshake concurrency, signature forgery rejection, latency guardrails (<10ms), and memory footprint.
"""

import time
import tracemalloc
import unittest
import secrets
from network.identity import NodeIdentity
from network.handshake import NodeHandshake, HandshakePayload
from network.session_manager import SessionKeyManager

class TestHandshakeStress(unittest.TestCase):

    def setUp(self):
        self.node_local = NodeIdentity()
        self.session_mgr = SessionKeyManager(self.node_local)

    def test_01_mass_handshake_and_unique_keys(self):
        """Stress Test: Execute 50 consecutive mutual handshakes and verify session keys."""
        print("\n[STRESS] Running 50 sequential handshakes and key derivations...")
        derived_keys = set()

        for _ in range(50):
            remote_node = NodeIdentity()
            latency = self.session_mgr.complete_mutual_handshake(remote_node)
            self.assertLess(latency, 10.0, f"Latency breached guardrail: {latency}ms")

        # Ensure all stored session keys are unique
        for key in self.session_mgr.active_sessions.values():
            derived_keys.add(key)

        self.assertEqual(len(derived_keys), 50, "Session key collision detected!")
        print("[PASS] 50 Handshakes executed successfully with 100% unique ephemeral session keys.")

    def test_02_invalid_signature_rejection(self):
        """Edge Case: Malicious/corrupt signature must be immediately rejected."""
        print("\n[EDGE-CASE] Testing signature tampering and unauthorized node rejection...")
        imposter_node = NodeIdentity()
        legit_handshake = NodeHandshake(self.node_local)

        challenge = legit_handshake.issue_challenge()
        corrupt_signature = secrets.token_bytes(64)

        tampered_payload = HandshakePayload(
            initiator_peer_id=imposter_node.get_peer_id() if hasattr(imposter_node, "get_peer_id") else "tampered_id",
            initiator_public_bytes=imposter_node.get_public_bytes(),
            nonce=challenge,
            signature=corrupt_signature
        )

        with self.assertRaises(PermissionError):
            legit_handshake.verify_remote_node(tampered_payload)
        print("[PASS] Tampered handshake payload successfully blocked by Zero-Trust guardrail.")

    def test_03_latency_and_memory_benchmarks(self):
        """Performance Audit: Verify latency and heap memory limits under stress."""
        print("\n[AUDIT] Auditing memory consumption and batch latency...")
        tracemalloc.start()
        start_time = time.perf_counter()

        remote_node = NodeIdentity()
        latency_ms = self.session_mgr.complete_mutual_handshake(remote_node)

        total_elapsed = (time.perf_counter() - start_time) * 1000
        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_kb = peak_mem / 1024
        print(f"[METRICS] Single Complete Mutual Handshake: {latency_ms:.3f} ms")
        print(f"[METRICS] Peak Memory Usage: {peak_kb:.2f} KB")

        self.assertLess(latency_ms, 10.0, "Handshake latency exceeded 10ms guardrail!")
        self.assertLess(peak_kb, 1024.0, "Memory footprint exceeded 1MB guardrail!")
        print("[PASS] Performance and memory metrics fully validated.")

if __name__ == "__main__":
    unittest.main()
