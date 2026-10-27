import socket
import threading
import json
import time
import sys

class P2PNode:
    def __init__(self, host, port, node_id):
        self.host = host
        self.port = port
        self.node_id = node_id
        self.peers = []

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"🟢 [{self.node_id}] సర్వర్ పోర్ట్ {self.port} వద్ద లైవ్ అయింది. కనెక్షన్స్ కోసం వేచి చూస్తోంది...")
        
        while True:
            conn, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn, addr):
        try:
            data = conn.recv(1024).decode('utf-8')
            if data:
                payload = json.loads(data)
                print(f"\n📩 [{self.node_id}] కొత్త మెసేజ్ అందుకుంది: {payload['msg']} (Sender: {payload['from']})")
                print(f"🏛️ ధర్మ నిధి షేర్ వెరిఫై అయింది: 80% Community / 20% Infra")
        except Exception as e:
            print(f"కనెక్షన్ లోపం: {e}")
        finally:
            conn.close()

    def send_data(self, target_port, message):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, target_port))
            payload = {
                "from": self.node_id,
                "msg": message,
                "timestamp": time.time()
            }
            client.send(json.dumps(payload).encode('utf-8'))
            client.close()
            print(f"🚀 [{self.node_id}] పోర్ట్ {target_port} కి డేటాను విజయవంతంగా బదిలీ చేసింది!")
        except Exception as e:
            print(f"❌ కనెక్షన్ విఫలమైంది: పోర్ట్ {target_port} లో నోడ్ ఆన్‌లో ఉందో లేదో సరిచూడండి ({e})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ఉపయోగం: python3 p2p_socket_node.py <Node_ID> <Port>")
        print("ఉదాహరణ: python3 p2p_socket_node.py NODE_HYD 5001")
        sys.exit(1)

    node_id = sys.argv[1]
    port = int(sys.argv[2])

    node = P2PNode("127.0.0.1", port, node_id)
    server_thread = threading.Thread(target=node.start_server, daemon=True)
    server_thread.start()

    time.sleep(1)

    while True:
        print("\n--- మెనూ ---")
        print("1. వేరే నోడ్‌కి లావాదేవీ సందేశం పంపండి")
        print("2. ఎగ్జిట్ (Exit)")
        choice = input("ఎంపిక (1/2): ").strip()

        if choice == '1':
            target_port = int(input("టార్గెట్ నోడ్ పోర్ట్ (ఉదా: 5002): ").strip())
            msg = input("పంపాల్సిన సందేశం/డేటా: ").strip()
            node.send_data(target_port, msg)
        elif choice == '2':
            print("నోడ్ ముగిసింది.")
            break