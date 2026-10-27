import hashlib
import time
import random

# బ్రహ్మాస్త్రం 5-నోడ్ నెట్‌వర్క్ క్లస్టర్
NODES = [
    {"id": "NODE_HYD_01", "location": "Hyderabad", "status": "ACTIVE"},
    {"id": "NODE_BLR_01", "location": "Bengaluru", "status": "ACTIVE"},
    {"id": "NODE_MUM_01", "location": "Mumbai", "status": "ACTIVE"},
    {"id": "NODE_CHE_01", "location": "Chennai", "status": "ACTIVE"},
    {"id": "NODE_SGP_01", "location": "Singapore", "status": "ACTIVE"}
]

def simulate_network():
    print("==================================================")
    print("🚀 బ్రహ్మాస్త్రం మల్టీ-నోడ్ డీసెంట్రలైజ్డ్ నెట్‌వర్క్ ప్రారంభం")
    print("==================================================")
    
    sender = random.choice(NODES)
    receivers = [n for n in NODES if n["id"] != sender["id"]]
    receiver = random.choice(receivers)
    
    tx_amount = 500.0  # క్రెడిట్స్
    fee = tx_amount * 0.01  # 1% నెట్‌వర్క్ ఫీజు
    dharma_pool = fee * 0.80  # 80% ధర్మ సంక్షేమ పూల్
    infra_pool = fee * 0.20   # 20% నిర్వహణ ఫీజు
    
    tx_data = f"{sender['id']}->{receiver['id']}:{tx_amount}:{time.time()}"
    tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
    
    print(f"\n[లావాదేవీ సృష్టి]: {sender['location']} ({sender['id']}) ➔ {receiver['location']} ({receiver['id']})")
    print(f"మొత్తం క్రెడిట్స్: {tx_amount} | ట్రాన్సాక్షన్ ఫీజు: {fee:.2f}")
    print(f"🔐 ఎన్‌క్రిప్టెడ్ హ్యాష్: {tx_hash}")
    
    print("\n📡 మిగిలిన నోడ్స్‌కు బ్రాడ్‌కాస్టింగ్ & కన్సెన్సస్ వెరిఫికేషన్ జరుగుతోంది...")
    time.sleep(1)
    
    verified_count = 0
    for node in NODES:
        time.sleep(0.3)
        print(f"  ✔ [{node['id']} - {node['location']}]: బ్లాక్ ధ్రువీకరించబడింది.")
        verified_count += 1
        
    print(f"\n[కన్సెన్సస్ ఫలితం]: 5/5 నోడ్స్ ఆమోదించాయి (100% సమన్వయం)")
    print("--------------------------------------------------")
    print(f"🏛️ ధర్మ సంక్షేమ పూల్ (80%): {dharma_pool:.2f} Credits జమ అయ్యాయి")
    print(f"⚙️ నెట్‌వర్క్ మెయింటెనెన్స్ (20%): {infra_pool:.2f} Credits")
    print("==================================================")
    print("✨ బ్రహ్మాస్త్రం ప్రొటోకాల్: గ్లోబల్ కన్సెన్సస్ సక్సెస్!")
    print("==================================================")

if __name__ == "__main__":
    simulate_network()