# Kademlia Distributed Hash Table (DHT) Architecture (Day 52)

## 1. Overview & Theoretical Foundations
Brahmastra utilizes Kademlia DHT for serverless, decentralized peer discovery and key-based content routing. The network maps nodes into a 256-bit metric space derived directly from the SHA-256 cryptographic hashes of their Ed25519 public identities.

## 2. XOR Metric Distance
Distance between two nodes x and y is defined as their bitwise XOR sum interpreted as an integer:
$$d(x, y) = x \oplus y$$

Properties:
- d(x, x) = 0
- d(x, y) = d(y, x) (Symmetric)
- d(x, z) <= d(x, y) ^ d(y, z) (Triangle inequality)

## 3. K-Bucket Routing Table Specification
- Parameter $k = 20$: Maximum contacts maintained per bucket.
- 256 Buckets: Organized based on logarithmic prefix distance from the host node.
- Replacement & Eviction Policy: Least-recently seen peers are pinged before eviction; live peers take precedence to guarantee churn resistance.
