# Liste Abfahrtszeiten Haltestelle A
Abfahrtszeiten = [
    "05:00", "05:10", "05:20", "05:30", "05:40", "05:50",
    "06:00", "06:10", "06:20", "06:30", "06:40", "06:50",
    "07:00", "07:10", "07:20", "07:30", "07:40", "07:50",
    "08:00", "08:10", "08:20", "08:30", "08:40", "08:50",
    "09:00", "09:10", "09:20", "09:30", "09:40", "09:50",
    "10:00", "10:10", "10:20", "10:30", "10:40", "10:50",
    "11:00", "11:10", "11:20", "11:30", "11:40", "11:50",
    "12:00", "12:10", "12:20", "12:30", "12:40", "12:50",
    "13:00", "13:10", "13:20", "13:30", "13:40", "13:50",
    "14:00", "14:10", "14:20", "14:30", "14:40", "14:50",
    "15:00", "15:10", "15:20", "15:30", "15:40", "15:50",
    "16:00", "16:10", "16:20", "16:30", "16:40", "16:50",
    "17:00", "17:10", "17:20", "17:30", "17:40", "17:50",
    "18:00", "18:10", "18:20", "18:30", "18:40", "18:50",
    "19:00", "19:10", "19:20", "19:30", "19:40", "19:50",
    "20:00", "20:10", "20:20", "20:30", "20:40", "20:50",
    "21:00", "21:10", "21:20", "21:30", "21:40", "21:50",
    "22:00", "22:10", "22:20", "22:30", "22:40", "22:50",
    "23:00"
]

# Adjazenzliste mit Fahrzeiten in Minuten
Adjazenzliste = {
    "A": [("B", 2)],
    "B": [("C", 3)],
    "C": [("D", 1)],
    "D": []
}


# Zeit (HH:MM) → Minuten seit 00:00
def zeit_zu_minuten(zeit):
    stunde, minute = map(int, zeit.split(":"))
    return stunde * 60 + minute


# Klasse Haltestelle
class Haltestelle:
    def __init__(self, name):
        self.name = name

    def fahrzeit_von_a(self):
        zeit = 0
        aktuelle_haltestelle = "A"

        while aktuelle_haltestelle != self.name:
            verbindungen = Adjazenzliste[aktuelle_haltestelle]
            if not verbindungen:
                return None

            naechste, minuten = verbindungen[0]
            zeit += minuten
            aktuelle_haltestelle = naechste

        return zeit

    def naechste_ankunft(self, aktuelle_zeit):
        fahrzeit = self.fahrzeit_von_a()
        aktuelle_min = zeit_zu_minuten(aktuelle_zeit)

        for abfahrt in Abfahrtszeiten:
            abfahrt_min = zeit_zu_minuten(abfahrt)
            ankunft_min = abfahrt_min + fahrzeit

            if ankunft_min >= aktuelle_min:
                return f"{ankunft_min // 60:02d}:{ankunft_min % 60:02d}"

        return None


# Klasse UserInput
class UserInput:
    def haltestelle_eingabe(self):
        return input("Geben Sie ihre Start-Haltestelle ein (A-D): ").strip().upper()

    def zeit_eingabe(self):
        return input("Aktuelle Zeit (HH:MM): ").strip()


# Zeit-Validierung
def zeit_validieren(zeit):
    if ":" not in zeit:
        return False

    stunde, minute = zeit.split(":")

    if not (stunde.isdigit() and minute.isdigit()):
        return False

    stunde = int(stunde)
    minute = int(minute)

    return 0 <= stunde <= 23 and 0 <= minute <= 59


# Hauptprogramm
def main():
    haltestellen = {
        "A": Haltestelle("A"),
        "B": Haltestelle("B"),
        "C": Haltestelle("C"),
        "D": Haltestelle("D")
    }

    user_input = UserInput()

    # Haltestelle abfragen
    while True:
        haltestelle = user_input.haltestelle_eingabe()
        if haltestelle in haltestellen:
            break
        print("Ungültige Haltestelle! Bitte A, B, C oder D eingeben.\n")

    # Zeit abfragen
    while True:
        zeit = user_input.zeit_eingabe()
        if zeit_validieren(zeit):
            break
        print("Ungültige Zeit! Bitte im Format HH:MM (00:00 - 23:59) eingeben.\n")

    ankunft = haltestellen[haltestelle].naechste_ankunft(zeit)

    if ankunft is None:
        print("Keine weitere Bahn heute.")
    else:
        print(f"Nächste Bahn erreicht Haltestelle {haltestelle} um {ankunft} Uhr.")


# Programmstart
main()
