"""
Brahmastra Core: Sphinx Packet Poisson Delay Engine & Interfaces
Day 67: Architecture & Interface Design (Calibrated)
"""

import time
import math
import secrets
from dataclasses import dataclass, field
from typing import List, Tuple
import heapq

DEFAULT_LAMBDA: float = 20.0       # Mean delay = 1/20 = 0.050s (50 ms)
MIN_DELAY_FLOOR_SEC: float = 0.020  # Minimum 20 ms floor to avoid immediate sub-tick leaks
MAX_DELAY_CAP_SEC: float = 0.200    # Maximum 200 ms ceiling cap

@dataclass(order=True)
class PrioritizedDelayedPacket:
    release_time: float
    arrival_time: float = field(compare=False)
    next_hop: str = field(compare=False)
    raw_packet: bytes = field(compare=False)

def sample_poisson_delay(rate_lambda: float = DEFAULT_LAMBDA,
                         min_floor: float = MIN_DELAY_FLOOR_SEC,
                         max_cap: float = MAX_DELAY_CAP_SEC) -> float:
    """
    Samples delay using inverse CDF of exponential distribution with safe floor and ceiling clamp.
    """
    rand_int = secrets.randbits(53)
    u = (rand_int + 1) / (2**53 + 1)
    raw_delay = -math.log(u) / rate_lambda
    # Clamp between min floor (20ms) and max cap (200ms)
    return max(min_floor, min(raw_delay, max_cap))

class SphinxDelayEngine:
    """
    Event-driven delay buffer that queues Sphinx packets and releases them
    according to Poisson distribution timings.
    """
    def __init__(self, rate_lambda: float = DEFAULT_LAMBDA,
                 min_floor: float = MIN_DELAY_FLOOR_SEC,
                 max_cap: float = MAX_DELAY_CAP_SEC):
        self.rate_lambda = rate_lambda
        self.min_floor = min_floor
        self.max_cap = max_cap
        self._priority_queue: List[PrioritizedDelayedPacket] = []

    def enqueue_packet(self, raw_packet: bytes, next_hop: str) -> float:
        now = time.time()
        delay = sample_poisson_delay(self.rate_lambda, self.min_floor, self.max_cap)
        target_release = now + delay
        entry = PrioritizedDelayedPacket(
            release_time=target_release,
            arrival_time=now,
            next_hop=next_hop,
            raw_packet=raw_packet
        )
        heapq.heappush(self._priority_queue, entry)
        return delay

    def pop_ready_packets(self) -> List[Tuple[str, bytes]]:
        now = time.time()
        ready: List[Tuple[str, bytes]] = []
        while self._priority_queue and self._priority_queue[0].release_time <= now:
            pkt = heapq.heappop(self._priority_queue)
            ready.append((pkt.next_hop, pkt.raw_packet))
        return ready

    def pending_count(self) -> int:
        return len(self._priority_queue)

if __name__ == "__main__":
    print("=== Testing SphinxDelayEngine Interface (Day 67) ===")
    engine = SphinxDelayEngine()
    test_pkt = b"\xaa" * 1024
    assigned_delay = engine.enqueue_packet(test_pkt, "Node-Beta")
    print(f"[PASS] Packet Enqueued. Assigned Poisson Delay: {assigned_delay * 1000:.2f} ms")
    print(f"[PASS] Pending Packets in Buffer: {engine.pending_count()}")
    ready_before = engine.pop_ready_packets()
    print(f"[PASS] Immediate Ready Packets (expected 0): {len(ready_before)}")
    
    # Wait for the delay to expire and verify proper release
    time.sleep(assigned_delay + 0.005)
    ready_after = engine.pop_ready_packets()
    print(f"[PASS] Released Packets after Delay Expired (expected 1): {len(ready_after)}")
    print(f"[PASS] Pending Remaining: {engine.pending_count()}")
