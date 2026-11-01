"""
Brahmastra Core: Sphinx Packet Poisson Delay Engine
Day 68: Core Implementation & Timing Obfuscation Benchmark
"""

import time
import math
import secrets
from dataclasses import dataclass, field
from typing import List, Tuple, Dict
import heapq

# Core Constants
DEFAULT_LAMBDA: float = 20.0       # Mean delay = 50ms
MIN_DELAY_FLOOR_SEC: float = 0.020  # 20ms Floor
MAX_DELAY_CAP_SEC: float = 0.200    # Strict 200ms Ceiling Clamp

@dataclass(order=True)
class DelayQueueItem:
    release_time: float
    arrival_time: float = field(compare=False)
    packet_id: int = field(compare=False)
    next_hop: str = field(compare=False)
    raw_packet: bytes = field(compare=False)

def compute_poisson_delay(rate_lambda: float = DEFAULT_LAMBDA,
                           min_floor: float = MIN_DELAY_FLOOR_SEC,
                           max_cap: float = MAX_DELAY_CAP_SEC) -> float:
    """
    Computes mathematically bounded Poisson inter-arrival delay.
    Strictly clamps output within [min_floor, max_cap].
    """
    rand_int = secrets.randbits(53)
    u = (rand_int + 1) / (2**53 + 1)
    raw_delay = -math.log(u) / rate_lambda
    # Task 2: Strict 200ms clamp enforcement
    return max(min_floor, min(raw_delay, max_cap))

class SphinxDelayCore:
    def __init__(self, rate_lambda: float = DEFAULT_LAMBDA, max_cap: float = MAX_DELAY_CAP_SEC):
        self.rate_lambda = rate_lambda
        self.max_cap = max_cap
        self._heap: List[DelayQueueItem] = []

    def enqueue(self, packet_id: int, raw_packet: bytes, next_hop: str) -> float:
        now = time.time()
        delay = compute_poisson_delay(self.rate_lambda, MIN_DELAY_FLOOR_SEC, self.max_cap)
        target_release = now + delay
        item = DelayQueueItem(
            release_time=target_release,
            arrival_time=now,
            packet_id=packet_id,
            next_hop=next_hop,
            raw_packet=raw_packet
        )
        heapq.heappush(self._heap, item)
        return delay

    def drain_ready(self, current_time: float) -> List[DelayQueueItem]:
        ready: List[DelayQueueItem] = []
        while self._heap and self._heap[0].release_time <= current_time:
            ready.append(heapq.heappop(self._heap))
        return ready

    def pending_count(self) -> int:
        return len(self._heap)

def verify_timing_obfuscation():
    """
    Task 1 & Task 2 Verification:
    Tests packet reordering (shuffling) due to independent Poisson delays.
    Validates that FIFO arrival order is broken to defeat timing correlation attacks.
    """
    engine = SphinxDelayCore(rate_lambda=DEFAULT_LAMBDA, max_cap=MAX_DELAY_CAP_SEC)
    total_packets = 25
    assigned_delays: List[float] = []

    print("=== Day 68: Ingesting 25 Sequential Packets ===")
    start_time = time.time()
    for i in range(total_packets):
        dummy_pkt = i.to_bytes(4, "big").ljust(1024, b"\x00")
        d = engine.enqueue(packet_id=i, raw_packet=dummy_pkt, next_hop=f"Node-Next-{i%3}")
        assigned_delays.append(d)

    # Verify Max Ceiling (Task 2)
    max_observed = max(assigned_delays)
    min_observed = min(assigned_delays)
    print(f"[PASS] Task 2: Max Delay Observed: {max_observed*1000:.2f} ms (Strict Limit <= 200.00 ms)")
    print(f"[PASS] Task 2: Min Delay Observed: {min_observed*1000:.2f} ms (Floor >= 20.00 ms)")
    assert max_observed <= MAX_DELAY_CAP_SEC, "Error: Delay exceeds 200ms ceiling!"

    # Simulate event loop drainage
    departure_order: List[int] = []
    sim_time = start_time
    step = 0.005  # 5ms time steps
    while engine.pending_count() > 0 or sim_time < start_time + MAX_DELAY_CAP_SEC + 0.05:
        sim_time += step
        ready = engine.drain_ready(sim_time)
        for r in ready:
            departure_order.append(r.packet_id)
        if len(departure_order) == total_packets:
            break

    print(f"[PASS] All {len(departure_order)} Packets Dispatched Successfully.")
    arrival_order = list(range(total_packets))
    is_shuffled = departure_order != arrival_order
    print(f"[PASS] Task 1: Arrival Order   : {arrival_order[:10]} ...")
    print(f"[PASS] Task 1: Departure Order : {departure_order[:10]} ...")
    print(f"[PASS] Timing Analysis Obfuscation (FIFO Broken): {is_shuffled}")
    assert is_shuffled, "Warning: Packets departed in identical FIFO order!"
    print("=== Day 68 Core Implementation: COMPLETE & VERIFIED ===")

if __name__ == "__main__":
    verify_timing_obfuscation()
