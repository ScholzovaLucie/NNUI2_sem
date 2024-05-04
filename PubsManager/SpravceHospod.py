import math

import numpy as np


def create_distance_matrix(pubs_data):
    num_pubs = len(pubs_data)
    distance_matrix = np.zeros((num_pubs, num_pubs))

    for i in range(num_pubs):
        for j in range(num_pubs):
            if i != j:
                coord_i = np.array(pubs_data[i]['koordináty'])
                coord_j = np.array(pubs_data[j]['koordináty'])
                distance_matrix[i][j] = np.linalg.norm(coord_i - coord_j)

    return distance_matrix


def vypocti_vzdalenost(souradnice1, souradnice2):
    lat1, lon1, lat2, lon2 = map(math.radians, [*souradnice1, *souradnice2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0
    vzdalenost = r * c
    return vzdalenost


def print_solution(path, distance, description):
    print(description)
    print("Best path found:", path)
    print("Total distance covered:", distance)
    print("\n")


class SpravceHospod:
    def __init__(self, hospody):
        self.hospody = hospody

    def ziskej_souradnice(self, id_hospody):
        try:
            return self.hospody[id_hospody - 1]["koordináty"]
        except Exception as e:
            return 'invalid coordinates' + e.args[0]

    def vypocti_celkovou_vzdalenost(self, cesta):
        vypoctene_vzdalenosti = [
            vypocti_vzdalenost(self.ziskej_souradnice(a),
                               self.ziskej_souradnice(b))
            for a, b in zip(cesta, cesta[1:])
        ]
        return sum(vypoctene_vzdalenosti)

    def dej_informace_o_nejlepsi_cesta(self, nejlepsi_cesta):
        try:
            return [{"id": hospoda, "název": self.hospody[hospoda - 1]["název"]} for hospoda in nejlepsi_cesta]
        except Exception as e:
            return 'invalid path ' + e.args[0]
