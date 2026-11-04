"""
Brahmastra Mesh Network - Day 55 Offline Local Mesh & Fallback Router
Implements broadcast beaconing, transport medium abstraction, and local peer caching.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time
import json
import secrets

class TransportMedium(Enum):
 UDP_BROADCAST = "udp_broadcast"
 BLE = "ble"
 WIFI_DIRECT = "wifi_direct"

@dataclass
class LocalPeerEndpoint:
 """Represents an active local mesh peer discovered via offline hardware radios."""
 node_id: bytes
 transport: TransportMedium
 address: str
 port: int
 last_beacon: float = field(default_factory=time.time)

class OfflineMeshRouter:
 """Handles local network peer discovery and fallback routing when WAN is offline."""

 def __init__(self, local_node_id: bytes, bind_port: int = 9555) -> None:
 if len(local_node_id) != 32:
 raise ValueError("Local node ID must be exactly 32 bytes")
 self.local_node_id = local_node_id
 self.bind_port = bind_port
 self.local_peers: Dict[bytes, LocalPeerEndpoint] = {}

 def craft_discovery_beacon(self) -> bytes:
 """Constructs a discovery beacon payload to broadcast across local radio mediums."""
 beacon_data = {
 "protocol": "BRAHMASTRA_OFFLINE_MESH_V1",
 "node_id": self.local_node_id.hex(),
 "port": self.bind_port,
 "timestamp": time.time()
 }
 return json.dumps(beacon_data).encode("utf-8")

 def handle_incoming_beacon(self, payload: bytes, source_addr: str, transport: TransportMedium = TransportMedium.UDP_BROADCAST) -> bool:
 """Parses and registers an incoming peer discovery beacon."""
 try:
 data = json.loads(payload.decode("utf-8"))
 if data.get("protocol") != "BRAHMASTRA_OFFLINE_MESH_V1":
 return False

 peer_id = bytes.fromhex(data["node_id"])
 if peer_id == self.local_node_id:
 # Do not register self as a local peer
 return False

 peer_port = int(data.get("port", self.bind_port))
 endpoint = LocalPeerEndpoint(
 node_id=peer_id,
 transport=transport,
 address=source_addr,
 port=peer_port,
 last_beacon=time.time()
 )
 self.local_peers[peer_id] = endpoint
 return True
 except (json.JSONDecodeError, KeyError, ValueError):
 return False

 def route_local_packet(self, target_id: bytes, payload: bytes) -> Optional[LocalPeerEndpoint]:
 """Resolves target peer in local cache for offline direct forwarding."""
 return self.local_peers.get(target_id)

if __name__ == "__main__":
 local_id = secrets.token_bytes(32)
 router = OfflineMeshRouter(local_id, bind_port=9555)
 print(f"[OFFLINE] Mesh Router active for Node: {local_id.hex()[:16]}...")

 # Craft local beacon
 beacon = router.craft_discovery_beacon()
 print(f"[OFFLINE] Generated Discovery Beacon: {beacon.decode('utf-8')}")

 # Simulate discovery of 2 nearby offline peers over Wi-Fi Direct and BLE
 peer1_id = secrets.token_bytes(32)
 peer2_id = secrets.token_bytes(32)

 router.handle_incoming_beacon(
 json.dumps({"protocol": "BRAHMASTRA_OFFLINE_MESH_V1", "node_id": peer1_id.hex(), "port": 9556}).encode("utf-8"),
 "192.168.49.2",
 TransportMedium.WIFI_DIRECT
 )
 router.handle_incoming_beacon(
 json.dumps({"protocol": "BRAHMASTRA_OFFLINE_MESH_V1", "node_id": peer2_id.hex(), "port": 9557}).encode("utf-8"),
 "AA:BB:CC:DD:EE:01",
 TransportMedium.BLE
 )

 print(f"[STATUS] Discovered Offline Peers: {len(router.local_peers)}")
 for pid, ep in router.local_peers.items():
 print(f" -> Peer: {pid.hex()[:16]}... | Medium: {ep.transport.value} | Endpoint: {ep.address}:{ep.port}")

 # Test offline packet dispatch
 resolved = router.route_local_packet(peer1_id, b"ENCRYPTED_CHA_CHA_PAYLOAD")
 if resolved:
 print(f"[ROUTED] Packet dispatched directly via {resolved.transport.value} to: {resolved.address}:{resolved.port}")
