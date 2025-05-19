import os
import json
import pandas as pd
from optimizer.box import Box
from optimizer.sa_optimizer import simulated_annealing
from optimizer.cost_functions import advanced_cost_function

def evaluate_task(task_id):
    box_file = f"data/task_{task_id:02}_boxes.csv"
    container_file = f"data/task_{task_id:02}_container.json"

    df = pd.read_csv(box_file)
    with open(container_file, "r") as f:
        container = json.load(f)

    df['is_fragile'] = df['is_fragile'].fillna(0).astype(int)

    boxes = [Box(
        row['box_id'],
        row['original_width'],
        row['original_height'],
        row['original_depth'],
        row['is_fragile']
    ) for _, row in df.iterrows()]

    best_solution, cost, details = simulated_annealing(boxes, container, return_details=True)
    placed_count = len(best_solution)
    total_volume = sum([b.width * b.height * b.depth for b in best_solution])
    container_volume = container['width'] * container['height'] * container['depth']
    utilization = total_volume / container_volume

    return {
        "task": f"task_{task_id:02}",
        "placed": placed_count,
        "utilization": round(utilization * 100, 2),
        "cost": round(cost, 2),
        **details
    }

def main():
    results = []
    for task_id in range(1, 11):
        try:
            result = evaluate_task(task_id)
            results.append(result)
            print(result)
        except Exception as e:
            print(f"❌ Task {task_id:02} failed:", e)

    df_result = pd.DataFrame(results)
    df_result.to_csv("evaluation_results.csv", index=False)
    print("\n✅ Evaluation completed. Results saved to evaluation_results.csv")

if __name__ == "__main__":
    main()