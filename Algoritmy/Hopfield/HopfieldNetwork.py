import numpy as np

from PubsManager.SpravceHospod import vypocti_vzdalenost


class HopfieldovaSit:
    def __init__(self, spravce_hospod, velikost, iterace):
        # Konstruktor inicializuje Hopfieldovu síť s daným správcem hospod, počtem uzlů (hospod)
        # a počtem iterací pro aktualizaci.
        self.spravce_hospod = spravce_hospod
        self.velikost = velikost
        self.iterace = iterace
        self.energie = np.zeros((velikost, velikost))  # Matice energií pro každý pár uzlů

    def inicializuj_energie(self):
        # Inicializuje matrici energií negativními vzdálenostmi mezi hospodami, kromě diagonály,
        # kde je energie nekonečno.
        for i in range(self.velikost):
            for j in range(self.velikost):
                souradnice1 = self.spravce_hospod.ziskej_souradnice(i)
                souradnice2 = self.spravce_hospod.ziskej_souradnice(j)
                if i != j:
                    self.energie[i, j] = -vypocti_vzdalenost(souradnice1, souradnice2)
                else:
                    self.energie[i, j] = float('inf')

    def update(self):
        # Náhodně aktualizuje energie pro simulaci dynamiky Hopfieldovy sítě.
        for _ in range(self.iterace):
            i, j = np.random.randint(0, self.velikost), np.random.randint(0, self.velikost)
            delta_energie = -2 * self.energie[i, j]
            if delta_energie < 0:
                self.energie[i] = np.roll(self.energie[i], 1)

    def najdi_nejlepsi_cestu(self):
        # Najde cestu s nejnižší celkovou energií, což naznačuje optimální trasu mezi hospodami.
        index_min_energie = np.argmin(np.sum(self.energie, axis=0))
        cesta = np.roll(np.arange(self.velikost), -index_min_energie)
        return cesta

    def solve(self):
        # Spustí celý výpočetní proces a vrátí nejlepší nalezenou cestu, její délku a název algoritmu.
        self.inicializuj_energie()
        self.update()
        nejlepsi_cesta = self.najdi_nejlepsi_cestu()
        return (
            self.spravce_hospod.dej_informace_o_nejlepsi_cesta(nejlepsi_cesta),
            self.spravce_hospod.vypocti_celkovou_vzdalenost(nejlepsi_cesta),
            'Hopfieldova síť'
        )
