import pandas as pd
import os

# Container specification
container = {'width': 18, 'height': 8, 'depth': 8}
container_volume = container['width'] * container['height'] * container['depth']

def load_boxes(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_dict(orient='records')

def compute_volume_utilization(boxes):
    total_volume = sum(b['width'] * b['height'] * b['depth'] for b in boxes)
    return total_volume, (total_volume / container_volume) * 100

def count_boxes_against_walls(boxes):
    return sum(
        1 for b in boxes if (
            b['x'] == 0 or b['y'] == 0 or b['z'] == 0 or
            b['x'] + b['width'] == container['width'] or
            b['y'] + b['height'] == container['height'] or
            b['z'] + b['depth'] == container['depth']
        )
    )

def count_unreasonable_edge_boxes(boxes):
    return sum(
        1 for b in boxes if (
            b['width'] * b['height'] * b['depth'] < 10 and (
                b['x'] == 0 or b['y'] == 0 or
                b['x'] + b['width'] == container['width'] or
                b['y'] + b['height'] == container['height']
            )
        )
    )

def check_fragile_boxes_supported(boxes, threshold=10):
    for box in boxes:
        if box.get('is_fragile', False):
            for other in boxes:
                if other == box:
                    continue
                # Check if other is stacked above this fragile box
                if (other['z'] < box['z'] + box['depth'] and
                    other['z'] >= box['z'] and
                    other['x'] < box['x'] + box['width'] and
                    other['x'] + other['width'] > box['x'] and
                    other['y'] < box['y'] + box['height'] and
                    other['y'] + other['height'] > box['y']):
                    
                    volume = other['width'] * other['height'] * other['depth']
                    if volume >= threshold:
                        return False
    return True

def compute_center_offset(boxes):
    center_x = container['width'] / 2
    center_z = container['depth'] / 2
    offsets = [
        abs((b['x'] + b['width'] / 2) - center_x) + abs((b['z'] + b['depth'] / 2) - center_z)
        for b in boxes
    ]
    return round(sum(offsets) / len(offsets), 2) if offsets else 0.0

def evaluate_solution(path, strategy_name):
    print(f"\nEvaluating: {strategy_name}")
    boxes = load_boxes(path)
    total_vol, util = compute_volume_utilization(boxes)
    result = {
        'Strategy': strategy_name,
        'Container Volume': container_volume,
        'Total Box Volume': total_vol,
        'Space Utilization (%)': round(util, 2),
        'Boxes Against Walls': count_boxes_against_walls(boxes),
        'Unreasonable Edge Boxes': count_unreasonable_edge_boxes(boxes),
        'Fragile Boxes Supported': 'Yes' if check_fragile_boxes_supported(boxes) else 'No',
        'Center Offset': compute_center_offset(boxes)
    }
    for k, v in result.items():
        print(f"{k}: {v}")
    return result

def main():
    output_dir = 'data/results'
    strategies = {
        'Simulated Annealing': os.path.join(output_dir, 'sa_output.csv'),
        'Greedy Heuristic': os.path.join(output_dir, 'greedy_output.csv'),
        'Random Permutation': os.path.join(output_dir, 'random_output.csv'),
        'Baseline': os.path.join(output_dir, 'baseline_output.csv')
    }

    results = []
    for name, path in strategies.items():
        if os.path.exists(path):
            results.append(evaluate_solution(path, name))
        else:
            print(f"[Warning] File not found: {path}")

    # Save all evaluations to one file
    results_df = pd.DataFrame(results)
    results_df.to_csv('data/optimization_comparison.csv', index=False)
    print("\nSaved comparison results to 'data/optimization_comparison.csv'")

if __name__ == '__main__':
    main()