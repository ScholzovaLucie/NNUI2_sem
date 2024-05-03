import time


def benchmark_algorithm(algorithm, *args, **kwargs):
    start_time = time.time()
    algorithm_result = algorithm(*args, **kwargs)
    result = algorithm_result.solve()
    end_time = time.time()
    execution_time = end_time - start_time
    algorithm_result.spravce_hospod.print_solution(result[0], result[1], result[2])
    return algorithm_result, result, execution_time
