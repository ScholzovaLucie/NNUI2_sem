from AntColony.AntColony import AntColony
from Genetic.GeneticAlgorithm import GenetickyAlgoritmus
from Hopfield.HopfieldNetwork import HopfieldNetwork
from Loader.DataLoader import DataLoader
from PubsManager.SpravceHospod import SpravceHospod
import openpyxl


def load_data(file_name):
    data_loader = DataLoader(file_name)
    return data_loader.format_data_for_algorithm()


def create_distance_matrix(pubs_data):
    spravce_hospod = SpravceHospod(pubs_data)
    return spravce_hospod.create_distance_matrix(pubs_data)


def run_hopfield_network(distance_matrix):
    iterations = 10
    network = HopfieldNetwork(distance_matrix)
    hopfield_solution = network.solve(iterations)
    network.print_hopfield_results(hopfield_solution, "Výsledky Hopfieldovy sítě:")


def run_genetic_algorithm(pubs_data, spravce_hospod):
    geneticky_algoritmus = GenetickyAlgoritmus(
        pubs_data,
        spravce_hospod,
        velikost_populace=1000,
        generace=500,
        mutace_pravdepodobnost=0.1
    )
    nejlepsi_cesta, celkova_vzdalenost = geneticky_algoritmus.geneticky_algoritmus()
    geneticky_algoritmus.print_genetic_results(nejlepsi_cesta, celkova_vzdalenost, "Výsledky genetického algoritmu:")


def run_ant_colony(pubs_data):
    colony = AntColony(pubs_data, num_ants=5, num_iterations=20, alpha=1, beta=2, evaporation_rate=0.5)
    best_tour, best_distance = colony.run()
    colony.print_ant_colony_results(best_tour, best_distance, "Výsledky algoritmu mravenčí kolonie:")


def main():
    file_name = "Pubs.xlsx"
    pubs_data = load_data(file_name)
    spravce_hospod = SpravceHospod(pubs_data)
    distance_matrix = create_distance_matrix(pubs_data)

    # Spuštění algoritmů
    run_hopfield_network(distance_matrix)
    run_genetic_algorithm(pubs_data, spravce_hospod)
    run_ant_colony(pubs_data)


if __name__ == '__main__':
    main()
