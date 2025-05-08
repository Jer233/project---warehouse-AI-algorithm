import pandas as pd
from optimizer.sa_optimizer import simulated_annealing
from optimizer.box import Box

def main():
    df = pd.read_csv('data/box_placement_data.csv')
    print(f"✅ Total rows in CSV: {len(df)}")
    df['is_fragile'] = df['is_fragile'].fillna(0).astype(int)

    boxes = [Box(
        row['box_id'],
        row['original_width'],
        row['original_height'],
        row['original_depth'],
        row['is_fragile']
    ) for _, row in df.iterrows()]

    print(f"✅ Total boxes created: {len(boxes)}")
    print(f"✅ Box IDs: {[box.box_id for box in boxes]}")

    container = {'width': 50, 'height': 50, 'depth': 50}

    best_solution, best_cost = simulated_annealing(boxes, container)

    print("\nBest order of boxes:")
    records = []
    for box in best_solution:
        print(f"Box ID: {box.box_id}, Unique ID: {box.unique_id}, Position: ({box.x}, {box.y}, {box.z}), Dimensions: ({box.width}, {box.height}, {box.depth})")
        records.append({
            'unique_id': box.unique_id,
            'box_id': box.box_id,
            'x': box.x,
            'y': box.y,
            'z': box.z,
            'width': box.width,
            'height': box.height,
            'depth': box.depth
        })

    pd.DataFrame(records).to_csv('data/optimized_box_data.csv', index=False)
    print("Optimized order saved to 'data/optimized_box_data.csv'.")

if __name__ == "__main__":
    main()
# This script runs the simulated annealing optimizer on a dataset of boxes.
# It reads the box data from a CSV file, applies the optimization algorithm,
# and saves the optimized order back to a new CSV file.