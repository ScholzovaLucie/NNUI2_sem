import numpy as np

from Hopfield.AnalizaVysledku import AnalizaVysledku


class HopfieldNetwork:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.N = distance_matrix.shape[0]
        self.states = np.random.rand(self.N, self.N) > 0.5  # Inicializace stavy neuronů
        self.analyzer = AnalizaVysledku()  # Přidání analyzátoru

    def compute_energy(self):
        # Energetická funkce TSP
        energy = 0
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    for k in range(self.N):
                        if k != j:
                            energy += self.distance_matrix[i][j] * self.states[i][k] * self.states[k][j]
        return energy

    def update_states(self):
        # Náhodná aktualizace neuronů
        for _ in range(100):  # Počet aktualizací na iteraci
            i, j = np.random.randint(0, self.N, size=2)
            delta_energy = -2 * (self.states[i][j] - 0.5) * sum(
                self.distance_matrix[i][k] * self.states[k][j] for k in range(self.N) if k != j)
            if delta_energy < 0 or np.random.rand() < np.exp(-delta_energy):
                self.states[i][j] = not self.states[i][j]

    def solve(self, iterations):
        for _ in range(iterations):
            self.update_states()
            current_energy = self.compute_energy()
            self.analyzer.record_energy(current_energy)
            print("Energy:", current_energy)
        self.analyzer.plot_energy()
        final_energy = self.compute_energy()
        final_path = self.decode_solution()
        return final_path, final_energy  # Vrátí trasy a energii jako tuple

    def decode_solution(self):
        # Předpokládá, že dekódování bylo úspěšné
        path = np.argmax(self.states, axis=0)
        if np.unique(path).size == self.N:  # Kontrola, zda je řešení validní (každé město je navštíveno jednou)
            return path
        return "Invalid solution (path may not visit each city exactly once)"

    def print_hopfield_results(self, solution, description):
        print(description)
        path, energy = solution
        if isinstance(path, str):
            print(path)  # V případě neplatného řešení
        else:
            print("Optimal path:", path)
        print("Energy of the final state:", energy)
        print("\n")
