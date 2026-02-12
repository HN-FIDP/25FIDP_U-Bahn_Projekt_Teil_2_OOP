class TicketKategorie:
    KURZ = "Kurz"
    MITTEL = "Mittel"
    LANG = "Lang"

    @staticmethod
    def bestimme_kategorie(stationen: int) -> str:
        if stationen <= 3:
            return TicketKategorie.KURZ
        elif stationen <= 8:
            return TicketKategorie.MITTEL
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
    def berechne_preis(kategorie: str, ticketart: str, sozialrabatt: bool, barzahlung: bool) -> float:
        preis = TarifRechner.BASISPREISE[ticketart][kategorie]
        if ticketart == TicketArt.EINZEL:
            preis *= 1.10
        if sozialrabatt:
            preis *= 0.80
        if barzahlung:
            preis *= 1.15
        return round(preis, 2)
