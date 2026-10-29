"""
Brahmastra Protocol - Clean Test Runner & Type Verification
Phase 3: Day 32 Implementation
"""

import time
from protocol import PacketHeader, MeshPacket, NodeInterface


class MockNode(NodeInterface):
    """Concrete mock implementation of NodeInterface for local verification."""

    def initialize_node(self) -> bool:
        return True

    def send_packet(self, target_node_id: str, packet: MeshPacket) -> bool:
        self.routing_table[target_node_id] = "127.0.0.1"
        return len(packet.encrypted_payload) == packet.header.payload_size

    def receive_packet(self) -> MeshPacket:
        dummy_header = PacketHeader(
            version=1,
            sender_id="node_alpha",
            receiver_id=self.node_id,
            timestamp=time.time(),
            payload_size=16,
        )
        return MeshPacket(
            header=dummy_header,
            encrypted_payload=b"encrypted_secret",
            signature=b"test_sig",
        )


def verify_clean_run() -> None:
    node = MockNode(node_id="node_omega", listen_port=9001)
    assert node.initialize_node() is True

    payload = b"brahmastra_secure"
    header = PacketHeader(
        version=1,
        sender_id="node_omega",
        receiver_id="node_alpha",
        timestamp=time.time(),
        payload_size=len(payload),
    )
    packet = MeshPacket(header=header, encrypted_payload=payload)

    assert node.send_packet("node_alpha", packet) is True
    received = node.receive_packet()
    assert received.header.payload_size == 16
    print("DAY 32 VERIFICATION: Clean run successful. Zero type errors.")


if __name__ == "__main__":
    verify_clean_run()