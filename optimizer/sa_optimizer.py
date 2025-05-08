import random
import math
import copy
from optimizer.cost_functions import advanced_cost_function

def simulated_annealing(boxes, container, initial_temp=1000, cooling_rate=0.99, stop_T=1, max_iter=10000):
    current_solution = [copy.deepcopy(b) for b in boxes]
    current_cost = advanced_cost_function(current_solution, container)
    best_solution = [copy.deepcopy(b) for b in current_solution]
    best_cost = current_cost

    T = initial_temp
    iteration = 0

    while T > stop_T and iteration < max_iter:
        neighbor = [copy.deepcopy(b) for b in current_solution]
        random.shuffle(neighbor)

        neighbor_cost = advanced_cost_function(neighbor, container)

        delta_cost = neighbor_cost - current_cost

        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / T):
            current_solution = [copy.deepcopy(b) for b in neighbor]
            current_cost = neighbor_cost

            if current_cost < best_cost:
                best_solution = [copy.deepcopy(b) for b in current_solution]
                best_cost = current_cost

        if iteration % 100 == 0:
            print(f"Iteration {iteration}: Current cost = {current_cost}, Best cost = {best_cost}, Temperature = {T}")

        T *= cooling_rate
        iteration += 1

    return best_solution, best_cost
