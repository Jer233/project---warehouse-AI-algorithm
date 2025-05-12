import math

def overlap(box1, box2):
    return not (box1.x + box1.width <= box2.x or
                box2.x + box2.width <= box1.x or
                box1.y + box1.height <= box2.y or
                box2.y + box2.height <= box1.y or
                box1.z + box1.depth <= box2.z or
                box2.z + box2.depth <= box1.z)

def try_place(box, placed_boxes, container):
    for z in range(container['depth'] - int(box.depth) + 1):
        for y in range(container['height'] - int(box.height) + 1):
            for x in range(container['width'] - int(box.width) + 1):
                box.x, box.y, box.z = x, y, z
                if all(not overlap(box, other) for other in placed_boxes):
                    return True
    return False

def is_small_box(box, threshold_volume=10):
    return box.width * box.height * box.depth < threshold_volume

def is_on_edge(box, container, margin=1.0):
    return (box.x <= margin or
            box.y <= margin or
            box.z <= margin or
            box.x + box.width >= container['width'] - margin or
            box.y + box.height >= container['height'] - margin or
            box.z + box.depth >= container['depth'] - margin)

def advanced_cost_function(order, container):
    placed_boxes = []
    center_x, center_y, center_z = container['width'] / 2, container['height'] / 2, container['depth'] / 2
    total_x = total_y = total_z = total_volume = 0
    fragile_penalty = 0
    max_z = 0
    unplaced_penalty = 0
    base_bias_penalty = 0
    edge_penalty = 0

    for box in order:
        placed = False
        for orientation_idx in range(6):
            box.rotate(orientation_idx)
            if try_place(box, placed_boxes, container):
                placed_boxes.append(box)
                total_x += box.x + box.width / 2
                total_y += box.y + box.height / 2
                total_z += box.z + box.depth / 2
                total_volume += box.width * box.height * box.depth
                max_z = max(max_z, box.z + box.depth)

                # Check fragile penalty
                if box.is_fragile:
                    stacked = sum(
                        1 for other in placed_boxes if other != box and overlap(other, box) and other.z < box.z
                    )
                    if stacked > 0:
                        fragile_penalty += 1e6
                
                base_bias_penalty += (box.x + box.y + box.z)

                if is_small_box(box) and is_on_edge(box, container):
                    edge_penalty += 1e6

                break

        if not placed:
            return 1e12

    avg_x, avg_y, avg_z = total_x / len(placed_boxes), total_y / len(placed_boxes), total_z / len(placed_boxes)
    center_penalty = math.sqrt((avg_x - center_x) ** 2 + (avg_y - center_y) ** 2 + (avg_z - center_z) ** 2)

    total_container_volume = container['width'] * container['height'] * container['depth']
    unused_volume = total_container_volume - total_volume

    volumn_penalty = unused_volume / total_container_volume
    height_penalty = max_z / container['depth']

    total_cost = (
        center_penalty +
        fragile_penalty +
        volumn_penalty +
        (max_z / container['depth']) +
        base_bias_penalty * 0.5 +
        unplaced_penalty +
        edge_penalty
    )
    return total_cost