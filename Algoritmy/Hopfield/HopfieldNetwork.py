import numpy as np

from PubsManager.SpravceHospod import vypocti_vzdalenost


class HopfieldovaSit:
    def __init__(self, spravce_hospod, velikost, iterace):
        self.spravce_hospod = spravce_hospod
        self.velikost = velikost
        self.iterace = iterace
        self.energie = np.zeros((velikost, velikost))

    def inicializuj_energie(self):
        for i in range(self.velikost):
            for j in range(self.velikost):
                souradnice1 = self.spravce_hospod.ziskej_souradnice(i)
                souradnice2 = self.spravce_hospod.ziskej_souradnice(j)
                if i != j:
                    self.energie[i, j] = -vypocti_vzdalenost(souradnice1, souradnice2)
                else:
                    self.energie[i, j] = float('inf')  # zakážeme město navštívit samo sebe

    def update(self):
        # Iterujeme skrz síť a updatujeme podle Hopfieldova pravidla
        for _ in range(self.iterace):  # počet iterací updatu
            i, j = np.random.randint(0, self.velikost), np.random.randint(0, self.velikost)
            delta_energie = -2 * self.energie[i, j]
            if delta_energie < 0:  # změna snižuje energii, tedy je přijata
                self.energie[i] = np.roll(self.energie[i], 1)  # posun řádku pro změnu cesty

    def najdi_nejlepsi_cestu(self):
        min_energie = np.min(np.sum(self.energie, axis=0))
        index_min_energie = np.argmin(np.sum(self.energie, axis=0))
        cesta = np.roll(np.arange(self.velikost), -index_min_energie)
        return cesta

    def solve(self):
        self.inicializuj_energie()
        self.update()
        nejlepsi_cesta = self.najdi_nejlepsi_cestu()
        return (
            self.spravce_hospod.dej_informace_o_nejlepsi_cesta(nejlepsi_cesta),
            self.spravce_hospod.vypocti_celkovou_vzdalenost(nejlepsi_cesta),
            'Hopfieldova síť'
        )
