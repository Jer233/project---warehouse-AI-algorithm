import pandas as pd
import time
from optimizer.sa_optimizer import simulated_annealing
from optimizer.box import Box

def main():
    df = pd.read_csv('data/box_placement_data.csv')
    df['is_fragile'] = df['is_fragile'].fillna(0).astype(int)

    boxes = [Box(
        row['box_id'],
        row['original_width'],
        row['original_height'],
        row['original_depth'],
        row['is_fragile']
    ) for _, row in df.iterrows()]

    container = {'width': 20, 'height': 15, 'depth': 20}

    best_overall = None
    best_cost = float('inf')
    total_runs = 10

    for i in range(total_runs):
        print(f"▶ Run {i+1}/{total_runs}")
        run_boxes = [b.copy() for b in boxes]
        solution, cost = simulated_annealing(run_boxes, container)
        if cost < best_cost:
            best_cost = cost
            best_overall = [b.copy() for b in solution]

    print("\n Best Cost:", best_cost)
    records = []
    for idx, box in enumerate(best_overall):
        records.append({
            'placement_order': idx+1,
            'box_id': box.box_id,
            'x': box.x,
            'y': box.y,
            'z': box.z,
            'width': box.width,
            'height': box.height,
            'depth': box.depth
            
        })

    pd.DataFrame(records).to_csv('data/optimized_box_data.csv', index=False)
    print("Saved to 'data/optimized_box_data.csv'")

if __name__ == "__main__":
    main()
