import math
import numpy as np


def create_distance_matrix(pubs_data):
    # Tato funkce vytváří matici vzdáleností mezi všemi páry hospod na základě jejich souřadnic.
    num_pubs = len(pubs_data)  # Počet hospod
    distance_matrix = np.zeros((num_pubs, num_pubs))  # Inicializace matice vzdáleností nulami

    for i in range(num_pubs):
        for j in range(num_pubs):
            if i != j:
                # Pro každý pár různých hospod vypočítá euklidovskou vzdálenost mezi nimi
                coord_i = np.array(pubs_data[i]['koordináty'])
                coord_j = np.array(pubs_data[j]['koordináty'])
                distance_matrix[i][j] = np.linalg.norm(coord_i - coord_j)

    return distance_matrix  # Vrátí matici s vypočítanými vzdálenostmi


def vypocti_vzdalenost(souradnice1, souradnice2):
    # Vypočítá geografickou vzdálenost mezi dvěma body na Zemi použitím Haversine vzorce
    lat1, lon1, lat2, lon2 = map(math.radians, [*souradnice1, *souradnice2])
    # Rozdíly v šířkách a délkách, výpočet pomocí sinů a kosinů
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0  # Předpokládaný poloměr Země v kilometrech
    return r * c  # Výsledná vzdálenost


def print_solution(path, distance, description):
    # Vytiskne popis a výsledky nalezené cesty
    print(description)
    print("Best path found:", path)
    print("Total distance covered:", distance)
    print("\n")


class SpravceHospod:
    def __init__(self, hospody):
        self.hospody = hospody  # Uchovává informace o hospodách

    def ziskej_souradnice(self, id_hospody):
        # Vrátí souřadnice hospody podle ID, ošetření chyb pokud ID neexistuje
        try:
            return self.hospody[id_hospody - 1]["koordináty"]
        except Exception as e:
            return 'invalid coordinates' + e.args[0]

    def vypocti_celkovou_vzdalenost(self, cesta):
        # Vypočítá celkovou vzdálenost uraženou na cestě procházející vybranými hospodami
        vypoctene_vzdalenosti = [vypocti_vzdalenost(self.ziskej_souradnice(a), self.ziskej_souradnice(b)) for a, b in zip(cesta, cesta[1:])]
        return sum(vypoctene_vzdalenosti)

    def dej_informace_o_nejlepsi_cesta(self, nejlepsi_cesta):
        # Vrátí informace o nejlepší cestě včetně ID a názvů hospod
        try:
            return [{"id": hospoda, "název": self.hospody[hospoda - 1]["název"]} for hospoda in nejlepsi_cesta]
        except Exception as e:
            return 'invalid path ' + e.args[0]
