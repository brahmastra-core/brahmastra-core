import hashlib
import random

print("--- బ్రహ్మాస్త్రం జీరో-నాలెడ్జ్ ప్రూఫ్ (ZKP) ఇంజిన్ ---")

# పెద్ద ప్రైమ్ నంబర్లు (గణిత గ్రూప్ పారామీటర్లు)
p = 2**256 - 189
g = 2

# 1. యూజర్ రహస్యం (Secret Key / Password) - ఇది ఎవరికీ కనిపించకూడదు
secret_x = 987654321
# పబ్లిక్ కీ (సర్వర్‌కు తెలిసేది కేవలం ఇది మాత్రమే)
public_y = pow(g, secret_x, p)

print(f"పబ్లిక్ కీ (సర్వర్‌కు తెలిసినది): {str(public_y)[:20]}...")
print("రహస్య కీ (Secret): సురక్షితంగా యూజర్ దగ్గరే దాచబడింది.")

# 2. యూజర్ ఇచ్చే ప్రామాణిక ప్రూఫ్ (Commitment & Proof Generation)
v = random.randint(1, p - 1)
t = pow(g, v, p)

# ఛాలెంజ్ క్రియేషన్ (క్రిప్టోగ్రాఫిక్ హాష్ ద్వారా)
challenge_c = int(hashlib.sha256(f"{g}{public_y}{t}".encode()).hexdigest(), 16) % p

# రెస్పాన్స్ గణన (రహస్యాన్ని వాడి లెక్కించడం, కానీ రహస్యాన్ని బయటపెట్టకుండా)
response_r = (v - challenge_c * secret_x) % (p - 1)

print("\nప్రూఫ్ సిద్ధమైంది (Proof Generated) -> సర్వర్‌కు పంపబడుతోంది...")

# 3. సర్వర్ ధ్రువీకరణ (Verification without knowing Secret)
verification_t = (pow(g, response_r, p) * pow(public_y, challenge_c, p)) % p

if verification_t == t:
    print("\n[VERIFICATION: SUCCESS]")
    print("ఫలితం: పాస్‌వర్డ్/రహస్యం తెలియకుండానే యూజర్ అసలైనవాడని సర్వర్ నిర్ధారించింది!")
else:
    print("\n[VERIFICATION: FAILED]")
    print("ఫలితం: తప్పుడు ప్రూఫ్!")