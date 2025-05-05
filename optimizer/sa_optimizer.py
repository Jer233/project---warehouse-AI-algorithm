import random
import math
from optimizer.cost_functions import volumn_priority_cost

def simulated_annealing(df, T=1000, cooling=0.98, stop_T=1):
    current = df['box_id'].tolist()
    current_cost = volumn_priority_cost(current, df)
    best = current[:]
    best_cost = current_cost

    while T > stop_T:
        new = current[:]
        i, j = random.sample(range(len(new)), 2)
        new[i], new[j] = new[j], new[i]
        new_cost = volumn_priority_cost(new, df)

        if new_cost < current_cost:
            current = new[:]
            current_cost = new_cost
            if new_cost < best_cost:
                best = new[:]
                best_cost = new_cost
        else:
            prob = math.exp((current_cost - new_cost) / T)
            if random.random() < prob:
                current = new[:]
                current_cost = new_cost

        T *= cooling
        
    return best, best_cost