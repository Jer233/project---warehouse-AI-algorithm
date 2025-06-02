import pandas as pd
import math

# This is for simulated annealing output evaluation
# === CONFIGURATION ===
csv_path = 'data/results/sa_output.csv'
container = {'width': 18, 'height': 8, 'depth': 8}
container_volume = container['width'] * container['height'] * container['depth']

# === LOAD BOXES ===
df = pd.read_csv(csv_path)
boxes = df.to_dict(orient='records')

# === METRIC 1: Space Utilization ===
total_box_volume = sum(b['width'] * b['height'] * b['depth'] for b in boxes)
space_utilization = round((total_box_volume / container_volume) * 100, 2)

# === METRIC 2: Boxes Against Walls ===
def count_boxes_against_walls(boxes, container):
    return sum(
        1 for b in boxes if (
            b['x'] == 0 or b['y'] == 0 or b['z'] == 0 or
            b['x'] + b['width'] == container['width'] or
            b['y'] + b['height'] == container['height'] or
            b['z'] + b['depth'] == container['depth']
        )
    )
boxes_against_walls = count_boxes_against_walls(boxes, container)

# === METRIC 3: Fragile Boxes Supported ===
def fragile_boxes_supported(boxes, threshold_volume=10):
    for fragile in [b for b in boxes if b['is_fragile'] == 1]:
        for other in boxes:
            if other == fragile:
                continue
            # Check if 'other' overlaps spatially on top of 'fragile'
            if (other['y'] == fragile['y'] + fragile['height'] and
                not (other['x'] + other['width'] <= fragile['x'] or other['x'] >= fragile['x'] + fragile['width']) and
                not (other['z'] + other['depth'] <= fragile['z'] or other['z'] >= fragile['z'] + fragile['depth'])):
                vol = other['width'] * other['height'] * other['depth']
                if vol >= threshold_volume:
                    return False
    return True
fragile_supported = fragile_boxes_supported(boxes)

# === METRIC 4: Proportion Supported ===
def proportion_supported(boxes):
    supported_count = 0
    for b in boxes:
        if b['y'] == 0:
            supported_count += 1
            continue
        base_supported = False
        for other in boxes:
            if other == b:
                continue
            if (other['y'] + other['height'] == b['y'] and
                not (other['x'] + other['width'] <= b['x'] or other['x'] >= b['x'] + b['width']) and
                not (other['z'] + other['depth'] <= b['z'] or other['z'] >= b['z'] + b['depth'])):
                base_supported = True
                break
        if base_supported:
            supported_count += 1
    return round((supported_count / len(boxes)) * 100, 2)
proportion_supported = proportion_supported(boxes)


# === METRIC 5: Count Small Boxes on Edges ===
def count_small_boxes_on_edges(boxes, container, volume_threshold=10):
    count = 0
    for box in boxes:
        volume = box['width'] * box['height'] * box['depth']
        if volume < volume_threshold:
            on_edge = (
                box['x'] == 0 or
                box['y'] == 0 or
                box['z'] == 0 or
                box['x'] + box['width'] == container['width'] or
                box['y'] + box['height'] == container['height'] or
                box['z'] + box['depth'] == container['depth']
            )
            if on_edge:
                count += 1
    return count

small_boxes_on_edges = count_small_boxes_on_edges(boxes, container)

# === METRIC 6: Maximum Stack Height ===
max_stack_height = max(b['y'] + b['height'] for b in boxes)

# === METRIC 7: Center Offset ===
def average_center_offset(boxes, container):
    cx, cz = container['width'] / 2, container['depth'] / 2
    total_offset = 0
    for b in boxes:
        bx = b['x'] + b['width'] / 2
        bz = b['z'] + b['depth'] / 2
        offset = math.sqrt((bx - cx)**2 + (bz - cz)**2)
        total_offset += offset
    return round(total_offset / len(boxes), 2)
center_offset = average_center_offset(boxes, container)

# === PRINT REPORT ===
print("==== Evaluation Report ====")
print(f"Space Utilization (%):        {space_utilization}")
print(f"Boxes Against Walls:          {boxes_against_walls}")
print(f"Fragile Boxes Supported:      {'Yes' if fragile_supported else 'No'}")
print(f"Proportion Supported (%):     {proportion_supported}")
print(f"Small Boxes on Edges:         {small_boxes_on_edges}")
print(f"Maximum Stack Height:         {max_stack_height}")
print(f"Average Center Offset:        {center_offset}")

# === SAVE CSV ===
summary_df = pd.DataFrame([{
    'Strategy': 'simulated annealing',
    'Container Volume': container_volume,
    'Total Box Volume': total_box_volume,
    'Space Utilization (%)': space_utilization,
    'Boxes Against Walls': boxes_against_walls,
    'Fragile Boxes Supported': 'Yes' if fragile_supported else 'No',
    'Proportion Supported (%)': proportion_supported,
    'Small Boxes on Edges': small_boxes_on_edges,
    'Maximum Stack Height': max_stack_height,
    'Center Offset': center_offset
}])
summary_df.to_csv('data/sa_evaluation.csv', index=False)
print("✅ Saved summary to data/sa_evaluation.csv")



# This is for baseline output evaluation
# === CONFIGURATION ===
csv_path = 'data/results/baseline_output.csv'
container = {'width': 18, 'height': 8, 'depth': 8}
container_volume = container['width'] * container['height'] * container['depth']

# === LOAD BOXES ===
df = pd.read_csv(csv_path)
boxes = df.to_dict(orient='records')

# === METRIC 1: Space Utilization ===
total_box_volume = sum(b['width'] * b['height'] * b['depth'] for b in boxes)
space_utilization = round((total_box_volume / container_volume) * 100, 2)

# === METRIC 2: Boxes Against Walls ===
def count_boxes_against_walls(boxes, container):
    return sum(
        1 for b in boxes if (
            b['x'] == 0 or b['y'] == 0 or b['z'] == 0 or
            b['x'] + b['width'] == container['width'] or
            b['y'] + b['height'] == container['height'] or
            b['z'] + b['depth'] == container['depth']
        )
    )
boxes_against_walls = count_boxes_against_walls(boxes, container)

# === METRIC 3: Fragile Boxes Supported ===
def fragile_boxes_supported(boxes, threshold_volume=10):
    for fragile in [b for b in boxes if b['is_fragile'] == 1]:
        for other in boxes:
            if other == fragile:
                continue
            # Check if 'other' overlaps spatially on top of 'fragile'
            if (other['y'] == fragile['y'] + fragile['height'] and
                not (other['x'] + other['width'] <= fragile['x'] or other['x'] >= fragile['x'] + fragile['width']) and
                not (other['z'] + other['depth'] <= fragile['z'] or other['z'] >= fragile['z'] + fragile['depth'])):
                vol = other['width'] * other['height'] * other['depth']
                if vol >= threshold_volume:
                    return False
    return True
fragile_supported = fragile_boxes_supported(boxes)

# === METRIC 4: Proportion Supported ===
def proportion_supported(boxes):
    supported_count = 0
    for b in boxes:
        if b['y'] == 0:
            supported_count += 1
            continue
        base_supported = False
        for other in boxes:
            if other == b:
                continue
            if (other['y'] + other['height'] == b['y'] and
                not (other['x'] + other['width'] <= b['x'] or other['x'] >= b['x'] + b['width']) and
                not (other['z'] + other['depth'] <= b['z'] or other['z'] >= b['z'] + b['depth'])):
                base_supported = True
                break
        if base_supported:
            supported_count += 1
    return round((supported_count / len(boxes)) * 100, 2)
proportion_supported = proportion_supported(boxes)


# === METRIC 5: Count Small Boxes on Edges ===
def count_small_boxes_on_edges(boxes, container, volume_threshold=10):
    count = 0
    for box in boxes:
        volume = box['width'] * box['height'] * box['depth']
        if volume < volume_threshold:
            on_edge = (
                box['x'] == 0 or
                box['y'] == 0 or
                box['z'] == 0 or
                box['x'] + box['width'] == container['width'] or
                box['y'] + box['height'] == container['height'] or
                box['z'] + box['depth'] == container['depth']
            )
            if on_edge:
                count += 1
    return count

small_boxes_on_edges = count_small_boxes_on_edges(boxes, container)

# === METRIC 6: Maximum Stack Height ===
max_stack_height = max(b['y'] + b['height'] for b in boxes)

# === METRIC 7: Center Offset ===
def average_center_offset(boxes, container):
    cx, cz = container['width'] / 2, container['depth'] / 2
    total_offset = 0
    for b in boxes:
        bx = b['x'] + b['width'] / 2
        bz = b['z'] + b['depth'] / 2
        offset = math.sqrt((bx - cx)**2 + (bz - cz)**2)
        total_offset += offset
    return round(total_offset / len(boxes), 2)
center_offset = average_center_offset(boxes, container)

# === PRINT REPORT ===
print("==== Evaluation Report ====")
print(f"Space Utilization (%):        {space_utilization}")
print(f"Boxes Against Walls:          {boxes_against_walls}")
print(f"Fragile Boxes Supported:      {'Yes' if fragile_supported else 'No'}")
print(f"Proportion Supported (%):     {proportion_supported}")
print(f"Small Boxes on Edges:         {small_boxes_on_edges}")
print(f"Maximum Stack Height:         {max_stack_height}")
print(f"Average Center Offset:        {center_offset}")

# === SAVE CSV ===
summary_df = pd.DataFrame([{
    'Strategy': 'baseline',
    'Container Volume': container_volume,
    'Total Box Volume': total_box_volume,
    'Space Utilization (%)': space_utilization,
    'Boxes Against Walls': boxes_against_walls,
    'Fragile Boxes Supported': 'Yes' if fragile_supported else 'No',
    'Proportion Supported (%)': proportion_supported,
    'Small Boxes on Edges': small_boxes_on_edges,
    'Maximum Stack Height': max_stack_height,
    'Center Offset': center_offset
}])
summary_df.to_csv('data/baseline_evaluation.csv', index=False)
print("✅ Saved summary to data/baseline_evaluation.csv")


# This is for sgreedy output evaluation
# === CONFIGURATION ===
csv_path = 'data/results/greedy_output.csv'
container = {'width': 18, 'height': 8, 'depth': 8}
container_volume = container['width'] * container['height'] * container['depth']

# === LOAD BOXES ===
df = pd.read_csv(csv_path)
boxes = df.to_dict(orient='records')

# === METRIC 1: Space Utilization ===
total_box_volume = sum(b['width'] * b['height'] * b['depth'] for b in boxes)
space_utilization = round((total_box_volume / container_volume) * 100, 2)

# === METRIC 2: Boxes Against Walls ===
def count_boxes_against_walls(boxes, container):
    return sum(
        1 for b in boxes if (
            b['x'] == 0 or b['y'] == 0 or b['z'] == 0 or
            b['x'] + b['width'] == container['width'] or
            b['y'] + b['height'] == container['height'] or
            b['z'] + b['depth'] == container['depth']
        )
    )
boxes_against_walls = count_boxes_against_walls(boxes, container)

# === METRIC 3: Fragile Boxes Supported ===
def fragile_boxes_supported(boxes, threshold_volume=10):
    for fragile in [b for b in boxes if b['is_fragile'] == 1]:
        for other in boxes:
            if other == fragile:
                continue
            # Check if 'other' overlaps spatially on top of 'fragile'
            if (other['y'] == fragile['y'] + fragile['height'] and
                not (other['x'] + other['width'] <= fragile['x'] or other['x'] >= fragile['x'] + fragile['width']) and
                not (other['z'] + other['depth'] <= fragile['z'] or other['z'] >= fragile['z'] + fragile['depth'])):
                vol = other['width'] * other['height'] * other['depth']
                if vol >= threshold_volume:
                    return False
    return True
fragile_supported = fragile_boxes_supported(boxes)

# === METRIC 4: Proportion Supported ===
def proportion_supported(boxes):
    supported_count = 0
    for b in boxes:
        if b['y'] == 0:
            supported_count += 1
            continue
        base_supported = False
        for other in boxes:
            if other == b:
                continue
            if (other['y'] + other['height'] == b['y'] and
                not (other['x'] + other['width'] <= b['x'] or other['x'] >= b['x'] + b['width']) and
                not (other['z'] + other['depth'] <= b['z'] or other['z'] >= b['z'] + b['depth'])):
                base_supported = True
                break
        if base_supported:
            supported_count += 1
    return round((supported_count / len(boxes)) * 100, 2)
proportion_supported = proportion_supported(boxes)


# === METRIC 5: Count Small Boxes on Edges ===
def count_small_boxes_on_edges(boxes, container, volume_threshold=10):
    count = 0
    for box in boxes:
        volume = box['width'] * box['height'] * box['depth']
        if volume < volume_threshold:
            on_edge = (
                box['x'] == 0 or
                box['y'] == 0 or
                box['z'] == 0 or
                box['x'] + box['width'] == container['width'] or
                box['y'] + box['height'] == container['height'] or
                box['z'] + box['depth'] == container['depth']
            )
            if on_edge:
                count += 1
    return count

small_boxes_on_edges = count_small_boxes_on_edges(boxes, container)

# === METRIC 6: Maximum Stack Height ===
max_stack_height = max(b['y'] + b['height'] for b in boxes)

# === METRIC 7: Center Offset ===
def average_center_offset(boxes, container):
    cx, cz = container['width'] / 2, container['depth'] / 2
    total_offset = 0
    for b in boxes:
        bx = b['x'] + b['width'] / 2
        bz = b['z'] + b['depth'] / 2
        offset = math.sqrt((bx - cx)**2 + (bz - cz)**2)
        total_offset += offset
    return round(total_offset / len(boxes), 2)
center_offset = average_center_offset(boxes, container)

# === PRINT REPORT ===
print("==== Evaluation Report ====")
print(f"Space Utilization (%):        {space_utilization}")
print(f"Boxes Against Walls:          {boxes_against_walls}")
print(f"Fragile Boxes Supported:      {'Yes' if fragile_supported else 'No'}")
print(f"Proportion Supported (%):     {proportion_supported}")
print(f"Small Boxes on Edges:         {small_boxes_on_edges}")
print(f"Maximum Stack Height:         {max_stack_height}")
print(f"Average Center Offset:        {center_offset}")

# === SAVE CSV ===
summary_df = pd.DataFrame([{
    'Strategy': 'greedy evaluation',
    'Container Volume': container_volume,
    'Total Box Volume': total_box_volume,
    'Space Utilization (%)': space_utilization,
    'Boxes Against Walls': boxes_against_walls,
    'Fragile Boxes Supported': 'Yes' if fragile_supported else 'No',
    'Proportion Supported (%)': proportion_supported,
    'Small Boxes on Edges': small_boxes_on_edges,
    'Maximum Stack Height': max_stack_height,
    'Center Offset': center_offset
}])
summary_df.to_csv('data/greedy_evaluation.csv', index=False)
print("✅ Saved summary to data/greedy_evaluation.csv")



# This is for random output evaluation
# === CONFIGURATION ===
csv_path = 'data/results/random_output.csv'
container = {'width': 18, 'height': 8, 'depth': 8}
container_volume = container['width'] * container['height'] * container['depth']

# === LOAD BOXES ===
df = pd.read_csv(csv_path)
boxes = df.to_dict(orient='records')

# === METRIC 1: Space Utilization ===
total_box_volume = sum(b['width'] * b['height'] * b['depth'] for b in boxes)
space_utilization = round((total_box_volume / container_volume) * 100, 2)

# === METRIC 2: Boxes Against Walls ===
def count_boxes_against_walls(boxes, container):
    return sum(
        1 for b in boxes if (
            b['x'] == 0 or b['y'] == 0 or b['z'] == 0 or
            b['x'] + b['width'] == container['width'] or
            b['y'] + b['height'] == container['height'] or
            b['z'] + b['depth'] == container['depth']
        )
    )
boxes_against_walls = count_boxes_against_walls(boxes, container)

# === METRIC 3: Fragile Boxes Supported ===
def fragile_boxes_supported(boxes, threshold_volume=10):
    for fragile in [b for b in boxes if b['is_fragile'] == 1]:
        for other in boxes:
            if other == fragile:
                continue
            # Check if 'other' overlaps spatially on top of 'fragile'
            if (other['y'] == fragile['y'] + fragile['height'] and
                not (other['x'] + other['width'] <= fragile['x'] or other['x'] >= fragile['x'] + fragile['width']) and
                not (other['z'] + other['depth'] <= fragile['z'] or other['z'] >= fragile['z'] + fragile['depth'])):
                vol = other['width'] * other['height'] * other['depth']
                if vol >= threshold_volume:
                    return False
    return True
fragile_supported = fragile_boxes_supported(boxes)

# === METRIC 4: Proportion Supported ===
def proportion_supported(boxes):
    supported_count = 0
    for b in boxes:
        if b['y'] == 0:
            supported_count += 1
            continue
        base_supported = False
        for other in boxes:
            if other == b:
                continue
            if (other['y'] + other['height'] == b['y'] and
                not (other['x'] + other['width'] <= b['x'] or other['x'] >= b['x'] + b['width']) and
                not (other['z'] + other['depth'] <= b['z'] or other['z'] >= b['z'] + b['depth'])):
                base_supported = True
                break
        if base_supported:
            supported_count += 1
    return round((supported_count / len(boxes)) * 100, 2)
proportion_supported = proportion_supported(boxes)


# === METRIC 5: Count Small Boxes on Edges ===
def count_small_boxes_on_edges(boxes, container, volume_threshold=10):
    count = 0
    for box in boxes:
        volume = box['width'] * box['height'] * box['depth']
        if volume < volume_threshold:
            on_edge = (
                box['x'] == 0 or
                box['y'] == 0 or
                box['z'] == 0 or
                box['x'] + box['width'] == container['width'] or
                box['y'] + box['height'] == container['height'] or
                box['z'] + box['depth'] == container['depth']
            )
            if on_edge:
                count += 1
    return count

small_boxes_on_edges = count_small_boxes_on_edges(boxes, container)

# === METRIC 6: Maximum Stack Height ===
max_stack_height = max(b['y'] + b['height'] for b in boxes)

# === METRIC 7: Center Offset ===
def average_center_offset(boxes, container):
    cx, cz = container['width'] / 2, container['depth'] / 2
    total_offset = 0
    for b in boxes:
        bx = b['x'] + b['width'] / 2
        bz = b['z'] + b['depth'] / 2
        offset = math.sqrt((bx - cx)**2 + (bz - cz)**2)
        total_offset += offset
    return round(total_offset / len(boxes), 2)
center_offset = average_center_offset(boxes, container)

# === PRINT REPORT ===
print("==== Evaluation Report ====")
print(f"Space Utilization (%):        {space_utilization}")
print(f"Boxes Against Walls:          {boxes_against_walls}")
print(f"Fragile Boxes Supported:      {'Yes' if fragile_supported else 'No'}")
print(f"Proportion Supported (%):     {proportion_supported}")
print(f"Small Boxes on Edges:         {small_boxes_on_edges}")
print(f"Maximum Stack Height:         {max_stack_height}")
print(f"Average Center Offset:        {center_offset}")

# === SAVE CSV ===
summary_df = pd.DataFrame([{
    'Strategy': 'random evaluation',
    'Container Volume': container_volume,
    'Total Box Volume': total_box_volume,
    'Space Utilization (%)': space_utilization,
    'Boxes Against Walls': boxes_against_walls,
    'Fragile Boxes Supported': 'Yes' if fragile_supported else 'No',
    'Proportion Supported (%)': proportion_supported,
    'Small Boxes on Edges': small_boxes_on_edges,
    'Maximum Stack Height': max_stack_height,
    'Center Offset': center_offset
}])
summary_df.to_csv('data/random_evaluation.csv', index=False)
print("✅ Saved summary to data/random_evaluation.csv")