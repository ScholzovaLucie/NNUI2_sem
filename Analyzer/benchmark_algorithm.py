import time

from PubsManager.SpravceHospod import print_solution


def benchmark_algorithm(algorithm, *args, **kwargs):
    # Funkce změří dobu běhu algoritmu a vypíše výsledky.
    start_time = time.time()  # Začátek měření
    algorithm_result = algorithm(*args, **kwargs)  # Spuštění algoritmu s argumenty
    result = algorithm_result.solve()  # Získání výsledku
    end_time = time.time()  # Konec měření
    execution_time = end_time - start_time  # Celková doba běhu
    print_solution(result[0], result[1], result[2])  # Výpis výsledků
    return algorithm_result, result, execution_time  # Vrátí výsledky a čas
