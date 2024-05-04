import random
from PubsManager.SpravceHospod import vypocti_vzdalenost

def id_to_int(hospoda_id):
    # Konvertuje ID hospody na celé číslo, pokud je vstup float.
    return int(hospoda_id) if isinstance(hospoda_id, float) else hospoda_id

class MravenciAlgoritmus:
    def __init__(self, hospody, spravce_hospod, pocet_mravencu, iterace, alfa, beta, odparovani):
        # Inicializuje parametry algoritmu mravenčí kolonie.
        self.hospody = hospody
        self.spravce_hospod = spravce_hospod
        self.pocet_mravencu = pocet_mravencu
        self.iterace = iterace
        self.alfa = alfa
        self.beta = beta
        self.odparovani = odparovani
        self.feromony = [[1 for _ in range(len(hospody))] for _ in range(len(hospody))]
        self.cesty = [[] for _ in range(pocet_mravencu)]

    def vypocti_pravdepodobnost(self, mravenec, aktualni_hospoda):
        # Vypočítá pravděpodobnosti výběru následujícího města pro daného mravence.
        pravdepodobnosti = []
        for i in range(len(self.hospody)):
            if i not in self.cesty[mravenec]:
                feromon = self.feromony[aktualni_hospoda][i] ** self.alfa
                souradnice1 = self.spravce_hospod.ziskej_souradnice(aktualni_hospoda)
                souradnice2 = self.spravce_hospod.ziskej_souradnice(i)
                inverzni_vzdalenost = (1 / vypocti_vzdalenost(souradnice1, souradnice2)) ** self.beta
                pravdepodobnosti.append(feromon * inverzni_vzdalenost)
            else:
                pravdepodobnosti.append(0)
        suma = sum(pravdepodobnosti)
        return [p / suma for p in pravdepodobnosti]

    def najdi_cestu(self):
        # Najde cesty pro všechny mravence.
        for mravenec in range(self.pocet_mravencu):
            self.cesty[mravenec] = [random.randint(0, len(self.hospody) - 1)]
            while len(self.cesty[mravenec]) < len(self.hospody):
                pravdepodobnosti = self.vypocti_pravdepodobnost(mravenec, self.cesty[mravenec][-1])
                dalsi_hospoda = random.choices(range(len(self.hospody)), weights=pravdepodobnosti, k=1)[0]
                self.cesty[mravenec].append(dalsi_hospoda)

    def aktualizuj_feromony(self):
        # Aktualizuje hodnoty feromonů na základě nalezených cest.
        for i in range(len(self.hospody)):
            for j in range(len(self.hospody)):
                self.feromony[i][j] *= (1 - self.odparovani)
        for mravenec in self.cesty:
            vzdalenost_cesty = self.spravce_hospod.vypocti_celkovou_vzdalenost(mravenec)
            for k in range(len(mravenec) - 1):
                self.feromony[mravenec[k]][mravenec[k+1]] += 1 / vzdalenost_cesty

    def solve(self):
        # Spustí algoritmus mravenčí kolonie pro hledání nejlepší cesty.
        for _ in range(self.iterace):
            self.najdi_cestu()
            self.aktualizuj_feromony()
        nejlepsi_cesta = min(self.cesty, key=self.spravce_hospod.vypocti_celkovou_vzdalenost)
        return (
            self.spravce_hospod.dej_informace_o_nejlepsi_cesta(nejlepsi_cesta),
            self.spravce_hospod.vypocti_celkovou_vzdalenost(nejlepsi_cesta),
            'Algoritmus mravenčí kolonie'
        )
