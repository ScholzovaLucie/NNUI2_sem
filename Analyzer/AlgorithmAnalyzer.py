import matplotlib.pyplot as plt
from Algoritmy.Hopfield.HopfieldNetwork import HopfieldovaSit
from Algoritmy.Genetic.GeneticAlgorithm import GenetickyAlgoritmus
from Algoritmy.AntColony.AntColony import MravenciAlgoritmus
from Loader.DataLoader import DataLoader
from PubsManager.SpravceHospod import SpravceHospod, create_distance_matrix
from benchmark_algorithm import benchmark_algorithm


def compare_lengths(results):
    # Vykreslí sloupcový graf porovnávající celkové vzdálenosti pro každý algoritmus
    algorithms = list(results.keys())  # Názvy algoritmů
    lengths = [result[1][1] for result in results.values()]  # Celkové vzdálenosti
    plt.figure(figsize=(10, 6))
    plt.bar(algorithms, lengths, color=['blue', 'green', 'red'])
    plt.ylabel('Celková vzdálenost')
    plt.title('Srovnání celkové vzdálenosti')
    plt.show()


def plot_comparison(results):
    # Vykreslí sloupcový graf porovnávající dobu běhu pro každý algoritmus
    algorithms = list(results.keys())
    times = [result[2] for result in results.values()]  # Doby běhu algoritmů
    plt.bar(algorithms, times, color=['blue', 'green', 'red'])
    plt.ylabel('Doba provedení (s)')
    plt.title('Srovnání výkonnosti algoritmů')
    plt.show()


class AlgorithmAnalyzer:
    def __init__(self, file_name):
        # Inicializace datových zdrojů a správce hospod
        self.file_name = file_name
        self.data_loader = DataLoader(file_name)
        self.pubs_data = self.data_loader.format_data_for_algorithm()
        self.pubs_manager = SpravceHospod(self.pubs_data)
        self.distance_matrix = create_distance_matrix(self.pubs_data)

    def analyze_algorithms(self):
        # Porovnává algoritmy pomocí funkce benchmark_algorithm a ukládá výsledky
        results = {
            "hopfield": benchmark_algorithm(
                HopfieldovaSit, self.pubs_manager, velikost=len(self.pubs_manager.hospody), iterace=100
            ),
            "genetic": benchmark_algorithm(
                GenetickyAlgoritmus, self.pubs_data, self.pubs_manager, velikost_populace=100, generace=500, mutace_pravdepodobnost=0.1
            ),
            "ant_colony": benchmark_algorithm(
                MravenciAlgoritmus, self.pubs_data, self.pubs_manager, pocet_mravencu=500, iterace=100, alfa=1, beta=2, odparovani=0.5
            )
        }
        return results

    def run(self):
        # Spustí analýzu a vykreslí výsledky
        results = self.analyze_algorithms()
        plot_comparison(results)
        compare_lengths(results)