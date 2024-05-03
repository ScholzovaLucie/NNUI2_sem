from matplotlib import pyplot as plt


class AnalizaVysledku:
    def __init__(self, populace, mutace):
        # Inicializace objektu pro analýzu výsledků
        self.vzdalenosti = []  # Seznam pro ukládání vzdáleností v každé generaci
        self.populace = populace  # Velikost populace pro účely analýzy
        self.mutace = mutace  # Pravděpodobnost mutace pro účely analýzy

    def zaznamenej_vysledek(self, vzdalenost):
        # Zaznamenání výsledku pro aktuální generaci
        self.vzdalenosti.append(vzdalenost)

    def vykresli_genetic_graf(self):
        # Vykreslení grafu vývoje vzdálenosti v průběhu generací
        generace = range(1, len(self.vzdalenosti) + 1)

        plt.plot(generace, self.vzdalenosti)
        plt.title(f'Vývoj celkové vzdálenosti v průběhu generací\nPopulace: {self.populace}, Mutace: {self.mutace}')
        plt.xlabel('Generace')
        plt.ylabel('Celková vzdálenost')
        plt.grid(True)  # Přidá mřížku pro lepší čitelnost
        plt.show()
