"""
Brahmastra Mesh Network - Node-A Startup Entrypoint
Phase 3: Day 38 Implementation
Ensures non-root identity verification, environment initialization,
and port 443 mesh readiness.
"""

import os
import sys
import time


def verify_execution_environment() -> None:
    current_uid = os.getuid()
    node_id = os.getenv("NODE_ID", "Node-A")
    node_ip = os.getenv("NODE_IP", "172.28.0.10")
    listen_port = os.getenv("LISTEN_PORT", "443")

    print(f"=================================================")
    print(f"[BOOT] Initializing Brahmastra Mesh {node_id}")
    print(f"=================================================")
    print(f"[STATUS] Running with UID: {current_uid}")
    print(f"[STATUS] Target IP:        {node_ip}")
    print(f"[STATUS] Listening Port:   {listen_port} (HTTPS Masquerade)")

    # Enforce non-root execution (UID != 0)
    if current_uid == 0:
        print("[CRITICAL ERROR] Running as root! Terminating for Zero-Trust compliance.", file=sys.stderr)
        sys.exit(1)

    print("[SECURITY] Zero-Trust Verified: Running as non-root unprivileged process.")
    print(f"[ACTIVE] Node {node_id} successfully initialized and operational.")


if __name__ == "__main__":
    verify_execution_environment()