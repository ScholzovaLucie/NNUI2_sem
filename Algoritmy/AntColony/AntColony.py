import random


def id_to_int(hospoda_id):
    return int(hospoda_id) if isinstance(hospoda_id, float) else hospoda_id


class MravenciAlgoritmus:
    def __init__(self, hospody, spravce_hospod, pocet_mravencu, iterace, alfa, beta, odparovani):
        self.hospody = hospody
        self.spravce_hospod = spravce_hospod
        self.pocet_mravencu = pocet_mravencu
        self.iterace = iterace
        self.alfa = alfa  # Vliv feromonů
        self.beta = beta  # Vliv vzdálenosti
        self.odparovani = odparovani  # Rychlost odpařování feromonů
        self.feromony = [[1 for _ in range(len(hospody))] for _ in range(len(hospody))]
        self.cesty = [[] for _ in range(pocet_mravencu)]

    def vypocti_pravdepodobnost(self, mravenec, aktualni_hospoda):
        pravdepodobnosti = []
        for i in range(len(self.hospody)):
            if i not in self.cesty[mravenec]:
                feromon = self.feromony[aktualni_hospoda][i] ** self.alfa
                souradnice1 = self.spravce_hospod.ziskej_souradnice(aktualni_hospoda)
                souradnice2 = self.spravce_hospod.ziskej_souradnice(i)

                # Předání těchto souřadnic do funkce vypocti_vzdalenost
                inverzni_vzdalenost = (1 / self.spravce_hospod.vypocti_vzdalenost(*souradnice1,
                                                                                  *souradnice2)) ** self.beta
                pravdepodobnosti.append(feromon * inverzni_vzdalenost)
            else:
                pravdepodobnosti.append(0)
        suma = sum(pravdepodobnosti)
        return [p / suma for p in pravdepodobnosti]

    def najdi_cestu(self):
        for mravenec in range(self.pocet_mravencu):
            self.cesty[mravenec] = [random.randint(0, len(self.hospody) - 1)]
            while len(self.cesty[mravenec]) < len(self.hospody):
                pravdepodobnosti = self.vypocti_pravdepodobnost(mravenec, self.cesty[mravenec][-1])
                dalsi_hospoda = random.choices(range(len(self.hospody)), weights=pravdepodobnosti, k=1)[0]
                self.cesty[mravenec].append(dalsi_hospoda)

    def aktualizuj_feromony(self):
        for i in range(len(self.hospody)):
            for j in range(len(self.hospody)):
                self.feromony[i][j] *= (1 - self.odparovani)

        for mravenec in self.cesty:
            vzdalenost_cesty = self.spravce_hospod.vypocti_celkovou_vzdalenost(mravenec)
            for k in range(len(mravenec) - 1):
                self.feromony[mravenec[k]][mravenec[k+1]] += 1 / vzdalenost_cesty

    def solve(self):
        for _ in range(self.iterace):
            self.najdi_cestu()
            self.aktualizuj_feromony()
        nejlepsi_cesta = min(self.cesty, key=self.spravce_hospod.vypocti_celkovou_vzdalenost)
        return (
            self.spravce_hospod.dej_informace_o_nejlepsi_cesta(nejlepsi_cesta),
            self.spravce_hospod.vypocti_celkovou_vzdalenost(nejlepsi_cesta),
            'Algoritmus mravenčí kolonie'
        )
