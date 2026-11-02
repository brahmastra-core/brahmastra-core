# Stratified Topology Architecture (Brahmastra Core)

## 1. Overview
In an unrestricted mesh network, arbitrary multi-hop routing causes loops, uneven traffic distribution, and vulnerabilities to multi-node collusion attacks. Brahmastra employs a Stratified Topology where nodes are partitioned into discrete sequential strata (layers).

## 2. Layer Taxonomy & Invariants
- **Layer 1 (Ingress / Entry Strata):** Ingests client traffic, performs initial blind authentication and rate calibration. Strictly forwards to Layer 2.
- **Layer 2 (Mix Strata):** Executes cryptographic Sphinx onion unwrapping, Poisson delay scheduling, and decoy packet mixing. Strictly forwards to Layer 3.
- **Layer 3 (Egress / Exit Strata):** Terminal layer that forwards genuine payloads to the ultimate recipient or silently drops expired decoy traffic.

## 3. Strict Routing Forward Invariant
Path transition enforces the mathematical order:
$$L_1 \longrightarrow L_2 \longrightarrow L_3$$
Backward routing ($L_{i} \to L_{j}$ where $j \le i$) or intra-layer hopping ($L_i \to L_i$) is mathematically rejected by the topology routing table.
