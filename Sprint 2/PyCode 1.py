import re
from typing import List
from difflib import SequenceMatcher

# =========================================================
# Eingabe-Normalisierung
# =========================================================

class InputNormalizer:
    UMLAUTS = {
        "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"
    }

    ABBREVIATIONS = {
        r"\bhbf\.?\b": "hauptbahnhof",
        r"\bstr\.?\b": "strasse",
        r"\bfr\.\-?\b": "friedrich"
    }

    @classmethod
    def normalize(cls, text: str) -> str:
        text = text.strip().lower().replace("-", " ")

        for k, v in cls.UMLAUTS.items():
            text = text.replace(k, v)

        for pattern, replacement in cls.ABBREVIATIONS.items():
            text = re.sub(pattern, replacement, text)

        return re.sub(r"\s+", " ", text)


# =========================================================
# Fuzzy-Matching
# =========================================================

class FuzzyMatcher:
    @staticmethod
    def similarity(a: str, b: str) -> float:
        return SequenceMatcher(None, a, b).ratio()


# =========================================================
# Haltestellen-Finder
# =========================================================

class HaltestellenFinder:
    def __init__(self, haltestellen: List[str]) -> None:
        self.haltestellen = haltestellen

    def finde(self, user_input: str) -> str | None:
        user_norm = InputNormalizer.normalize(user_input)
        kandidaten = []

        for name in self.haltestellen:
            score = FuzzyMatcher.similarity(
                user_norm,
                InputNormalizer.normalize(name)
            )
            if score >= 0.8:
                kandidaten.append((name, score))

        if not kandidaten:
            print("❌ Diese Haltestelle existiert nicht auf der Linie oder die Eingabe ist zu ungenau.")
            return None

        kandidaten.sort(key=lambda x: x[1], reverse=True)

        if len(kandidaten) > 1 and kandidaten[0][1] - kandidaten[1][1] < 0.05:
            print("⚠️ Die Eingabe ist nicht eindeutig. Bitte genauer eingeben.")
            return None

        return kandidaten[0][0]


# =========================================================
# Haltezeit & Haltestelle
# =========================================================

def haltezeit(name: str, erster_umlauf: bool = False) -> int:
    if erster_umlauf and name == "Langwasser Süd":
        return 0
    if name in ("Plärrer", "Hauptbahnhof", "Langwasser Süd", "Fürth Hauptbahnhof"):
        return 60
    return 30


class Haltestelle:
    def __init__(self, name: str, fahrzeit_zur_naechsten_min: int, haltezeit_sec: int) -> None:
        self.name = name
        self.fahrzeit_zur_naechsten = fahrzeit_zur_naechsten_min * 60
        self.haltezeit = haltezeit_sec


# =========================================================
# Linie U1
# =========================================================

class LinieU1:
    def __init__(self) -> None:
        self.haltestellen: List[Haltestelle] = []
        self.takt = 10 * 60
        self.startzeit = self.hhmm_to_seconds("05:00")
        self.endzeit = self.hhmm_to_seconds("23:00")
        self.finder: HaltestellenFinder | None = None

    def add_haltestelle(self, h: Haltestelle) -> None:
        self.haltestellen.append(h)

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

    def naechste_abfahrt(self, start: str, ziel: str, zeit_input: str) -> str | None:
        try:
            frueheste = self.hhmm_to_seconds(zeit_input)
        except Exception:
            print("❌ Ungültiges Zeitformat. Bitte HH:MM verwenden.")
            return None

        namen = [h.name for h in self.haltestellen]

        start_idx = namen.index(start)
        ziel_idx = namen.index(ziel)
        hin = start_idx < ziel_idx
        umlauf = 0

        while True:
            start_langwasser = self.startzeit + umlauf * self.takt
            if start_langwasser > self.endzeit:
                print("❌ Zu dieser Uhrzeit fährt keine Bahn mehr.")
                return None

            if hin:
                abfahrt = start_langwasser
                for i in range(start_idx):
                    abfahrt += self.haltestellen[i].fahrzeit_zur_naechsten
                    abfahrt += self.haltestellen[i].haltezeit
                if start_idx != 0:
                    abfahrt += self.haltestellen[start_idx].haltezeit
            else:
                hin_gesamt = 0
                for i in range(len(self.haltestellen) - 1):
                    hin_gesamt += self.haltestellen[i].fahrzeit_zur_naechsten
                    hin_gesamt += self.haltestellen[i].haltezeit

                wende = self.haltestellen[-1].haltezeit

                rueck = 0
                for i in range(len(self.haltestellen) - 1, start_idx, -1):
                    rueck += self.haltestellen[i - 1].fahrzeit_zur_naechsten
                    rueck += self.haltestellen[i].haltezeit

                abfahrt = start_langwasser + hin_gesamt + wende + rueck

            if abfahrt >= frueheste:
                return self.seconds_to_hhmmss(abfahrt)

            umlauf += 1


# =========================================================
# Benutzer-Dialog (SOFORTIGE VALIDIERUNG)
# =========================================================

class UserDialog:
    def __init__(self, linie: LinieU1) -> None:
        self.linie = linie

    def start(self) -> None:
        while True:
            start_input = input("Start-Haltestelle: ")
            start = self.linie.finder.finde(start_input)
            if not start:
                continue

            ziel_input = input("Ziel-Haltestelle: ")
            ziel = self.linie.finder.finde(ziel_input)
            if not ziel:
                continue

            if start == ziel:
                print("⚠️ Start und Ziel dürfen nicht gleich sein.")
                continue

            zeit = input("Früheste gewünschte Abfahrtszeit (HH:MM): ")

            abfahrt = self.linie.naechste_abfahrt(start, ziel, zeit)
            if abfahrt:
                print(f"✅ Nächste Abfahrt: {abfahrt} Uhr")
                break


# =========================================================
# Initialisierung
# =========================================================

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
    ("Fürth Hauptbahnhof", 0),
]

for name, fahrzeit in haltestellen_daten:
    linie_u1.add_haltestelle(
        Haltestelle(name, fahrzeit, haltezeit(name, name == "Langwasser Süd"))
    )

linie_u1.finder = HaltestellenFinder([h.name for h in linie_u1.haltestellen])

UserDialog(linie_u1).start()
