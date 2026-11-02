# Node Disconnect & Self-Healing Routing Architecture (Brahmastra Core)

## 1. Overview
In a decentralized mixnet, relay nodes may experience unexpected shutdowns, churn, or network partitions. The self-healing subsystem detects dropped intermediaries and dynamically reconstructs healthy circuit paths without compromising anonymity.

## 2. Failure Detection Mechanics
- **Heartbeat / Probe Latency:** If an intermediary node fails to acknowledge packet transit within the defined threshold (e.g., 200ms), it is marked as `UNREACHABLE`.
- **Fault Isolation:** The preceding node flags the circuit break and requests dynamic path reconfiguration.

## 3. Dynamic Re-Routing (Self-Healing)
- **Circuit Rebuilding:** The ingress node replaces the faulty hop with an active standby node from the peer routing table.
- **Payload Preservation:** In-flight frames are preserved in transient buffer queues and dispatched across the alternate route with zero data loss.
