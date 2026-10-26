import time
import random
import secrets

print("--- బ్రహ్మాస్త్రం మిక్స్‌నెట్ & డెకాయ్ రూటింగ్ ఇంజిన్ ---\n")

# అసలైన రహస్య సందేశం
real_message = "బ్రహ్మాస్త్రం గోప్యతా డేటా: యూజర్ ID #7789"
print(f"[యూజర్ అసలు సందేశం]: {real_message}")

# 1. డెకాయ్ (నకిలీ) ప్యాకెట్ల సృష్టి - ట్రాకింగ్ వ్యవస్థలను తప్పుదోవ పట్టించడానికి
def generate_decoy():
    return f"DECOY_{secrets.token_hex(4)}"

packets = [
    {"type": "REAL", "payload": real_message},
    {"type": "DECOY", "payload": generate_decoy()},
    {"type": "DECOY", "payload": generate_decoy()},
    {"type": "DECOY", "payload": generate_decoy()}
]

print(f"\n[ట్రాఫిక్ ఇంజెక్షన్]: 1 అసలు ప్యాకెట్ + 3 నకిలీ డెకాయ్ ప్యాకెట్లు కలపబడ్డాయి.")

# 2. ప్యాకెట్లను మిక్సర్ (షఫుల్) చేయడం
random.shuffle(packets)
print("[మిక్స్‌నెట్ పూల్]: ప్యాకెట్ల క్రమాన్ని పూర్తిగా తారుమారు చేశాం.")

# 3. Sphinx Delay సిమ్యులేషన్ (టైమింగ్ అటాక్స్ జరగకుండా డిలే ఇవ్వడం)
print("\n--- పీర్-టు-పీర్ రూటింగ్ ప్రారంభమైంది ---")
for index, pkt in enumerate(packets, start=1):
    delay = round(random.uniform(0.3, 0.9), 2)
    time.sleep(delay)  # యాదృచ్ఛిక సమయం ఆగి పంపడం
    
    if pkt["type"] == "REAL":
        print(f"నోడ్ {index} -> ప్యాకెట్ చేరింది (రిసీవర్‌కు అసలు డేటా డెలివరీ అయింది) [ఆలస్యం: {delay}s]")
    else:
        print(f"నోడ్ {index} -> డెకాయ్ ప్యాకెట్ డ్రాప్ అయింది (ట్రాకర్స్ కన్ఫ్యూజ్ అయ్యాయి) [ఆలస్యం: {delay}s]")

print("\n[ఫలితం]: బిగ్-టెక్ సంస్థలు అసలైన ట్రాఫిక్‌ను ట్రాక్ చేయలేకపోయాయి. రూటింగ్ సక్సెస్!")