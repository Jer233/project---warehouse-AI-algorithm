import pandas as pd
from optimizer.sa_optimizer import simulated_annealing

def main():
    df = pd.read_csv('data/box_placement_data.csv')
    best_order, best_cost = simulated_annealing(df)

    print("Best order of boxes:", best_order)
    print("Best cost:", best_cost)

    df['optimized_order'] = best_order
    for idx, box_id in enumerate(best_order):
        df.loc[df['box_id'] == box_id, 'optimized_order'] = idx + 1
    df.to_csv('data/optimized_box_data.csv', index=False)


if __name__ == "__main__":
    main()
# This script runs the simulated annealing optimizer on a dataset of boxes.
# It reads the box data from a CSV file, applies the optimization algorithm,
# and saves the optimized order back to a new CSV file.