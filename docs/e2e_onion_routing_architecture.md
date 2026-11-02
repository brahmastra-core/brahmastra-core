# End-to-End 3-Hop Onion Routing Architecture (Brahmastra Core)

## 1. Overview
This module demonstrates an end-to-end 3-hop onion encrypted circuit across the Brahmastra stratified mesh network (Node-A -> Node-B -> Node-D -> Node-E).

## 2. Cryptographic Peeling Mechanics
- **Client (Node-A):** Encapsulates the plaintext payload into 3 layers of symmetric/asymmetric encryption in reverse topological order ($PK_E \to PK_D \to PK_B$).
- **Hop 1 - Ingress (Node-B):** Peels Layer 1 using its private key, unmasks the routing directive for Node-D, and forwards Layer 2 blob.
- **Hop 2 - Mix (Node-D):** Peels Layer 2, applies Poisson delay scheduling, and forwards Layer 3 blob to Node-E.
- **Hop 3 - Egress (Node-E):** Peels Layer 3, recovers the genuine plaintext, and delivers to destination or drops decoy packets.

## 3. Threat Mitigation
- **Non-collusion Invariant:** Intermediate node Node-D knows only preceding hop (Node-B) and next hop (Node-E), maintaining zero awareness of origin Node-A.
- **Payload Invariance:** Constant packet size maintained through padding at each decryption layer.
