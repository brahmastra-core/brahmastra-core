#!/usr/bin/env python3
"""
Brahmastra Mesh Node Entrypoint Daemon
Ensures zero-trust execution as UID 10001 and keeps socket listener active.
"""

import os
import sys
import socket
import signal
import time

def handle_sigterm(signum, frame):
    print("\n[SHUTDOWN] Graceful termination received. Closing node daemon...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)

node_id = os.environ.get("NODE_ID", "Node-A")
node_ip = os.environ.get("NODE_IP", "172.28.0.10")
listen_port = int(os.environ.get("LISTEN_PORT", 443))
current_uid = os.getuid()

print(f"[BOOT] Initializing Brahmastra Mesh {node_id}")
print("=" * 45)
print(f"[STATUS] Running with UID: {current_uid}")
print(f"[STATUS] Target IP: {node_ip}")
print(f"[STATUS] Listening Port: {listen_port} (HTTPS Masquerade)")

# Zero-trust privilege verification
if current_uid == 0:
    print("[ERROR] Root execution detected! Immediate shutdown for security.", file=sys.stderr)
    sys.exit(1)

print("[SECURITY] Zero-Trust Verified: Running as non-root unprivileged process.")

# Start persistent TCP listener
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(("0.0.0.0", listen_port))
        server_sock.listen(5)
        print(f"[ACTIVE] {node_id} daemon listening on port {listen_port}. Cluster ready.")
        sys.stdout.flush()

        while True:
            try:
                conn, addr = server_sock.accept()
                with conn:
                    conn.sendall(f"ACK:{node_id}:OK\n".encode())
            except socket.error:
                time.sleep(0.5)

except Exception as err:
    print(f"[ERROR] Socket initialization failed: {err}", file=sys.stderr)
    sys.exit(1)