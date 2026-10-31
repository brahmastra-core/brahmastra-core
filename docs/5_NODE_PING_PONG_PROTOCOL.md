# 5-Node Mesh Ping-Pong Protocol Specification (Day 49)

## 1. Overview
The Ping-Pong Protocol provides a cryptographically verified heartbeat and bi-directional message transmission mechanism across local simulated mesh nodes. It validates end-to-end forward secrecy over established ephemeral session keys.

## 2. Packet Wire Anatomy
Every transport datagram adheres to strict binary encapsulation:
- source_peer_id: 32-byte derived identifier of originating node.
- target_peer_id: 32-byte identifier of intended recipient node.
- nonce: Cryptographically random 12-byte initialization vector.
- ciphertext: Encrypted payload (PING / PONG payload with sequential counter).
- tag: 16-byte authentication tag ensuring integrity and authentic data origin.

## 3. State Machine & Flow
1. Node-A creates an authenticated ephemeral packet (type: PING, seq: N).
2. Node-A sends encrypted ciphertext via simulated loopback transport.
3. Node-B receives datagram, validates authentication tag using derived session key.
4. Node-B unpacks PING and responds immediately with an authenticated PONG packet (echo_seq: N).
5. Node-A verifies PONG and records round-trip latency.

## 4. Latency & Integrity Guardrails
- Round-trip ping-pong transit time must remain under 10ms.
- Forged payloads or modified ciphertexts must trigger immediate packet drops without crashing nodes.
