import numpy as np
import time


class HopfieldNetwork:
    def __init__(self, distance_matrix):
        self.N = len(distance_matrix)
        self.distance_matrix = distance_matrix
        self.neurons = np.random.rand(self.N, self.N)

    def energy(self):
        E = 0
        for i in range(self.N):
            E += (np.sum(self.neurons[i, :]) - 1) ** 2 + (np.sum(self.neurons[:, i]) - 1) ** 2
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    for k in range(self.N):
                        if k != i:
                            E += self.distance_matrix[i, k] * self.neurons[i, j] * self.neurons[j, k]
        return E

    def update_neurons(self):
        for i in range(self.N):
            for j in range(self.N):
                total_input = 0
                for k in range(self.N):
                    if k != i:
                        total_input += self.distance_matrix[i, k] * self.neurons[k, (j + 1) % self.N]
                self.neurons[i, j] = 1 / (1 + np.exp(-total_input))

    def solve(self, iterations=100):
        for _ in range(iterations):
            self.update_neurons()
        return self.neurons


def nearest_neighbor(distance_matrix):
    N = len(distance_matrix)
    start = 0
    visited = set([start])
    tour = [start]
    cost = 0

    while len(visited) < N:
        last = tour[-1]
        next_city = min([(distance_matrix[last][j], j) for j in range(N) if j not in visited], key=lambda x: x[0])
        cost += next_city[0]
        tour.append(next_city[1])
        visited.add(next_city[1])

    cost += distance_matrix[tour[-1]][tour[0]]
    tour.append(tour[0])
    return tour, cost

