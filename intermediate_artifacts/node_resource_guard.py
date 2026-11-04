"""
Brahmastra Core - Node Resource Guard & Threshold Enforcement
Day 58: Data Structures & Function Signatures
"""
from dataclasses import dataclass
from typing import Optional

MAX_MEMORY_BUDGET_BYTES: int = 80 * 1024 * 1024 # 80 MB Hard Limit
MAX_CPU_PERCENT_LIMIT: float = 20.0 # 20% CPU Limit

@dataclass
class NodeMetrics:
 node_id: str
 current_memory_bytes: int
 current_cpu_percent: float
 is_throttled: bool = False

class ResourceExceededException(Exception):
 """Raised when memory or CPU budget exceeds Day 58 thresholds."""
 pass

def check_memory_limit(metrics: NodeMetrics) -> bool:
 """Verifies if the current node exceeds the 80 MB hard memory threshold."""
 return metrics.current_memory_bytes <= MAX_MEMORY_BUDGET_BYTES

def enforce_budget(metrics: NodeMetrics) -> Optional[str]:
 """Applies traffic throttling if container approaches memory budget."""
 if not check_memory_limit(metrics):
 metrics.is_throttled = True
 raise ResourceExceededException(
 f"Node {metrics.node_id} exceeded 80MB limit: {metrics.current_memory_bytes} bytes"
 )
 return "RESOURCE_OK"

if __name__ == "__main__":
 test_node = NodeMetrics("Node-A", 12 * 1024 * 1024, 2.5)
 print(f"[{test_node.node_id}] Budget Check: {enforce_budget(test_node)}")
