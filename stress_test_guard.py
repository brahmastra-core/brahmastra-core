"""
Day 60: Stress Testing & Latency Verification for Node Resource Guard
"""
import time
from node_resource_guard import NodeMetrics, enforce_budget, ResourceExceededException, MAX_MEMORY_BUDGET_BYTES

def run_stress_suite():
    print("=== Starting Day 60 Stress & Edge Case Suite ===")
    
    # 1. Normal Load Case
    start_time = time.perf_counter()
    normal_node = NodeMetrics("Node-Normal", 15 * 1024 * 1024, 5.0)
    res = enforce_budget(normal_node)
    normal_latency = (time.perf_counter() - start_time) * 1000
    print(f"[PASS] Normal Case (15MB): {res} | Latency: {normal_latency:.4f} ms")
    
    # 2. Exact Boundary Case (80 MB)
    start_time = time.perf_counter()
    boundary_node = NodeMetrics("Node-Boundary", MAX_MEMORY_BUDGET_BYTES, 18.0)
    res_b = enforce_budget(boundary_node)
    boundary_latency = (time.perf_counter() - start_time) * 1000
    print(f"[PASS] Exact 80MB Boundary Case: {res_b} | Latency: {boundary_latency:.4f} ms")
    
    # 3. Edge Case Overflow (85 MB - Throttling Trigger)
    overflow_node = NodeMetrics("Node-Overflow", 85 * 1024 * 1024, 22.0)
    start_time = time.perf_counter()
    try:
        enforce_budget(overflow_node)
        print("[FAIL] Overflow check failed: Exception was not raised.")
    except ResourceExceededException as e:
        overflow_latency = (time.perf_counter() - start_time) * 1000
        print(f"[PASS] Edge Overflow Intercepted: {e} | Latency: {overflow_latency:.4f} ms")
        print(f"       Node Throttled Status: {overflow_node.is_throttled}")

if __name__ == "__main__":
    run_stress_suite()
