import math

import numpy as np


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

    def create_distance_matrix(self, pubs_data):
        num_pubs = len(pubs_data)
        distance_matrix = np.zeros((num_pubs, num_pubs))

        for i in range(num_pubs):
            for j in range(num_pubs):
                if i != j:
                    coord_i = np.array(pubs_data[i]['koordináty'])
                    coord_j = np.array(pubs_data[j]['koordináty'])
                    # Euklidovská vzdálenost mezi dvěma body
                    distance_matrix[i][j] = np.linalg.norm(coord_i - coord_j)

        return distance_matrix
