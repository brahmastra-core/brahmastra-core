# Offline Local Mesh Architecture & Hardware Radio Fallback (Day 55)

## 1. Zero-Internet Radio Architecture
Brahmastra activates autonomous local mesh discovery when WAN/Internet access is severed. Communication leverages existing physical device radios without requiring external cell towers or central DNS.

## 2. Radio Transports & Dual Layer
- Primary Fast Transport: Wi-Fi Direct (P2P) & Local UDP Subnet Broadcast (`255.255.255.255`). High throughput for payload routing.
- Secondary Low-Power Transport: Bluetooth Low Energy (BLE) advertisements for proximity beaconing.
- Relay Topology: Multi-hop Store-and-Forward routing using ChaCha20-Poly1305 encrypted packets.

## 3. Fallback Discovery Protocol
- Beacon Structure: Periodic local broadcast emitting Ed25519 identity hashes and local listening ports.
- Dynamic Peering: Automatic peer registration and ping refresh upon receiving valid beacon acknowledgments.
