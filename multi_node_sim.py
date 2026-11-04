import hashlib
import time
import random

# Brahmastra 5-Node Network Cluster
NODES = [
 {"id": "NODE_HYD_01", "location": "Hyderabad", "status": "ACTIVE"},
 {"id": "NODE_BLR_01", "location": "Bengaluru", "status": "ACTIVE"},
 {"id": "NODE_MUM_01", "location": "Mumbai", "status": "ACTIVE"},
 {"id": "NODE_CHE_01", "location": "Chennai", "status": "ACTIVE"},
 {"id": "NODE_SGP_01", "location": "Singapore", "status": "ACTIVE"}
]

def simulate_network():
 print("==================================================")
 print("🚀 Brahmastra Multi-Node Decentralized Network Initialized")
 print("==================================================")
 
 sender = random.choice(NODES)
 receivers = [n for n in NODES if n["id"] != sender["id"]]
 receiver = random.choice(receivers)
 
 tx_amount = 500.0 # Credits
 fee = tx_amount * 0.01 # 1% Network Fee
 dharma_pool = fee * 0.80 # 80% Dharma Welfare Pool
 infra_pool = fee * 0.20 # 20% Maintenance Fee
 
 tx_data = f"{sender['id']}->{receiver['id']}:{tx_amount}:{time.time()}"
 tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
 
 print(f"\n[Transaction Created]: {sender['location']} ({sender['id']}) ➔ {receiver['location']} ({receiver['id']})")
 print(f" Credits: {tx_amount} | Transaction Fee: {fee:.2f}")
 print(f"🔐 Encrypted Hash: {tx_hash}")
 
 print("\n📡 ‌ ‌ & ...")
 time.sleep(1)
 
 verified_count = 0
 for node in NODES:
 time.sleep(0.3)
 print(f" ✔ [{node['id']} - {node['location']}]: Block Verified.")
 verified_count += 1
 
 print(f"\n[Consensus Result]: 5/5 Nodes Approved (100% Synchronized)")
 print("--------------------------------------------------")
 print(f"🏛️ Dharma Welfare Pool (80%): {dharma_pool:.2f} Credits ")
 print(f"⚙️ Network Maintenance (20%): {infra_pool:.2f} Credits")
 print("==================================================")
 print("✨ Brahmastra Protocol: Global Consensus Success!")
 print("==================================================")

if __name__ == "__main__":
 simulate_network()