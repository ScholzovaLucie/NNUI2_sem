from matplotlib import pyplot as plt


class AnalizaVysledku:
    def __init__(self, populace, mutace):
        self.vzdalenosti = []
        self.populace = populace
        self.mutace = mutace

    def zaznamenej_vysledek(self, vzdalenost):
        self.vzdalenosti.append(vzdalenost)

    def vykresli_graf(self):
        generace = range(1, len(self.vzdalenosti) + 1)
        plt.figure(figsize=(10, 5))  # Nastavení velikosti grafu
        plt.plot(generace, self.vzdalenosti, label='Vzdálenost')

        # Najít minimum a jeho index
        min_vzdalenost = min(self.vzdalenosti)
        min_index = self.vzdalenosti.index(min_vzdalenost) + 1  # +1 protože indexace generací začíná od 1

        # Zvýraznit minimum
        plt.scatter(min_index, min_vzdalenost, color='red')  # Zvýraznění bodu
        plt.text(min_index, min_vzdalenost, f' Min: {min_vzdalenost}', color='red', verticalalignment='bottom')

        plt.title(f'Vývoj celkové vzdálenosti v průběhu generací\nPopulace: {self.populace}, Mutace: {self.mutace}')
        plt.xlabel('Generace')
        plt.ylabel('Celková vzdálenost')
        plt.legend()
        plt.grid(True)
        plt.show()