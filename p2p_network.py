import hashlib
import time
import random

print("=== బ్రహ్మాస్త్రం: వికేంద్రీకృత P2P నోడ్ నెట్‌వర్క్ ఇంజిన్ ===\n")

class BrahmastraNode:
    def __init__(self, node_id, location):
        self.node_id = node_id
        self.location = location
        self.peers = []

    def connect_peer(self, peer_node):
        if peer_node not in self.peers:
            self.peers.append(peer_node)
            peer_node.peers.append(self)

    def relay_packet(self, sender_id, encrypted_payload, hops=3):
        if hops == 0:
            print(f"[{self.node_id} ({self.location})]: ప్యాకెట్ గమ్యాన్ని చేరింది! ప్రాసెసింగ్ ముగిసింది.")
            return

        print(f"[{self.node_id} ({self.location})]: ఎన్‌క్రిప్టెడ్ డేటాను తదుపరి నోడ్‌కు రిలే చేస్తోంది... (మిగిలిన హాప్స్: {hops})")
        time.sleep(0.4)

        # అందుబాటులో ఉన్న పీర్లలో ఒకదానికి ఫార్వర్డ్ చేయడం
        eligible_peers = [p for p in self.peers if p.node_id != sender_id]
        if eligible_peers:
            next_hop = random.choice(eligible_peers)
            next_hop.relay_packet(self.node_id, encrypted_payload, hops - 1)

# 1. ప్రపంచవ్యాప్తంగా 4 వర్చువల్ నోడ్లను సృష్టించడం
node_in = BrahmastraNode("Node_IND_01", "హైదరాబాద్, భారత్")
node_ch = BrahmastraNode("Node_CHE_01", "జ్యూరిచ్, స్విట్జర్లాండ్")
node_de = BrahmastraNode("Node_DEU_01", "ఫ్రాంక్‌ఫర్ట్, జర్మనీ")
node_sg = BrahmastraNode("Node_SGP_01", "సింగపూర్")

# 2. నోడ్ల మధ్య వికేంద్రీకృత మెష్ కనెక్షన్ల ఏర్పాటు
node_in.connect_peer(node_sg)
node_sg.connect_peer(node_ch)
node_ch.connect_peer(node_de)
node_de.connect_peer(node_in)

print(f"[నెట్‌వర్క్ స్థితి]: 4 అంతర్జాతీయ నోడ్లు మెష్ నెట్‌వర్క్‌గా అనుసంధానించబడ్డాయి.\n")

# 3. ఒక గోప్యమైన లావాదేవీ ప్యాకెట్‌ను పంపడం
mock_encrypted_payload = hashlib.sha256(b"Brahmastra_Encrypted_Tx_500Credits").hexdigest()
print(f"[ప్రారంభం]: Node_IND_01 నుంచి లావాదేవీ ప్యాకెట్ ప్రయాణం మొదలైంది...")
print(f"[సైఫర్‌టెక్స్ట్ హాష్]: {mock_encrypted_payload[:16]}...\n")

# ప్యాకెట్‌ను 3 హాప్స్ (జంప్స్) ద్వారా రూట్ చేయడం
node_in.relay_packet("CLIENT_USER", mock_encrypted_payload, hops=3)

print("\n" + "=" * 45)
print("P2P నెట్‌వర్క్ ధ్రువీకరణ: కేంద్రీకృత సర్వర్ లేకుండా డేటా సురక్షితంగా రిలే అయింది!")
print("=" * 45)