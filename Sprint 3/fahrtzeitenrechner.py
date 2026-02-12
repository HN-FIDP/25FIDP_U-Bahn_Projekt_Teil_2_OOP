from typing import List
from normalizer import HaltestellenFinder

def haltezeit(name: str, erster_umlauf: bool = False) -> int:
    if erster_umlauf and name == "Langwasser Süd":
        return 0
    if name in ("Plärrer", "Hauptbahnhof", "Langwasser Süd", "Fürth Hauptbahnhof"):
        return 60
    return 30

class Haltestelle:
    def __init__(self, name: str, fahrzeit_min: int, erster_umlauf: bool = False):
        self.name = name
        self.fahrzeit_zur_naechsten = fahrzeit_min * 60
        self.haltezeit = haltezeit(name, erster_umlauf)

class LinieU1:
    def __init__(self):
        self.haltestellen: List[Haltestelle] = []
        self.takt = 10 * 60
        self.startzeit = self.hhmm_to_seconds("05:00")
        self.endzeit = self.hhmm_to_seconds("23:00")
        self.finder: HaltestellenFinder | None = None

    @staticmethod
    def hhmm_to_seconds(zeit: str) -> int:
        teile = list(map(int, zeit.split(":")))
        if len(teile) == 2:
            h, m = teile
            s = 0
        elif len(teile) == 3:
            h, m, s = teile
        else:
            raise ValueError("Ungültiges Zeitformat")
        return h * 3600 + m * 60 + s

    @staticmethod
    def seconds_to_hhmmss(seconds: int) -> str:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def add_haltestelle(self, h: Haltestelle):
        self.haltestellen.append(h)

    def naechste_abfahrt(self, start: str, ziel: str, zeit_input: str) -> str | None:
        try:
            frueheste = self.hhmm_to_seconds(zeit_input)
        except:
            return None

        namen = [h.name for h in self.haltestellen]
        start_idx = namen.index(start)

        umlauf = 0
        while True:
            start_langwasser = self.startzeit + umlauf * self.takt
            if start_langwasser > self.endzeit:
                return None

            abfahrt = start_langwasser
            for i in range(start_idx):
                abfahrt += self.haltestellen[i].fahrzeit_zur_naechsten
                abfahrt += self.haltestellen[i].haltezeit
            if start_idx != 0:
                abfahrt += self.haltestellen[start_idx].haltezeit

            if abfahrt >= frueheste:
                return self.seconds_to_hhmmss(abfahrt)

            umlauf += 1

class ReiseBerechner:
    @staticmethod
    def berechne_ankunft(linie: LinieU1, start: str, ziel: str, abfahrtszeit: str) -> str:
        start_sec = LinieU1.hhmm_to_seconds(abfahrtszeit)
        namen = [h.name for h in linie.haltestellen]
        start_idx = namen.index(start)
        ziel_idx = namen.index(ziel)
        zeit = start_sec
        if start_idx < ziel_idx:
            for i in range(start_idx, ziel_idx):
                zeit += linie.haltestellen[i].fahrzeit_zur_naechsten
                zeit += linie.haltestellen[i + 1].haltezeit
        else:
            for i in range(start_idx, ziel_idx, -1):
                zeit += linie.haltestellen[i - 1].fahrzeit_zur_naechsten
                zeit += linie.haltestellen[i - 1].haltezeit
        return LinieU1.seconds_to_hhmmss(zeit)

def erstelle_linie():
    from normalizer import HaltestellenFinder
    linie = LinieU1()
    daten = [
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
    for idx, (name, fahrzeit) in enumerate(daten):
        linie.add_haltestelle(Haltestelle(name, fahrzeit, erster_umlauf=(idx == 0)))
    linie.finder = HaltestellenFinder([h.name for h in linie.haltestellen])
    return linie
