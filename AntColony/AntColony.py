import numpy as np

from AntColony.AnalyzaVysledku import AnalizaVysledku


class AntColony:
    def __init__(self, pubs_data, num_ants, num_iterations, alpha, beta, evaporation_rate):
        self.pubs_data = pubs_data
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.coords = [pub['koordináty'] for pub in pubs_data]
        self.dist_matrix = self.calculate_distance_matrix(self.coords)
        self.pheromone_matrix = np.ones((len(self.coords), len(self.coords)))
        self.analyzer = AnalizaVysledku(populace=num_ants, mutace=evaporation_rate)  # Instance analyzátoru

    def calculate_distance_matrix(self, coords):
        """Vypočítá matici Euklidovských vzdáleností mezi body."""
        num_locations = len(coords)
        dist_matrix = np.zeros((num_locations, num_locations))
        for i in range(num_locations):
            for j in range(i + 1, num_locations):
                dist = np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))
                dist_matrix[i][j] = dist
                dist_matrix[j][i] = dist
        return dist_matrix

    def run(self):
        best_tour = None
        best_distance = float('inf')

        for iteration in range(self.num_iterations):
            tours = []
            distances = []
            for _ in range(self.num_ants):
                tour = [np.random.randint(0, len(self.coords))]
                for _ in range(len(self.coords) - 1):
                    current = tour[-1]
                    probabilities = self.pheromone_matrix[current] ** self.alpha * (1.0 / (self.dist_matrix[current] + 1e-10)) ** self.beta
                    probabilities[tour] = 0  # exclude already visited
                    next_city = np.random.choice(len(self.coords), p=probabilities / probabilities.sum())
                    tour.append(next_city)
                tour.append(tour[0])
                total_distance = sum(self.dist_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))
                tours.append(tour)
                distances.append(total_distance)
                if total_distance < best_distance:
                    best_distance = total_distance
                    best_tour = tour
            self.analyzer.zaznamenej_vysledek(best_distance)

            self.update_pheromones(tours, distances)

        self.analyzer.vykresli_graf()  # Vykreslení grafu po dokončení simulace
        return best_tour, best_distance

    def update_pheromones(self, tours, distances):
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        for tour, dist in zip(tours, distances):
            for i in range(len(tour) - 1):
                self.pheromone_matrix[tour[i]][tour[i+1]] += 1.0 / dist

    def print_ant_colony_results(self, path, distance, description):
        print(description)
        print("Best tour found by ants:", path)
        print("Total distance of the tour:", distance)
        print("\n")
