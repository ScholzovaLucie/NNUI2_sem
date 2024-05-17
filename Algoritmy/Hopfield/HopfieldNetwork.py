import numpy as np
from PubsManager.SpravceHospod import vypocti_vzdalenost


# Třída HopfieldovaSíť implementuje samotnou síť
class HopfieldovaSit:
    def __init__(self, spravce_hospod, iterace):
        self.spravce_hospod = spravce_hospod  # Správce hospod obsahující informace o hospodách
        self.velikost = len(spravce_hospod.hospody)  # Počet hospod
        self.iterace = iterace  # Počet iterací pro aktualizaci neuronů
        self.energie = np.zeros((self.velikost, self.velikost))  # Matice energií pro každý pár uzlů
        self.neurony = np.random.uniform(0, 1, (self.velikost, self.velikost))  # Inicializace neuronů náhodnými hodnotami
        self.penal_radek = 500  # Penalizace za aktivaci více neuronů ve stejném řádku
        self.penal_sloupec = 500  # Penalizace za aktivaci více neuronů ve stejném sloupci
        self.penal_vice_mest = 200  # Penalizace za aktivaci více nebo méně neuronů než je měst
        self.penal_vzdalenost = 500  # Penalizace za vzdálenost
        self.step = 1e-6  # Krok pro gradient descent algoritmus, použitý k aktualizaci vah sítě

    # Inicializace matic energií na základě vzdáleností mezi hospodami
    def inicializuj_energie(self):
        for i in range(self.velikost):
            for j in range(self.velikost):
                souradnice1 = self.spravce_hospod.ziskej_souradnice(i)  # Získání souřadnic první hospody
                souradnice2 = self.spravce_hospod.ziskej_souradnice(j)  # Získání souřadnic druhé hospody
                if i != j:
                    self.energie[i, j] = -vypocti_vzdalenost(souradnice1, souradnice2)  # Vypočítání negativní vzdálenosti
                else:
                    self.energie[i, j] = float('inf')  # Nekonečno pro stejnou hospodu

    # Aktualizace stavů neuronů na základě penalizací a energie
    def update(self):
        for _ in range(self.iterace):
            for i in range(self.velikost):
                for j in range(self.velikost):
                    if i != j:
                        u_ij = self.neurony[i, j]  # Aktuální hodnota neuronu
                        delta_u_ij = -self.penal_vzdalenost * self.energie[i, j]  # Penalizace za vzdálenost
                        delta_u_ij += -self.penal_radek * (np.sum(self.neurony[i, :]) - self.neurony[i, j])  # Penalizace pro řádky
                        delta_u_ij += -self.penal_sloupec * (np.sum(self.neurony[:, j]) - self.neurony[i, j])  # Penalizace pro sloupce
                        delta_u_ij += -self.penal_vice_mest * (np.sum(self.neurony) - self.velikost)  # Penalizace za počet aktivací

                        u_ij += self.step * delta_u_ij  # Aktualizace hodnoty neuronu pomocí gradientního sestupu

                        # Skoková aktivační funkce
                        if u_ij >= 0:
                            self.neurony[i, j] = 1
                        else:
                            self.neurony[i, j] = -1

    # Najde nejlepší cestu podle stavů neuronů
    def najdi_nejlepsi_cestu(self):
        cesta = []  # Seznam pro ukládání cesty
        navstiveno = set()  # Množina navštívených hospod
        for i in range(self.velikost):
            max_index = np.argmax(self.neurony[i, :])  # Index neuronu s nejvyšší hodnotou v řádku
            while max_index in navstiveno:  # Pokud již byl navštíven, hledáme další
                self.neurony[i, max_index] = 0  # Vynulovat opakovaně navštívené místo
                max_index = np.argmax(self.neurony[i, :])  # Najít další maximum
            cesta.append(max_index)  # Přidat nalezený index do cesty
            navstiveno.add(max_index)  # Označit jako navštívený
        return cesta  # Vrátit nalezenou cestu

    # Spustí celý výpočetní proces a vrátí nejlepší nalezenou cestu, její délku a název algoritmu
    def solve(self):
        self.inicializuj_energie()  # Inicializace energie
        self.update()  # Aktualizace neuronů
        nejlepsi_cesta = self.najdi_nejlepsi_cestu()  # Nalezení nejlepší cesty
        return (
            self.spravce_hospod.dej_informace_o_nejlepsi_cesta(nejlepsi_cesta),  # Informace o nejlepší cestě
            self.spravce_hospod.vypocti_celkovou_vzdalenost(nejlepsi_cesta),  # Celková vzdálenost cesty
            'Hopfieldova síť'  # Název algoritmu
        )
