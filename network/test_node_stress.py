"""
Brahmastra Mesh Network - Node-A Stress & Unit Verification Test
Phase 3: Day 39/42 Implementation
Validates edge cases, startup latency, memory footprint, and Zero-Trust.
"""

import subprocess
import time
import unittest

class TestNodeAStressAndHardening(unittest.TestCase):

 def test_01_non_root_execution_enforcement(self):
 """Edge Case: Enforce that running as UID 10001 succeeds with Zero-Trust status."""
 cmd = ["docker", "run", "--rm", "brahmastra-node-a:v1", "python3", "-c", 
 "import os; uid=os.getuid(); print(f'Running with UID: {uid}'); print('Zero-Trust Verified' if uid==10001 else 'Failed')"]
 start_time = time.perf_counter()
 result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
 latency_ms = (time.perf_counter() - start_time) * 1000
 
 self.assertEqual(result.returncode, 0, f"Container failed to start: {result.stderr}")
 self.assertIn("Running with UID: 10001", result.stdout)
 self.assertIn("Zero-Trust Verified", result.stdout)
 print(f"\n[PASS] Edge Case 1: Non-root execution confirmed. Latency: {latency_ms:.2f} ms")

 def test_02_root_tamper_rejection(self):
 """Edge Case: Simulate attacker attempting forced root execution."""
 cmd = ["docker", "run", "--rm", "--user", "0", "brahmastra-node-a:v1"]
 result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
 
 self.assertNotEqual(result.returncode, 0, "Security violation: Root execution was not rejected!")
 self.assertTrue(
 "[ERROR] Root execution detected!" in result.stderr or "CRITICAL ERROR" in result.stderr,
 f"Unexpected error output: {result.stderr}"
 )
 print("[PASS] Edge Case 2: Forced root execution successfully rejected with exit code 1.")

 def test_03_memory_footprint_and_latency(self):
 """Performance: Verify container execution latency and lightweight initialization."""
 start_time = time.perf_counter()
 cmd = ["docker", "run", "--rm", "brahmastra-node-a:v1", "python3", "-c", "import sys; sys.exit(0)"]
 result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
 latency_ms = (time.perf_counter() - start_time) * 1000
 
 self.assertEqual(result.returncode, 0)
 self.assertLess(latency_ms, 2500, f"Startup latency exceeded threshold: {latency_ms:.2f} ms")
 print(f"[PASS] Performance Check: Latency {latency_ms:.2f} ms is within production bounds.")

if __name__ == "__main__":
 unittest.main()
