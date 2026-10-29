# Brahmastra Architecture - Phase 3 Roadmap
## Focus: Mixnet, Defense & Dharma Rules (Day 31 to Day 90)

Goal: Extend the FHE core cryptographic engine with mixnet protection, decentralized P2P communication, onion routing, and traffic obfuscation.

---

### Milestone Breakdown

#### 1. Docker & Virtual Networking Ecosystem (Day 31 - 36)
- **Day 31 - 33**: Docker CE & environment setup, base networking implementation, and commit.
- **Day 34 - 36**: Virtual mesh bridge configuration (`brahmastra-mesh-net`) and subnet isolation firewall rules.

#### 2. Multi-Node Topology & Peer Identity (Day 37 - 45)
- **Day 37 - 39**: Lightweight virtual node (Node-A) Dockerfile (< 100 MB, non-root security).
- **Day 40 - 42**: 5-Node topology Docker Compose setup (Node-A to Node-E isolation and resource limits).
- **Day 43 - 45**: Cryptographic peer identity generation (Ed25519 keys & SHA-256 peer IDs).

#### 3. Secure Handshake & P2P Discovery (Day 46 - 60)
- **Day 46 - 48**: Node-to-node mutual handshake protocol (Noise/mTLS, < 10ms latency).
- **Day 49 - 51**: 5-Node encrypted ping-pong message test with zero packet drop.
- **Day 52 - 54**: Decentralized discovery via Kademlia DHT routing tables.
- **Day 55 - 57**: Offline local mesh fallback architecture (Bluetooth / Wi-Fi Direct).
- **Day 58 - 60**: Resource profiling (< 80 MB RAM per node, < 15% CPU load).

#### 4. Onion Routing & Sphinx Mixnet Core (Day 61 - 75)
- **Day 61 - 63**: 3-Layer onion encryption routing chain.
- **Day 64 - 66**: Sphinx packet format implementation with fixed packet sizing.
- **Day 67 - 69**: Poisson delay distribution against traffic analysis attacks.
- **Day 70 - 72**: Decoy dummy packet generator for continuous background traffic.
- **Day 73 - 75**: Stratified mixnet topology (Input, Mixing, Output layers).

#### 5. Self-Healing, Obfuscation & Benchmarking (Day 76 - 90)
- **Day 76 - 78**: Full 5-node mesh end-to-end onion transmission test.
- **Day 79 - 81**: Constant-size packet verification (strict 4096 bytes).
- **Day 82 - 84**: Domain fronting and HTTPS traffic obfuscation (DPI bypass).
- **Day 85 - 87**: Fault-tolerance and dynamic self-healing rerouting upon node disconnect.
- **Day 88 - 90**: Bandwidth and latency benchmarking, tagging release `v0.2.5`.