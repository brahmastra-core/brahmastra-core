"""
Brahmastra Mesh Network - Day 52 Kademlia Routing Table & Discovery Engine
Implements 256-bit XOR metric distance, K-bucket peer management, and closest-node lookup.
"""

from dataclasses import dataclass
from typing import List, Optional
import time

K_BUCKET_SIZE = 20
ID_BIT_LENGTH = 256

@dataclass
class Contact:
    """Represents a discovered peer endpoint in the Kademlia DHT topology."""
    node_id: bytes
    ip: str
    port: int
    last_seen: float = 0.0

    def __post_init__(self) -> None:
        if self.last_seen == 0.0:
            self.last_seen = time.time()

class KBucket:
    """Maintains a bounded list of up to k contacts sharing a prefix distance."""

    def __init__(self, k_size: int = K_BUCKET_SIZE) -> None:
        self.k_size = k_size
        self.contacts: List[Contact] = []

    def add(self, contact: Contact) -> bool:
        """Add contact or refresh existing contact position."""
        for idx, existing in enumerate(self.contacts):
            if existing.node_id == contact.node_id:
                # Refresh contact to tail (most recently active)
                self.contacts.pop(idx)
                contact.last_seen = time.time()
                self.contacts.append(contact)
                return True

        if len(self.contacts) < self.k_size:
            self.contacts.append(contact)
            return True

        # Bucket is full; caller must evaluate eviction policy
        return False

    def remove(self, node_id: bytes) -> None:
        self.contacts = [c for c in self.contacts if c.node_id != node_id]

class RoutingTable:
    """Manages 256 K-Buckets partitioned by bitwise XOR distance from local node."""

    def __init__(self, local_node_id: bytes) -> None:
        if len(local_node_id) != 32:
            raise ValueError("Local node ID must be exactly 32 bytes (256 bits)")
        self.local_node_id = local_node_id
        self.buckets: List[KBucket] = [KBucket() for _ in range(ID_BIT_LENGTH)]

    @staticmethod
    def distance(id1: bytes, id2: bytes) -> int:
        """Calculate bitwise XOR distance between two 32-byte node identifiers."""
        int1 = int.from_bytes(id1, byteorder="big")
        int2 = int.from_bytes(id2, byteorder="big")
        return int1 ^ int2

    def _get_bucket_index(self, node_id: bytes) -> int:
        """Compute the bucket index based on leading zero bits in XOR distance."""
        dist = self.distance(self.local_node_id, node_id)
        if dist == 0:
            return 0
        # Determine bit length to assign appropriate bucket bucket (0-255)
        return min(dist.bit_length() - 1, ID_BIT_LENGTH - 1)

    def add_contact(self, contact: Contact) -> bool:
        """Insert or update a contact inside the corresponding K-bucket."""
        if contact.node_id == self.local_node_id:
            return False
        b_idx = self._get_bucket_index(contact.node_id)
        return self.buckets[b_idx].add(contact)

    def find_closest_nodes(self, target_id: bytes, count: int = 5) -> List[Contact]:
        """Return the closest contacts to a target ID sorted by XOR distance."""
        all_contacts: List[Contact] = []
        for bucket in self.buckets:
            all_contacts.extend(bucket.contacts)

        # Sort all known contacts by XOR distance relative to target_id
        all_contacts.sort(key=lambda c: self.distance(c.node_id, target_id))
        return all_contacts[:count]

if __name__ == "__main__":
    import secrets

    local_id = secrets.token_bytes(32)
    rt = RoutingTable(local_id)
    print(f"[DHT] Routing Table initialized for Local Node ID: {local_id.hex()[:16]}...")

    # Insert 10 synthetic peer nodes
    for i in range(10):
        peer_id = secrets.token_bytes(32)
        contact = Contact(node_id=peer_id, ip="127.0.0.1", port=9000 + i)
        rt.add_contact(contact)

    # Lookup closest nodes to a random query target
    target = secrets.token_bytes(32)
    closest = rt.find_closest_nodes(target, count=3)

    print(f"[DHT] Closest 3 peers to target {target.hex()[:16]}...:")
    for idx, c in enumerate(closest, 1):
        dist = rt.distance(c.node_id, target)
        print(f"  {idx}. Node ID: {c.node_id.hex()[:16]}... | Port: {c.port} | XOR Distance: {dist}")
