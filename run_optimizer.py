import pandas as pd
from optimizer.sa_optimizer import simulated_annealing
from optimizer.box import Box

def main():
    df = pd.read_csv('data/box_placement_data.csv')
    df['is_fragile'] = df['is_fragile'].fillna(0).astype(int)

    boxes = [
        Box(row['box_id'], row['original_width'], row['original_height'], row['original_depth'], row['is_fragile'])
        for _, row in df.iterrows()
    ]

    container = {'width': 50, 'height': 50, 'depth': 50}

    best_solution, best_cost = simulated_annealing(boxes, container)

    print("\nBest order of boxes:")
    for box in best_solution:
        print(f"Box(id={box.box_id}, x={box.x}, y={box.y}, z={box.z}, w={box.width}, h={box.height}, d={box.depth})")

    # Remove duplicates by box_id (keep first occurrence)
    seen_ids = set()
    records = []
    for box in best_solution:
        if box.box_id not in seen_ids:
            records.append({
                'box_id': box.box_id,
                'x': box.x,
                'y': box.y,
                'z': box.z,
                'width': box.width,
                'height': box.height,
                'depth': box.depth
            })
            seen_ids.add(box.box_id)

    pd.DataFrame(records).to_csv('data/optimized_box_data.csv', index=False)
    print("Optimized order saved to 'data/optimized_box_data.csv'.")

if __name__ == "__main__":
    main()
# This script runs the simulated annealing optimizer on a dataset of boxes.
# It reads the box data from a CSV file, applies the optimization algorithm,
# and saves the optimized order back to a new CSV file.