import unittest
from node_resource_guard import NodeMetrics, enforce_budget, ResourceExceededException, MAX_MEMORY_BUDGET_BYTES

class TestNodeResourceStress(unittest.TestCase):
    def test_01_normal_payload(self):
        node = NodeMetrics("Node-1", 10 * 1024 * 1024, 2.0)
        self.assertEqual(enforce_budget(node), "RESOURCE_OK")
        self.assertFalse(node.is_throttled)

    def test_02_exact_boundary(self):
        node = NodeMetrics("Node-2", MAX_MEMORY_BUDGET_BYTES, 15.0)
        self.assertEqual(enforce_budget(node), "RESOURCE_OK")
        self.assertFalse(node.is_throttled)

    def test_03_overflow_rejection(self):
        node = NodeMetrics("Node-3", MAX_MEMORY_BUDGET_BYTES + 1024, 25.0)
        with self.assertRaises(ResourceExceededException):
            enforce_budget(node)
        self.assertTrue(node.is_throttled)

if __name__ == "__main__":
    unittest.main()
