from AntColony.AntColony import AntColony
from Genetic.GeneticAlgorithm import GenetickyAlgoritmus
from Loader.DataLoader import DataLoader
from PubsManager.SpravceHospod import SpravceHospod
import openpyxl


def main():
    # Nastavení názvu souboru
    file_name = "Pubs.xlsx"

    # Načtení dat a formátování pro algoritmus
    data_loader = DataLoader(file_name)
    pubs_data = data_loader.format_data_for_algorithm()

    spravce_hospod = SpravceHospod(pubs_data)

    # Inicializace genetického algoritmu
    geneticky_algoritmus = GenetickyAlgoritmus(
        pubs_data,
        spravce_hospod,
        velikost_populace=1000,
        generace=500,
        mutace_pravdepodobnost=0.1
    )

    # Spuštění genetického algoritmu
    nejlepsi_cesta, celkova_vzdalenost = geneticky_algoritmus.geneticky_algoritmus()

    # Výpis výsledků
    print_results(nejlepsi_cesta, celkova_vzdalenost)

    colony = AntColony(pubs_data, num_ants=5, num_iterations=20, alpha=1, beta=2, evaporation_rate=0.5)
    best_tour, best_distance = colony.run()
    # Výpis výsledků
    print_results(best_tour, best_distance)


def print_results(nejlepsi_cesta, celkova_vzdalenost):
    # Výpis nejlepšího pořadí hospod a celkové uražené vzdálenosti
    print("Nejlepší pořadí návštěvy hospod:")

    for hospoda in nejlepsi_cesta:
        print(f"{hospoda['id']}. {hospoda['název']}")

    print("Celková uražená vzdálenost:", celkova_vzdalenost)


if __name__ == '__main__':
    # Volání hlavní funkce
    main()
