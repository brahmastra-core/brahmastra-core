import os
import sys
import json
import time

LEDGER_FILE = "dharma_ledger.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    print("=" * 60)
    print("      🏹 బ్రహ్మాస్త్రం కోర్ (BRAHMASTRA-CORE) డ్యాష్‌బోర్డ్ 🏹      ")
    print("          డీసెంట్రలైజ్డ్ ధర్మ ప్రోటోకాల్ కమాండ్ సెంటర్           ")
    print("=" * 60)

def view_ledger():
    if not os.path.exists(LEDGER_FILE):
        print("\n⚠️ లెడ్జర్ ఫైల్ ఇంకా క్రియేట్ కాలేదు. దయచేసి లావాదేవీని ప్రారంభించండి.")
        return
    with open(LEDGER_FILE, "r") as f:
        data = json.load(f)
    
    print("\n--- [ఆన్-చైన్ ధర్మ నిధి నిల్వలు] ---")
    print(f"🏛️ ధర్మ సంక్షేమ పూల్ : {data.get('total_dharma_pool', 0):.2f} Credits")
    print(f"⚙️ నెట్‌వర్క్ పూల్   : {data.get('total_infra_pool', 0):.2f} Credits")
    print(f"📦 మొత్తం బ్లాక్స్    : {len(data.get('chain', []))}")
    print("\n--- [తాజా బ్లాక్స్ హిస్టరీ] ---")
    for block in data.get('chain', [])[-3:]:
        print(f"Block #{block['block_id']} | From: {block['sender']} -> To: {block['receiver']} | Amt: {block['amount']} Cr")
        print(f"Hash: {block['block_hash'][:24]}...")
        print("-" * 40)

def send_transaction():
    try:
        from dharma_ledger import record_transaction
        print("\n--- [కొత్త లావాదేవీని సృష్టించండి] ---")
        sender = input("పంపే నోడ్ ID (ఉదా: NODE_HYD_01): ").strip()
        receiver = input("స్వీకరించే నోడ్ ID (ఉదా: NODE_SGP_01): ").strip()
        amount_str = input("ట్రాన్స్‌ఫర్ క్రెడిట్స్ పరిమాణం: ").strip()
        if not sender or not receiver or not amount_str:
            print("❌ వివరాలు సరిగ్గా ఇవ్వలేదు!")
            return
        amount = float(amount_str)
        record_transaction(sender, receiver, amount)
    except Exception as e:
        print(f"❌ లావాదేవీ విఫలమైంది: {e}")

def main_menu():
    while True:
        show_banner()
        print("\n1. 📊 ధర్మ నిధి & బ్లాక్‌చెయిన్ లెడ్జర్ చూడండి")
        print("2. 💸 కొత్త లావాదేవీని రికార్డ్ చేయండి")
        print("3. 🛡️ భేద్య షీల్డ్ సెక్యూరిటీ ఆడిట్ రన్ చేయండి")
        print("4. 🌐 5-నోడ్ మల్టీ కన్సెన్సస్ సిమ్యులేట్ చేయండి")
        print("5. ❌ నిష్క్రమించండి (Exit)")
        print("=" * 60)
        
        choice = input("మీ ఎంపికను ఎంచుకోండి (1-5): ").strip()
        
        if choice == '1':
            view_ledger()
            input("\nకొనసాగడానికి Enter నొక్కండి...")
        elif choice == '2':
            send_transaction()
            input("\nకొనసాగడానికి Enter నొక్కండి...")
        elif choice == '3':
            os.system("python3 security_audit.py")
            input("\nకొనసాగడానికి Enter నొక్కండి...")
        elif choice == '4':
            os.system("python3 multi_node_sim.py")
            input("\nకొనసాగడానికి Enter నొక్కండి...")
        elif choice == '5':
            print("\n👋 బ్రహ్మాస్త్రం కమాండ్ సెంటర్ ముగిసింది. జై హింద్!")
            sys.exit(0)
        else:
            print("❌ సరైన ఎంపికను ఇవ్వండి!")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()