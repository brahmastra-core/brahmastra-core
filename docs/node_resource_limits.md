# Mesh Node Resource Specification & Architecture

## System Constraints (Day 58 Specification)
- Target Hardware: Lenovo ThinkPad T490 (Linux / WSL2)
- Total Active Nodes: 5 Local Mesh Relays
- Hard Memory Limit per Node: 80 MB (Enforced via cgroups)
- Target Idle Footprint: 8 MB - 15 MB
- Maximum Burst Allocation: 80 MB (Under heavy lattice payload routing)
- CPU Quota: 0.20 CPU shares per container (< 20% total utilization)

## Stability Verification
- OOM (Out Of Memory) Defense: Enforced dynamic buffer throttling.
- Packet Drop Strategy: Constant-size 4 KB padding queued up to 30 MB max buffer.
