class TicketKategorie:
    KURZ = "Kurz"
    MITTEL = "Mittel"
    LANG = "Lang"

    @staticmethod
    def bestimme_kategorie(stationen: int) -> str:
        if stationen < 1:
            raise ValueError("Stationen müssen mindestens 1 sein.")

        if 1 <= stationen <= 3:
            return TicketKategorie.KURZ
        elif 4 <= stationen <= 8:
            return TicketKategorie.MITTEL
        else:
            return TicketKategorie.LANG


class TicketArt:
    EINZEL = "Einzelticket"
    MEHRFAHRT = "Mehrfahrtenticket"


class TarifRechner:
    BASISPREISE = {
        TicketArt.EINZEL: {
            TicketKategorie.KURZ: 1.50,
            TicketKategorie.MITTEL: 2.00,
            TicketKategorie.LANG: 3.00,
        },
        TicketArt.MEHRFAHRT: {
            TicketKategorie.KURZ: 5.00,
            TicketKategorie.MITTEL: 7.00,
            TicketKategorie.LANG: 10.00,
        },
    }

    @staticmethod
    def berechne_preis(kategorie: str,
                       ticketart: str,
                       sozialrabatt: bool = False,
                       barzahlung: bool = False) -> float:

        basispreis = TarifRechner.BASISPREISE[ticketart][kategorie]

        # Prozentuale Änderungen sammeln
        prozent_aenderung = 0.0

        # +10% für Einzelticket
        if ticketart == TicketArt.EINZEL:
            prozent_aenderung += 0.10

        # -20% Sozialrabatt
        if sozialrabatt:
            prozent_aenderung -= 0.20

        # +15% Barzahlung
        if barzahlung:
            prozent_aenderung += 0.15

        # Einmalige Berechnung
        endpreis = basispreis * (1 + prozent_aenderung)

        return round(endpreis, 2)
