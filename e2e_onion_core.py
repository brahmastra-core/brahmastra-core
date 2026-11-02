"""
Brahmastra Core: Day 77 - End-to-End Onion Routing Core Implementation
Verifies:
  1. Full Plaintext Reconstruction at Exit Node (Node-E)
  2. Zero Plaintext Leakage at Intermediate Relays (Node-B & Node-D)
"""

import hashlib
from typing import Dict, List, Tuple
from onion_mesh_tester import EndToEndOnionPipeline, OnionPacket

class AuditedOnionPipeline(EndToEndOnionPipeline):
    def __init__(self):
        super().__init__()
        # Internal log buffers to simulate memory captures of relays
        self.node_memory_logs: Dict[str, List[bytes]] = {
            "Node-B": [],
            "Node-D": [],
            "Node-E": []
        }

    def execute_and_audit_circuit(self, packet: OnionPacket, target_secret: bytes) -> Tuple[bytes, bool]:
        """
        Executes traversal while auditing memory/packet snapshots at intermediate relays.
        """
        print(f"\n--- Initiating Circuit Relay ---")
        
        # 1. Hop 1: Node-B (Ingress)
        self.node_memory_logs["Node-B"].append(packet.layer_data)
        next_hop1, payload1 = self.nodes[packet.next_hop].peel_layer(packet.layer_data)
        self.node_memory_logs["Node-B"].append(payload1)
        print(f"[HOP 1 - Node-B] Ingress processing complete. Forwarding to -> {next_hop1}")

        # 2. Hop 2: Node-D (Mix Relay)
        self.node_memory_logs["Node-D"].append(payload1)
        next_hop2, payload2 = self.nodes[next_hop1].peel_layer(payload1)
        self.node_memory_logs["Node-D"].append(payload2)
        print(f"[HOP 2 - Node-D] Mix processing & Poisson delay applied. Forwarding to -> {next_hop2}")

        # 3. Hop 3: Node-E (Egress Destination)
        self.node_memory_logs["Node-E"].append(payload2)
        status, recovered_plaintext = self.nodes[next_hop2].peel_layer(payload2)
        print(f"[HOP 3 - Node-E] Egress terminal layer unsealed. Status -> {status}")

        # Task 2: Audit Intermediate Relays for Plaintext Leakage
        leakage_detected = False
        for relay_id in ["Node-B", "Node-D"]:
            for snapshot in self.node_memory_logs[relay_id]:
                if target_secret in snapshot:
                    print(f"[CRITICAL ALERT] Plaintext leaked inside {relay_id} memory buffer!")
                    leakage_detected = True

        return recovered_plaintext, leakage_detected

def run_day77_implementation():
    print("=== Brahmastra Day 77: Core Onion Routing Verification ===")
    
    pipeline = AuditedOnionPipeline()
    secret_payload = b"BRAHMASTRA_SACRED_ZERO_SURVEILLANCE_PAYLOAD_2026"
    print(f"[ORIGIN: Node-A] Plaintext Secret: {secret_payload.decode()}")

    # Construct nested onion
    onion_packet = pipeline.create_onion_message(secret_payload)
    
    # Execute circuit and audit
    recovered_data, leak_status = pipeline.execute_and_audit_circuit(onion_packet, secret_payload)

    print("\n--- Verification Checks ---")
    
    # Task 1: Check Data Integrity at Node-E
    hash_orig = hashlib.sha256(secret_payload).hexdigest()
    hash_recv = hashlib.sha256(recovered_data).hexdigest()
    print(f"[HASH ORIGIN] : {hash_orig}")
    print(f"[HASH RECV]   : {hash_recv}")
    
    assert recovered_data == secret_payload, "Task 1 Failed: Data corruption detected!"
    print(f"[PASS] Task 1: Exact Plaintext Integrity Verified at Node-E")

    # Task 2: Confirm Zero Leakage at Node-B and Node-D
    assert not leak_status, "Task 2 Failed: Plaintext was exposed to intermediate nodes!"
    print(f"[PASS] Task 2: Zero Plaintext Leakage Confirmed across Intermediate Nodes")

    print("\n=== Day 77 Core Implementation: COMPLETE & VERIFIED ===")

if __name__ == "__main__":
    run_day77_implementation()
