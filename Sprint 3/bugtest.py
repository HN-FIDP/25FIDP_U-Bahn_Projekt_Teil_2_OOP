# test_runner.py
# =========================================================
# Automatische Tests für HaltestellenFinder
# =========================================================

# Importiere den Hauptcode aus test.py
from Test import linie_u1

# =========================================================
# Testfälle aus der Tabelle
# =========================================================
tests = [
    ("Messe", "Messe erkannt"),
    ("Fürth Hbf.", "Fürth Hauptbahnhof erkannt"),
    ("aufseßplatz", "Aufseßplatz erkannt"),
    ("Aufsessplatz", "Aufseßplatz erkannt"),
    ("Baerenchanze", "Bärenschanze erkannt"),
    ("Maffeiplat", "Maffeiplatz erkannt"),
    ("Jakobinenstrase", "Jakobinenstraße erkannt"),
    (" Gostenhof", "Gostenhof erkannt"),
    ("Langwasser-Nord", "Langwasser Nord erkannt"),
    ("Hauptbahnhof", "Hauptbahnhof erkannt"),
    ("Wasser", "Fehlermeldung"),
    ("Flughafen", "Fehlermeldung"),
]

# =========================================================
# Testlauf
# =========================================================
print("===== HaltestellenFinder Tests =====")
for i, (eingabe, erwartet) in enumerate(tests, start=1):
    print(f"\nTest {i}: Eingabe = '{eingabe}'")
    result = linie_u1.finder.finde(eingabe)
    if result:
        ausgabe = f"{result} erkannt"
    else:
        ausgabe = "Fehlermeldung"

    status = "✅ OK" if ausgabe == erwartet else "❌ FAIL"
    print(f"Erwartet: {erwartet} | Tatsächlich: {ausgabe} | {status}")
