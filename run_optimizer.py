import pandas as pd
import time
from optimizer.sa_optimizer import simulated_annealing
from optimizer.box import Box

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
def main():
    df = pd.read_csv('data/box_placement_data.csv')
    df['is_fragile'] = df['is_fragile'].fillna(0).astype(int)

    boxes = [Box(
        row['box_id'],
        row['width'],
        row['height'],
        row['depth'],
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
            'depth': box.depth,
            'is_fragile': box.is_fragile
        })

    pd.DataFrame(records).to_csv('data/optimized_box_data.csv', index=False)
    print("Saved to 'data/optimized_box_data.csv'")

if __name__ == "__main__":
    main()
