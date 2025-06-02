import pandas as pd
import time
from optimizer.sa_optimizer import simulated_annealing
from optimizer.box import Box
import random
import os

# 规则：
# 1. 箱子不能重叠
# 2. 箱子不能超出容器的边界
# 3. fragile箱子上不能放超过1个箱子
# 4. 小箱子不能放边缘
# 5. 箱子越低越好
# 6. 箱子越靠近原点越好
# 7. 空间利用率越高越好
# 8. 靠墙放置箱子越好
# 9. 箱子越靠近中心越好

# 这个文件是一个优化器的主程序。它从 CSV 文件中读取箱子数据，创建箱子对象，并使用模拟退火算法来优化箱子的放置。
# 最后，它将优化后的箱子数据保存到另一个 CSV 文件中。该程序的设计允许用户轻松地调整容器的大小和模拟退火算法的参数，以获得最佳的箱子放置方案。
# def main():
#     df = pd.read_csv('data/box_placement_data.csv')
#     df['is_fragile'] = df['is_fragile'].fillna(0).astype(int)

#     boxes = [Box(
#         row['box_id'],
#         row['width'],
#         row['height'],
#         row['depth'],
#         row['is_fragile']
#     ) for _, row in df.iterrows()]

#     container = {'width': 20, 'height': 15, 'depth': 20}

#     best_overall = None
#     best_cost = float('inf')
#     total_runs = 10

#     for i in range(total_runs):
#         print(f"▶ Run {i+1}/{total_runs}")
#         run_boxes = [b.copy() for b in boxes]
#         solution, cost = simulated_annealing(run_boxes, container)
#         if cost < best_cost:
#             best_cost = cost
#             best_overall = [b.copy() for b in solution]

#     print("\n Best Cost:", best_cost)
#     records = []
#     for idx, box in enumerate(best_overall):
#         records.append({
#             'placement_order': idx+1,
#             'box_id': box.box_id,
#             'x': box.x,
#             'y': box.y,
#             'z': box.z,
#             'width': box.width,
#             'height': box.height,
#             'depth': box.depth,
#             'is_fragile': box.is_fragile
#         })

#     pd.DataFrame(records).to_csv('data/optimized_box_data.csv', index=False)
#     print("Saved to 'data/optimized_box_data.csv'")

# if __name__ == "__main__":
#     main()


def load_boxes(csv_path):
    Box.counter = 1  # Reset static counter for consistent unique_id
    df = pd.read_csv(csv_path)
    df['is_fragile'] = df['is_fragile'].fillna(0).astype(int)
    return [Box(
        row['box_id'],
        row['width'],
        row['height'],
        row['depth'],
        row['is_fragile']
    ) for _, row in df.iterrows()]

def save_solution(solution, path, best_cost=None):
    records = []
    for idx, box in enumerate(solution):
        records.append({
            'placement_order': idx + 1,
            'box_id': box.box_id,
            'x': box.x,
            'y': box.y,
            'z': box.z,
            'width': box.width,
            'height': box.height,
            'depth': box.depth,
            'is_fragile': box.is_fragile
        })
    df = pd.DataFrame(records)
    df.to_csv(path, index=False)
    print(f"✅ Saved solution to {path}")
    if best_cost is not None:
        print(f"   ↪ Cost: {best_cost:.2f}")

def greedy_heuristic(boxes, container):
    placed = []
    cursor = [0, 0, 0]
    max_y = 0
    for box in boxes:
        box.x, box.y, box.z = cursor
        placed.append(box)
        cursor[0] += box.width
        if cursor[0] >= container['width']:
            cursor[0] = 0
            cursor[2] += box.depth
        if cursor[2] >= container['depth']:
            cursor[2] = 0
            max_y += box.height
            cursor[1] = max_y
        if cursor[1] + box.height > container['height']:
            break
    return placed

def random_permutation(boxes, container):
    boxes_copy = [b.copy() for b in boxes]
    random.shuffle(boxes_copy)
    for box in boxes_copy:
        box.rotate(random.randint(0, 5))
    return greedy_heuristic(boxes_copy, container)

def sort_by_position(boxes):
    return sorted(boxes, key=lambda b: (b.z, b.y, b.x))

def run_experiments():
    input_path = 'data/box_sample.csv'
    container = {'width': 18, 'height': 8, 'depth': 8}
    total_runs = 10
    output_dir = 'data/results'
    os.makedirs(output_dir, exist_ok=True)

    original_boxes = load_boxes(input_path)

    # Simulated Annealing
    best_sa_cost = float('inf')
    best_sa_solution = None
    for i in range(total_runs):
        print(f"[SA Run {i+1}/{total_runs}]")
        boxes = [b.copy() for b in original_boxes]
        solution, cost = simulated_annealing(boxes, container)
        if cost < best_sa_cost:
            best_sa_cost = cost
            best_sa_solution = solution
    sorted_sa_solution = sort_by_position(best_sa_solution)
    save_solution(sorted_sa_solution, os.path.join(output_dir, 'sa_output.csv'), best_sa_cost)

    # Greedy Heuristic
    print("[Greedy Heuristic]")
    greedy_result = greedy_heuristic([b.copy() for b in original_boxes], container)
    sorted_greedy = sort_by_position(greedy_result)
    save_solution(sorted_greedy, os.path.join(output_dir, 'greedy_output.csv'))

    # Random Permutation
    print("[Random Permutation]")
    random_result = random_permutation(original_boxes, container)
    sorted_random = sort_by_position(random_result)
    save_solution(sorted_random, os.path.join(output_dir, 'random_output.csv'))

if __name__ == "__main__":
    run_experiments()