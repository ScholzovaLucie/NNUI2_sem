from matplotlib import pyplot as plt


class AnalizaVysledku:
    def __init__(self):
        self.energies = []  # Seznam pro ukládání energií v každé iteraci

    def record_energy(self, energy):
        # Zaznamenání energie pro aktuální iteraci
        self.energies.append(energy)

    def plot_energy(self):
        # Vykreslení grafu vývoje energie
        iterations = range(1, len(self.energies) + 1)
        plt.figure(figsize=(10, 5))
        plt.plot(iterations, self.energies, label='Energie')
        plt.title('Vývoj energie Hopfieldovy sítě')
        plt.xlabel('Iterace')
        plt.ylabel('Energie')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Zvýraznění minima
        if self.energies:
            min_energy = min(self.energies)
            min_index = self.energies.index(min_energy) + 1
            plt.scatter(min_index, min_energy, color='red')
            plt.text(min_index, min_energy, f' Min: {min_energy}', color='red', verticalalignment='bottom')

        plt.show()