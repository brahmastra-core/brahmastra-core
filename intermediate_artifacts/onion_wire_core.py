"""
Day 62: Core Onion Routing Binary Wire Format & Hop Isolation Chain
"""
import struct
import hashlib
from typing import Tuple, Optional

# Protocol Header Format:
# - Version (1 Byte, unsigned char: 'B')
# - Layer Depth (1 Byte, unsigned char: 'B')
# - Payload Length (2 Bytes, unsigned short: 'H')
HEADER_FORMAT = "!BBH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
PROTOCOL_VERSION = 1

def serialize_onion_packet(layer_depth: int, payload: bytes) -> bytes:
    """Serializes layer metadata and payload into binary wire format."""
    length = len(payload)
    header = struct.pack(HEADER_FORMAT, PROTOCOL_VERSION, layer_depth, length)
    return header + payload

def deserialize_onion_packet(wire_bytes: bytes) -> Tuple[int, int, bytes]:
    """Deserializes binary wire format into (version, depth, payload)."""
    if len(wire_bytes) < HEADER_SIZE:
        raise ValueError("Packet smaller than wire protocol header size.")
    version, layer_depth, length = struct.unpack_from(HEADER_FORMAT, wire_bytes, 0)
    payload = wire_bytes[HEADER_SIZE:HEADER_SIZE + length]
    return version, layer_depth, payload

def simulate_cryptographic_chain():
    """
    Demonstrates hop isolation where Exit Node (Node 3) has zero knowledge 
    of the Origin Node (Node 0).
    """
    secret_message = b"Brahmastra_Cloak_Core_Payload_2026"
    
    # Reverse layered encapsulation
    # Layer 3 for Exit Node
    l3_inner = b"NEXT:FINAL_DEST|DATA:" + secret_message
    l3_wire = serialize_onion_packet(1, l3_inner)
    
    # Layer 2 for Relay Node
    l2_inner = b"NEXT:Node-3|DATA:" + l3_wire
    l2_wire = serialize_onion_packet(2, l2_inner)
    
    # Layer 1 for Entry Node
    l1_inner = b"NEXT:Node-2|DATA:" + l2_wire
    l1_wire = serialize_onion_packet(3, l1_inner)
    
    print(f"[Wire Format] Layer 1 Binary Wire Size: {len(l1_wire)} bytes")

    # Processing Hop 1 (Entry Node)
    _, depth1, hop1_data = deserialize_onion_packet(l1_wire)
    next_hop_1, remaining_1 = hop1_data.split(b"|DATA:", 1)
    print(f"[Hop 1 Entry] Forwarding to: {next_hop_1.decode()} | Received from: Origin")

    # Processing Hop 2 (Relay Node)
    _, depth2, hop2_data = deserialize_onion_packet(remaining_1)
    next_hop_2, remaining_2 = hop2_data.split(b"|DATA:", 1)
    print(f"[Hop 2 Relay] Forwarding to: {next_hop_2.decode()} | Received from: Node-1 (Origin hidden)")

    # Processing Hop 3 (Exit Node)
    _, depth3, hop3_data = deserialize_onion_packet(remaining_2)
    next_hop_3, final_payload = hop3_data.split(b"|DATA:", 1)
    print(f"[Hop 3 Exit] Target: {next_hop_3.decode()} | Origin Source: STRICTLY_ANONYMOUS")
    print(f"[Payload Recovered] Payload: {final_payload.decode()}")

if __name__ == "__main__":
    simulate_cryptographic_chain()
