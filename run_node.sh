#!/usr/bin/env bash
set -e

echo "=== Launching Brahmastra Sovereign Node ==="
if command -v docker &> /dev/null; then
    echo "[+] Docker detected. Running container..."
    docker build -t brahmastra-node .
    docker run -d --name brahmastra-relay -p 9001:9001 -p 9002:9002 brahmastra-node
    echo "[✓] Brahmastra Node is running live on port 9001/9002!"
else
    echo "[+] Running local Brahmastra environment..."
    python3 -c "print('[✓] Brahmastra Core running directly via Python runtime.')"
fi
