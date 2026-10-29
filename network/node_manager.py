"""
Brahmastra Mesh Network - Node Lifecycle Interface
Phase 3: Day 37 Architecture & Interface Setup
Defines node configuration structures and verifies container requirements.
"""

from dataclasses import dataclass
from typing import Dict, Any
import os


@dataclass(frozen=True)
class VirtualNodeConfig:
    node_id: str
    ip_address: str
    listen_port: int
    dockerfile_path: str
    user_id: int = 10001
    memory_limit_mb: int = 80

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "ip_address": self.ip_address,
            "listen_port": self.listen_port,
            "user_id": self.user_id,
            "memory_limit_mb": self.memory_limit_mb,
        }


class NodeLifecycleManager:
    """Manages virtual node configuration verification and execution lifecycle."""

    def __init__(self, config: VirtualNodeConfig):
        self.config = config

    def verify_interface_specifications(self) -> bool:
        """Validates that Dockerfile exists and security baselines are strictly defined."""
        if not os.path.exists(self.config.dockerfile_path):
            return False

        with open(self.config.dockerfile_path, "r") as f:
            content = f.read()

        # Strict Security Checks
        has_non_root = f"USER {self.config.user_id}" in content or "USER brahmastra_user" in content
        has_port_443 = f"EXPOSE {self.config.listen_port}" in content
        return has_non_root and has_port_443


def run_day_37_interface_verification() -> None:
    print("\n--- Starting Brahmastra Day 37: Node Interface & Architecture Verification ---")

    # Define Node-A configuration
    node_a_config = VirtualNodeConfig(
        node_id="Node-A",
        ip_address="172.28.0.10",
        listen_port=443,
        dockerfile_path="network/Dockerfile.node",
        user_id=10001,
        memory_limit_mb=80,
    )

    manager = NodeLifecycleManager(node_a_config)

    # 1. Verify Dockerfile exists
    assert os.path.exists(node_a_config.dockerfile_path), "Dockerfile.node missing"
    print(f"[PASS] Dockerfile verified at: {node_a_config.dockerfile_path}")

    # 2. Verify Documentation exists
    assert os.path.exists("docs/NODE_DOCKERFILE_ARCHITECTURE.md"), "Documentation file missing"
    print("[PASS] Technical documentation verified in docs/ folder.")

    # 3. Verify Non-root security configuration
    is_valid = manager.verify_interface_specifications()
    assert is_valid, "Security validation failed: Non-root user or port not configured correctly"
    print(f"[PASS] Security Architecture Verified: UID {node_a_config.user_id}, Non-Root Confirmed.")
    print(f"[PASS] Port Masking Confirmed: {node_a_config.listen_port} (HTTPS Masquerade).")

    print("\n=======================================================")
    print("DAY 37 SUCCESS: Node-A Architecture & Interface Ready.")
    print("=======================================================\n")


if __name__ == "__main__":
    run_day_37_interface_verification()