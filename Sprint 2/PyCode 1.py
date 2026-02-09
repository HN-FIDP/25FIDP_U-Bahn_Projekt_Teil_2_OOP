from typing import List

# ----------------- Haltezeiten -----------------
def haltezeit(name: str, erster_umlauf: bool = False) -> int:
    """
    Gibt die Haltezeit in Sekunden zurück.
    Ausnahme: erster Zug um 05:00 ab Langwasser Süd → Haltezeiten zählen nicht.
    """
    if erster_umlauf and name == "Langwasser Süd":
        return 0  # erste Fahrt ab 05:00 → keine Haltezeit am Start
    if name in ("Plärrer", "Hauptbahnhof", "Langwasser Süd", "Fürth Hbf."):
        return 60
    return 30

# ----------------- Klasse Haltestelle -----------------
class Haltestelle:
    def __init__(self, name: str, fahrzeit_zur_naechsten_min: int, haltezeit_sec: int) -> None:
        self.name: str = name
        self.fahrzeit_zur_naechsten: int = fahrzeit_zur_naechsten_min * 60
        self.haltezeit: int = haltezeit_sec

# ----------------- Klasse Linie U1 -----------------
class LinieU1:
    def __init__(self) -> None:
        self.haltestellen: List[Haltestelle] = []
        self.takt: int = 10 * 60
        self.startzeit: int = self.hhmm_to_seconds("05:00")
        self.endzeit: int = self.hhmm_to_seconds("23:00")

    def add_haltestelle(self, haltestelle: Haltestelle) -> None:
        self.haltestellen.append(haltestelle)

    @staticmethod
    def hhmm_to_seconds(hhmm: str) -> int:
        h, m = map(int, hhmm.split(":"))
        return h * 3600 + m * 60

    @staticmethod
    def seconds_to_hhmmss(seconds: int) -> str:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    # ----------------- Fahrzeitberechnung -----------------
    def _fahrzeit_bis(self, von_idx: int, bis_idx: int, start_ist_umlauf: bool, halte_start: bool = True) -> int:
        """
        Berechnet Fahrzeit inkl. Haltezeiten zwischen von_idx und bis_idx.
        halte_start=False → Haltezeit der ersten Station wird nicht gezählt (für Rückfahrt).
        Zielhaltezeit wird nie gezählt.
        """
        zeit = 0
        step = 1 if bis_idx > von_idx else -1
        for i in range(von_idx, bis_idx, step):
            zeit += self.haltestellen[i].fahrzeit_zur_naechsten
            # Haltezeit der Zwischenstationen
            if not (start_ist_umlauf and i == von_idx and self.haltestellen[i].name == "Langwasser Süd"):
                if halte_start or i != von_idx:
                    zeit += self.haltestellen[i].haltezeit
        return zeit

    # ----------------- Berechnung der nächsten Abfahrt -----------------
    def naechste_abfahrt(self, start_name: str, ziel_name: str, frueheste_hhmm: str) -> str:
        frueheste = self.hhmm_to_seconds(frueheste_hhmm)
        namen = [h.name for h in self.haltestellen]

        if start_name not in namen or ziel_name not in namen:
            raise ValueError("Ungültige Haltestelle.")
        if start_name == ziel_name:
            raise ValueError("Start und Ziel dürfen nicht gleich sein.")

        start_idx = namen.index(start_name)
        ziel_idx = namen.index(ziel_name)
        hin = start_idx < ziel_idx
        umlauf = 0

        while True:
            start_langwasser = self.startzeit + umlauf * self.takt
            if start_langwasser > self.endzeit:
                raise ValueError("Zu dieser Uhrzeit fährt keine Bahn mehr.")

            # erster Umlauf für Haltezeit am Langwasser Süd Start
            erster_umlauf = (umlauf == 0)

            if hin:
                # -------- Hinfahrt --------
                abfahrt_start = start_langwasser + self._fahrzeit_bis(0, start_idx, start_ist_umlauf=True)
                if start_idx != 0:
                    abfahrt_start += self.haltestellen[start_idx].haltezeit
            else:
                # -------- Rückfahrt --------
                hin_gesamt = self._fahrzeit_bis(0, len(self.haltestellen) - 1, start_ist_umlauf=True)
                wende = self.haltestellen[-1].haltezeit  # Haltezeit Fürth Hbf
                rueck_bis_start = self._fahrzeit_bis(len(self.haltestellen) - 1, start_idx, start_ist_umlauf=False, halte_start=False)
                abfahrt_start = start_langwasser + hin_gesamt + wende + rueck_bis_start

            if abfahrt_start >= frueheste:
                return self.seconds_to_hhmmss(abfahrt_start)

            umlauf += 1

# ----------------- Linie U1 erstellen -----------------
linie_u1 = LinieU1()

haltestellen_daten = [
    ("Langwasser Süd", 3),
    ("Gemeinschaftshaus", 2),
    ("Langwasser Mitte", 2),
    ("Scharfreiterring", 3),
    ("Langwasser Nord", 2),
    ("Messe", 3),
    ("Bauernfeindstraße", 2),
    ("Hasenbuck", 2),
    ("Frankenstraße", 2),
    ("Maffeiplatz", 1),
    ("Aufseßplatz", 2),
    ("Hauptbahnhof", 2),
    ("Lorenzkirche", 3),
    ("Weißer Turm", 2),
    ("Plärrer", 2),
    ("Gostenhof", 1),
    ("Bärenschanze", 2),
    ("Maximilianstraße", 2),
    ("Eberhardshof", 2),
    ("Muggenhof", 3),
    ("Stadtgrenze", 2),
    ("Jakobinenstraße", 3),
    ("Fürth Hbf.", 0),
]

for name, fahrzeit in haltestellen_daten:
    # erster Umlauf Langwasser Süd
    if name == "Langwasser Süd":
        linie_u1.add_haltestelle(Haltestelle(name, fahrzeit, haltezeit(name, erster_umlauf=True)))
    else:
        linie_u1.add_haltestelle(Haltestelle(name, fahrzeit, haltezeit(name)))

# ----------------- Benutzerabfrage -----------------
start = input("Start-Haltestelle: ")
ziel = input("Ziel-Haltestelle: ")
zeit = input("Früheste gewünschte Abfahrtszeit (HH:MM): ")

try:
    abfahrt = linie_u1.naechste_abfahrt(start, ziel, zeit)
    print(f"Nächste Abfahrt: {abfahrt} Uhr")
except ValueError as e:
    print(e)
