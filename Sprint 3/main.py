from preislogik import TicketKategorie, TicketArt, TarifRechner
from fahrtzeitenrechner import erstelle_linie, ReiseBerechner
from datetime import datetime

def main():
    linie = erstelle_linie()

    # Start-Haltestelle abfragen
    while True:
        start_input = input("Start-Haltestelle: ")
        start = linie.finder.finde(start_input)
        if start:
            break
        print("Bitte gültige Start-Haltestelle eingeben.")

    # Ziel-Haltestelle abfragen
    while True:
        ziel_input = input("Ziel-Haltestelle: ")
        ziel = linie.finder.finde(ziel_input)
        if ziel:
            break
        print("Bitte gültige Ziel-Haltestelle eingeben.")

    # Früheste Abfahrt
    zeit = input("Früheste Abfahrt (HH:MM): ")

    # Nächste Abfahrt berechnen
    abfahrt = linie.naechste_abfahrt(start, ziel, zeit)
    if abfahrt is None:
        print("❌ Keine Abfahrt verfügbar.")
        return

    # Anzahl Stationen
    namen = [h.name for h in linie.haltestellen]
    stationen = abs(namen.index(start) - namen.index(ziel))

    # Ticketart
    print("1 = Einzelticket")
    print("2 = Mehrfahrtenticket")
    art_input = input("Ticketart: ")
    ticketart = TicketArt.EINZEL if art_input == "1" else TicketArt.MEHRFAHRT

    # Sozialrabatt & Barzahlung
    sozial = input("Sozialrabatt (j/n): ").lower() == "j"
    bar = input("Barzahlung (j/n): ").lower() == "j"

    # Preis berechnen
    kategorie = TicketKategorie.bestimme_kategorie(stationen)
    preis = TarifRechner.berechne_preis(kategorie, ticketart, sozial, bar)

    # Ankunft berechnen
    ankunft = ReiseBerechner.berechne_ankunft(linie, start, ziel, abfahrt)

    # Ausgabe
    print("\n===== REISE =====")
    print(f"Start: {start}")
    print(f"Ziel: {ziel}")
    print(f"Abfahrt: {abfahrt}")
    print(f"Ankunft: {ankunft}")
    print(f"Preis: {preis:.2f} €")
    print(f"Zeitstempel: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
