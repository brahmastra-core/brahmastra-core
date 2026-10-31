"""
Brahmastra Mesh Network - Day 54 Kademlia DHT Stress & Benchmark Suite
Validates routing table constraints, k-bucket overflow, duplicate handling,
high-volume discovery convergence, and memory footprint bounds.
"""

import unittest
import tracemalloc
import time
import secrets
from network.routing_table import Contact, RoutingTable, K_BUCKET_SIZE
from network.kademlia_discovery import KademliaNode

class TestKademliaStressSuite(unittest.TestCase):
    """Comprehensive stress tests for Kademlia DHT routing and discovery."""

    def setUp(self) -> None:
        tracemalloc.start()
        self.local_id = secrets.token_bytes(32)
        self.routing_table = RoutingTable(self.local_id)

    def tearDown(self) -> None:
        tracemalloc.stop()

    def test_01_bucket_overflow_and_deduplication(self) -> None:
        """Ensure K-bucket adheres strictly to capacity limit and deduplicates peers."""
        # Target a specific synthetic bucket by crafting peer IDs
        base_id = bytearray(self.local_id)
        base_id[0] ^= 0x01  # Flips 1 bit to cluster into the same target bucket

        # Insert 30 nodes with the same prefix into the routing table
        added_count = 0
        for i in range(30):
            mock_id = bytearray(base_id)
            mock_id[-1] = (mock_id[-1] + i) % 256
            contact = Contact(node_id=bytes(mock_id), ip="127.0.0.1", port=10000 + i)
            if self.routing_table.add_contact(contact):
                added_count += 1

        b_idx = self.routing_table._get_bucket_index(bytes(base_id))
        bucket_len = len(self.routing_table.buckets[b_idx].contacts)

        # Bucket should not exceed capacity k (20)
        self.assertLessEqual(bucket_len, K_BUCKET_SIZE, f"Bucket overflow detected: {bucket_len} > {K_BUCKET_SIZE}")

        # Test deduplication: re-inserting an existing contact must return True and not increase bucket size
        existing_contact = self.routing_table.buckets[b_idx].contacts[0]
        re_added = self.routing_table.add_contact(existing_contact)
        self.assertTrue(re_added, "Re-adding an active contact should refresh and return True")
        self.assertEqual(len(self.routing_table.buckets[b_idx].contacts), bucket_len, "Duplicate contact added to bucket")

    def test_02_self_and_invalid_id_rejection(self) -> None:
        """Verify routing table strictly rejects self-insertion and invalid ID lengths."""
        # Self-insertion rejection
        self_contact = Contact(node_id=self.local_id, ip="127.0.0.1", port=9000)
        self.assertFalse(self.routing_table.add_contact(self_contact), "Local node must reject adding itself")

        # Invalid ID length rejection on table initialization
        with self.assertRaises(ValueError, msg="Routing table must reject non-32-byte node ID"):
            RoutingTable(b"too_short_id")

    def test_03_high_volume_discovery_and_latency(self) -> None:
        """Validate multi-node DHT bootstrap discovery latency under 10.0 ms."""
        bootstrap_node = KademliaNode(secrets.token_bytes(32), "127.0.0.1", 7000)
        
        # Populate bootstrap node with 50 synthetic network peers
        for i in range(50):
            peer = Contact(node_id=secrets.token_bytes(32), ip="127.0.0.1", port=7001 + i)
            bootstrap_node.routing_table.add_contact(peer)

        new_node = KademliaNode(secrets.token_bytes(32), "127.0.0.1", 8888)
        
        # Execute join discovery and measure convergence latency
        peers_found, latency_ms = new_node.bootstrap_into_network(bootstrap_node)

        self.assertGreater(peers_found, 0, "New node must discover peers from bootstrap")
        self.assertLess(latency_ms, 10.0, f"Discovery convergence latency {latency_ms:.3f}ms exceeded 10.0ms threshold")

    def test_04_memory_consumption_benchmark(self) -> None:
        """Ensure memory allocation during extensive routing operations remains under 5.0 MB."""
        # Perform 200 XOR lookups and insertions
        for i in range(200):
            cid = secrets.token_bytes(32)
            self.routing_table.add_contact(Contact(node_id=cid, ip="127.0.0.1", port=6000 + i))
            self.routing_table.find_closest_nodes(cid, count=5)

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        peak_mb = peak_mem / (1024 * 1024)

        self.assertLess(peak_mb, 5.0, f"Peak memory usage {peak_mb:.2f}MB exceeded 5.0MB limit")

if __name__ == "__main__":
    unittest.main()
