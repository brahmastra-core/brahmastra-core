import json
import os
import time
import hashlib

LEDGER_FILE = "dharma_ledger.json"

def init_ledger():
    if not os.path.exists(LEDGER_FILE):
        genesis_block = {
            "chain": [
                {
                    "block_id": 0,
                    "timestamp": time.time(),
                    "sender": "GENESIS",
                    "receiver": "DHARMA_ROOT",
                    "amount": 0,
                    "dharma_welfare_pool": 0,
                    "infra_maintenance": 0,
                    "prev_hash": "0" * 64,
                    "block_hash": "GENESIS_BLOCK_BRAHMASTRA"
                }
            ],
            "total_dharma_pool": 0.0,
            "total_infra_pool": 0.0
        }
        with open(LEDGER_FILE, "w") as f:
            json.dump(genesis_block, f, indent=4)
        print("🏛️ జెనెసిస్ బ్లాక్ (Genesis Block) విజయవంతంగా సృష్టించబడింది!")

def record_transaction(sender, receiver, amount):
    init_ledger()
    with open(LEDGER_FILE, "r") as f:
        data = json.load(f)

    fee = amount * 0.01  # 1% ట్రాన్సాక్షన్ ఫీజు
    dharma_share = fee * 0.80  # 80% ధర్మ పూల్
    infra_share = fee * 0.20   # 20% మెయింటెనెన్స్ ఫీజు

    last_block = data["chain"][-1]
    prev_hash = last_block["block_hash"]
    
    tx_raw = f"{sender}:{receiver}:{amount}:{time.time()}:{prev_hash}"
    block_hash = hashlib.sha256(tx_raw.encode()).hexdigest()

    new_block = {
        "block_id": len(data["chain"]),
        "timestamp": time.time(),
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "dharma_welfare_pool": dharma_share,
        "infra_maintenance": infra_share,
        "prev_hash": prev_hash,
        "block_hash": block_hash
    }

    data["chain"].append(new_block)
    data["total_dharma_pool"] += dharma_share
    data["total_infra_pool"] += infra_share

    with open(LEDGER_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("==================================================")
    print(f"📦 కొత్త బ్లాక్ #{new_block['block_id']} ఆన్-చైన్ లెడ్జర్‌లో రికార్డ్ అయింది!")
    print(f"🔗 బ్లాక్ హ్యాష్: {block_hash}")
    print(f"🏛️ మొత్తం ధర్మ నిధి నిల్వ: {data['total_dharma_pool']:.2f} Credits")
    print(f"⚙️ మొత్తం నెట్‌వర్క్ నిల్వ: {data['total_infra_pool']:.2f} Credits")
    print("==================================================")

if __name__ == "__main__":
    init_ledger()
    print("\nటెస్ట్ లావాదేవీని రికార్డ్ చేస్తున్నాం...")
    record_transaction("NODE_HYD_01", "NODE_CHE_01", 1000.0)