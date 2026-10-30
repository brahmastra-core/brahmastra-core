# Brahmastra Mesh Network - Day 40 Architecture
## 5-Node Cluster Topology Specification

### 1. Topology Overview
The Brahmastra decentralized mesh network deploys a 5-node virtual cluster (Node-A through Node-E) executing in an isolated bridge network (`brahmastra-mesh-net`).

### 2. Node Allocation & Network Matrix
| Node Name | Static IP | External Port | Internal Port | Memory Limit | Execution Mode |
|---|---|---|---|---|---|
| Node-A | 172.28.0.10 | 8443 | 443 | 512 MB | UID: 10001 (Non-Root) |
| Node-B | 172.28.0.11 | 8444 | 443 | 512 MB | UID: 10001 (Non-Root) |
| Node-C | 172.28.0.12 | 8445 | 443 | 512 MB | UID: 10001 (Non-Root) |
| Node-D | 172.28.0.13 | 8446 | 443 | 512 MB | UID: 10001 (Non-Root) |
| Node-E | 172.28.0.14 | 8447 | 443 | 512 MB | UID: 10001 (Non-Root) |

### 3. Security Hardening Controls
- **Resource Boundary:** Linux `cgroups` enforce a strict 512 MB RAM ceiling per container to mitigate DoS amplification.
- **Privilege Separation:** Non-root execution enforced at UID 10001 with zero-trust entrypoint validation.
- **Port Masking:** Traffic encapsulated and mapped via HTTPS-standard ports to bypass deep packet inspection.