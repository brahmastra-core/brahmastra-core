"""
Day 65: Sphinx Packet Core Implementation & Replay Attack Defense
Enforces strict 1024-byte packet format and single-use packet tag verification.
"""
import hashlib
from typing import Tuple, Set

TOTAL_SPHINX_SIZE = 1024
ALPHA_SIZE = 32
BETA_SIZE = 160
GAMMA_SIZE = 16
DELTA_SIZE = 816

class SphinxReplayCache:
 """In-memory replay attack defense cache tracking observed packet tags."""
 def __init__(self):
 self._seen_tags: Set[bytes] = set()

 def check_and_record(self, tag: bytes) -> bool:
 """
 Returns True if packet is unique and recorded.
 Returns False if packet has already been seen (Replay Attack).
 """
 if tag in self._seen_tags:
 return False
 self._seen_tags.add(tag)
 return True

def build_sphinx_wire_packet(alpha: bytes, beta: bytes, gamma: bytes, delta: bytes) -> bytes:
 """Builds a continuous 1024-byte Sphinx wire packet."""
 if len(alpha) != ALPHA_SIZE or len(beta) != BETA_SIZE or len(gamma) != GAMMA_SIZE or len(delta) != DELTA_SIZE:
 raise ValueError("Invalid component size for Sphinx packet.")
 return alpha + beta + gamma + delta

def process_sphinx_packet_with_replay_guard(
 raw_packet: bytes, 
 replay_cache: SphinxReplayCache
) -> Tuple[str, bytes]:
 """
 Validates packet structure, checks against replay attacks,
 and returns next hop and transformed constant-size packet.
 """
 if len(raw_packet) != TOTAL_SPHINX_SIZE:
 raise ValueError(f"Packet must be exactly {TOTAL_SPHINX_SIZE} bytes.")

 alpha = raw_packet[:ALPHA_SIZE]
 beta = raw_packet[ALPHA_SIZE:ALPHA_SIZE + BETA_SIZE]
 gamma = raw_packet[ALPHA_SIZE + BETA_SIZE:ALPHA_SIZE + BETA_SIZE + GAMMA_SIZE]
 delta = raw_packet[ALPHA_SIZE + BETA_SIZE + GAMMA_SIZE:]

 # Packet tag derived from Alpha and Gamma for unique identification
 packet_tag = hashlib.sha256(alpha + gamma).digest()[:16]

 # Replay Protection Check
 if not replay_cache.check_and_record(packet_tag):
 raise ValueError("SecurityError: Replay attack detected. Packet rejected!")

 # Unpack next hop and shift beta with deterministic padding
 next_hop = "Node-Relay-Next"
 peeled_beta = beta[32:] + b"\x00" * 32
 new_alpha = hashlib.sha256(alpha).digest()[:ALPHA_SIZE]

 transformed_packet = build_sphinx_wire_packet(new_alpha, peeled_beta, gamma, delta)
 return next_hop, transformed_packet

if __name__ == "__main__":
 cache = SphinxReplayCache()
 mock_alpha = b"\x01" * ALPHA_SIZE
 mock_beta = b"\x02" * BETA_SIZE
 mock_gamma = b"\x03" * GAMMA_SIZE
 mock_delta = b"\x04" * DELTA_SIZE

 pkt = build_sphinx_wire_packet(mock_alpha, mock_beta, mock_gamma, mock_delta)
 print(f"[Sphinx Core] Initial Packet Size: {len(pkt)} Bytes")

 # First presentation: Success
 next_hop, out_pkt = process_sphinx_packet_with_replay_guard(pkt, cache)
 print(f"[First Processing] Success -> Forwarding to: {next_hop} | Out Size: {len(out_pkt)} Bytes")

 # Second presentation (Replay attempt): Must raise error
 try:
 process_sphinx_packet_with_replay_guard(pkt, cache)
 print("[FAIL] Replay attack succeeded without detection.")
 except ValueError as e:
 print(f"[PASS] Replay Guard Verification: {e}")
