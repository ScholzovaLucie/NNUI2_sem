import math


class SpravceHospod:
    def __init__(self, hospody):
        # Inicializace správce hospod s poskytnutými hospodami
        self.hospody = hospody

    def ziskej_souradnice(self, id_hospody):
        # Získání souřadnic hospody na základě poskytnutého ID
        return self.hospody[id_hospody - 1]["koordináty"]

    def vypocti_vzdalenost(self, souradnice1, souradnice2):
        # Výpočet vzdálenosti mezi dvěma body na zeměkouli
        lat1, lon1, lat2, lon2 = map(math.radians, [*souradnice1, *souradnice2])  # Zjednodušení převodu do radiánů
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371.0  # Poloměr Země v kilometrech
        vzdalenost = r * c
        return vzdalenost
