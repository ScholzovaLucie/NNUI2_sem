import matplotlib.pyplot as plt
from Algoritmy.Hopfield.HopfieldNetwork import HopfieldovaSit
from Algoritmy.Genetic.GeneticAlgorithm import GenetickyAlgoritmus
from Algoritmy.AntColony.AntColony import MravenciAlgoritmus
from Loader.DataLoader import DataLoader
from PubsManager.SpravceHospod import SpravceHospod
from benchmark_algorithm import benchmark_algorithm


class AlgorithmAnalyzer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data_loader = DataLoader(file_name)
        self.pubs_data = self.data_loader.format_data_for_algorithm()
        self.pubs_manager = SpravceHospod(self.pubs_data)
        self.distance_matrix = self.pubs_manager.create_distance_matrix(self.pubs_data)

    def analyze_algorithms(self):
        # Spustí benchmarking pro všechny algoritmy
        results = {
            "hopfield": benchmark_algorithm(
                HopfieldovaSit,  self.pubs_manager,
                velikost=len(self.pubs_manager.hospody), iterace=1000
            ),
            "genetic": benchmark_algorithm(
                GenetickyAlgoritmus, self.pubs_data, self.pubs_manager,
                velikost_populace=1000, generace=500, mutace_pravdepodobnost=0.1
            ),
            "ant_colony": benchmark_algorithm(
                MravenciAlgoritmus, self.pubs_data, self.pubs_manager,
                pocet_mravencu=500, iterace=1000, alfa=1, beta=2, odparovani=0.5
            )
        }
        return results

    def plot_comparison(self, results):
        algorithms = list(results.keys())  # Získání jmen algoritmů
        times = [result[1] for result in results.values()[1]]  # Získání časů pro porovnání
        plt.bar(algorithms, times, color=['blue', 'green', 'red'])
        plt.ylabel('Execution Time (s)')
        plt.title('Algorithm Performance Comparison')
        plt.show()

    def run(self):
        results = self.analyze_algorithms()
        self.plot_comparison(results)
        self.analyze_results(results)

    def compare_lengths(self, results):
        algorithms = list(results.keys())
        lengths = [result[0] for result in results.values()[1]]

        # Vykreslení histogramu délek tras
        plt.figure(figsize=(10, 6))
        plt.bar(algorithms, lengths, color=['blue', 'green', 'red'])
        plt.ylabel('Total Distance')
        plt.title('Comparison of Total Distance')
        plt.show()

    def compare_times(self, results):
        algorithms = list(results.keys())
        times = [result[1] for result in results.values()[2]]

        # Vykreslení histogramu časů algoritmů
        plt.figure(figsize=(10, 6))
        plt.bar(algorithms, times, color=['blue', 'green', 'red'])
        plt.ylabel('Execution Time (s)')
        plt.title('Comparison of Execution Time')
        plt.show()

    def analyze_results(self, results):
        # Analyzuj výsledky a vykresli grafy
        self.compare_lengths(results)
        self.compare_times(results)
