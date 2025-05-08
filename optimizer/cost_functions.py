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

def advanced_cost_function(order, container):
    placed_boxes = []
    center_x, center_y, center_z = container['width'] / 2, container['height'] / 2, container['depth'] / 2
    total_x = total_y = total_z = total_volume = 0
    fragile_penalty = 0
    max_z = 0

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
                    above_count = sum(
                        1 for other in placed_boxes if 
                        other.x == box.x and other.y == box.y and 
                        other.z > box.z and overlap(other, box)
                    )
                    if above_count > 1:
                        fragile_penalty += 1e6
                placed = True
                break
        if not placed:
            return 1e9

    avg_x, avg_y, avg_z = total_x / len(placed_boxes), total_y / len(placed_boxes), total_z / len(placed_boxes)
    center_penalty = math.sqrt((avg_x - center_x) ** 2 + (avg_y - center_y) ** 2 + (avg_z - center_z) ** 2)
    unused_volume = container['width'] * container['height'] * container['depth'] - total_volume
    height_penalty = max_z / container['depth']

    return center_penalty + fragile_penalty + height_penalty + unused_volume / (container['width'] * container['height'] * container['depth'])
