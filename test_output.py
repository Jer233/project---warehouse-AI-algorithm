import pandas as pd

# Load the output file
csv_path = 'data/optimized_box_data.csv'
# csv_path = 'data/box_original_data.csv'  # Replace if needed
df = pd.read_csv(csv_path)

# Container spec
container = {'width': 20, 'height': 15, 'depth': 20}
container_volume = container['width'] * container['height'] * container['depth']

# Convert to list
boxes = df.to_dict(orient='records')

# Total used volume
total_box_volume = sum(box['width'] * box['height'] * box['depth'] for box in boxes)
space_utilization = (total_box_volume / container_volume) * 100

# Boxes against wall
def count_boxes_against_walls(boxes, container):
    return sum(
        1 for box in boxes if (
            box['x'] == 0 or box['y'] == 0 or box['z'] == 0 or
            box['x'] + box['width'] == container['width'] or
            box['y'] + box['height'] == container['height'] or
            box['z'] + box['depth'] == container['depth']
        )
    )

# Unreasonable small boxes at edges
def count_unreasonable_edge_boxes(boxes):
    return sum(
        1 for box in boxes
        if (box['width'] * box['height'] * box['depth'] < 10 and
            (box['x'] == 0 or box['y'] == 0 or
             box['x'] + box['width'] == container['width'] or
             box['y'] + box['height'] == container['height']))
    )

# Fragile box stacking check
def check_fragile_boxes_supported(boxes, small_volume_threshold=10):
    for box in boxes:
        if box.get('is_fragile', False):
            for other in boxes:
                if other == box:
                    continue
                if (other['z'] < box['z'] + box['depth'] and
                    other['z'] >= box['z'] and
                    other['x'] < box['x'] + box['width'] and
                    other['x'] + other['width'] > box['x'] and
                    other['y'] < box['y'] + box['height'] and
                    other['y'] + other['height'] > box['y']):

                    # 允许小箱子放在 fragile 上面
                    volume = other['width'] * other['height'] * other['depth']
                    if volume >= small_volume_threshold:
                        return False
    return True


# Run checks
boxes_against_walls = count_boxes_against_walls(boxes, container)
unreasonable_edge_boxes = count_unreasonable_edge_boxes(boxes)
fragile_supported = check_fragile_boxes_supported(boxes)

# Print results
print("\n--- Optimization Evaluation ---")
print(f"Container Volume: {container_volume}")
print(f"Total Box Volume: {total_box_volume}")
print(f"Space Utilization: {space_utilization:.2f}%")
print(f"Boxes Against Walls: {boxes_against_walls}")
print(f"Unreasonable Edge Boxes: {unreasonable_edge_boxes}")
print(f"Fragile Boxes Supported: {'Yes' if fragile_supported else 'No'}")

# Save results
results_df = pd.DataFrame([{
    'Container Volume': container_volume,
    'Total Box Volume': total_box_volume,
    'Space Utilization (%)': round(space_utilization, 2),
    'Boxes Against Walls': boxes_against_walls,
    'Unreasonable Edge Boxes': unreasonable_edge_boxes,
    'Fragile Boxes Supported': 'Yes' if fragile_supported else 'No'
}])

results_df.to_csv('data/optimization_results.csv', index=False)
print("Results saved to 'data/optimization_results.csv'")
