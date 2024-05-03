import math
import random


class Vzdalenost(object):

    def __init__(self, start, cil):
        self.start = start
        self.cil = cil

    def vzdalenost(self):
        # Funkce pro výpočet vzdálenosti mezi dvěma body
        lat1, lon1, lat2, lon2 = map(math.radians, [*self.start, *self.cil])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        # Poloměr Země v kilometrech
        r = 6371.0
        # Vzdálenost v kilometrech
        distance = r * c
        return distance