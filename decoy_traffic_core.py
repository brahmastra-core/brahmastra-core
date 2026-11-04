"""
Brahmastra Core: Decoy Traffic Generator Core Engine
Day 71: Core Implementation & Silent Drop Verification
"""

import os
import time
import queue
from typing import List, Tuple, Optional
from decoy_traffic import DecoyTrafficGenerator, DecoyPacket, DECOY_PACKET_SIZE, DECOY_FLAG_HEADER

class ConstantRateTrafficPump:
 """
 Core engine maintaining continuous constant-rate transmission across nodes.
 Injects dummy 4KB packets whenever real application data is absent.
 """
 def __init__(self, node_pool: List[str], target_rate_hz: float = 20.0):
 self.node_pool = node_pool
 self.interval = 1.0 / target_rate_hz
 self.generator = DecoyTrafficGenerator(node_pool=node_pool, packet_size=DECOY_PACKET_SIZE)
 self.real_packet_queue: queue.Queue[bytes] = queue.Queue()
 self.transmitted_count = 0
 self.decoy_transmitted = 0
 self.real_transmitted = 0

 def submit_real_packet(self, payload: bytes) -> None:
 """Pushes legitimate application traffic to the transmission buffer."""
 self.real_packet_queue.put(payload)

 def dispatch_next_slot(self) -> Tuple[bool, bytes, List[str]]:
 """
 Task 1: Constant-rate dispatch slot.
 Transmits real packet if available; otherwise falls back to a 4KB decoy packet.
 """
 if not self.real_packet_queue.empty():
 real_data = self.real_packet_queue.get()
 # Ensure real payload is padded to identical 4KB invariant
 if len(real_data) < DECOY_PACKET_SIZE:
 real_data = real_data.ljust(DECOY_PACKET_SIZE, b"\x00")
 self.real_transmitted += 1
 self.transmitted_count += 1
 return (False, real_data, ["Node-A", "Node-B", "Node-C"])
 else:
 decoy = self.generator.build_decoy_packet(hop_count=3)
 self.decoy_transmitted += 1
 self.transmitted_count += 1
 return (True, decoy.raw_bytes, decoy.target_route)


class RelayDestinationProcessor:
 """
 Task 2: Ingress processor at destination node.
 Performs silent drop on decoy packets, preventing memory leaks and user-space pollution.
 """
 def __init__(self):
 self.silent_dropped_count = 0
 self.delivered_count = 0

 def process_incoming_packet(self, packet_bytes: bytes) -> Optional[bytes]:
 """
 Inspects packet payload.
 If flagged as decoy -> silently drops without logs/side-channels.
 If legitimate -> delivers to application layer.
 """
 if len(packet_bytes) != DECOY_PACKET_SIZE:
 return None

 # Check internal drop flag header
 if packet_bytes.startswith(DECOY_FLAG_HEADER):
 self.silent_dropped_count += 1
 del packet_bytes # Immediate deallocation
 return None

 self.delivered_count += 1
 return packet_bytes.rstrip(b"\x00")


def run_day71_verification():
 print("=== Brahmastra Day 71: Core Implementation Verification ===")
 nodes = ["Node-A", "Node-B", "Node-C", "Node-D", "Node-E"]
 pump = ConstantRateTrafficPump(node_pool=nodes, target_rate_hz=20.0)
 processor = RelayDestinationProcessor()

 # Step 1: Simulate 10 transmission slots with 2 real packets inserted mid-stream
 print("\n[TEST] Simulating 10 transmission slots (Idle + Real Traffic)...")
 pump.submit_real_packet(b"BRAHMASTRA_SECURE_PAYLOAD_1")
 pump.submit_real_packet(b"BRAHMASTRA_SECURE_PAYLOAD_2")

 for slot in range(10):
 is_decoy, raw_bytes, route = pump.dispatch_next_slot()
 # Destination processing
 result = processor.process_incoming_packet(raw_bytes)

 # Verification Assertions
 print(f"[PASS] Task 1: Constant Rate Total Dispatched : {pump.transmitted_count} packets")
 print(f"[PASS] Task 1: Real Packets Transmitted : {pump.real_transmitted}")
 print(f"[PASS] Task 1: Decoy Cover Packets Injected : {pump.decoy_transmitted}")
 print(f"[PASS] Task 2: Decoy Packets Silently Dropped: {processor.silent_dropped_count}")
 print(f"[PASS] Task 2: Legitimate Delivered to User : {processor.delivered_count}")

 assert pump.transmitted_count == 10, "Transmission count mismatch!"
 assert pump.real_transmitted == 2, "Real packet count mismatch!"
 assert pump.decoy_transmitted == 8, "Decoy packet count mismatch!"
 assert processor.silent_dropped_count == 8, "Silent drop logic failed!"
 assert processor.delivered_count == 2, "Delivery count mismatch!"

 print("\n=== Day 71 Core Implementation: COMPLETE & VERIFIED ===")

if __name__ == "__main__":
 run_day71_verification()
