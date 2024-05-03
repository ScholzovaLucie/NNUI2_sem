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
        plt.plot(generace, self.vzdalenosti)
        plt.title(f'Vývoj celkové vzdálenosti v průběhu generací\nPopulace: {self.populace}, Mutace: {self.mutace}')
        plt.xlabel('Generace')
        plt.ylabel('Celková vzdálenost')
        plt.grid(True)
        plt.show()