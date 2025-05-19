import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("evaluation_results.csv")

plt.figure(figsize=(12, 6))
plt.bar(df['task'], df['utilization'], color='skyblue')
plt.title("Container Utilization per Task")
plt.ylabel("Utilization (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("utilization_chart.png")

plt.figure(figsize=(12, 6))
plt.bar(df['task'], df['cost'], color='salmon')
plt.title("Total Cost per Task")
plt.ylabel("Cost")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cost_chart.png")

plt.figure(figsize=(12, 6))
df.set_index("task")[["fragile_penalty", "edge_penalty", "volume_penalty", "height_penalty"]].plot(kind="bar", stacked=True)
plt.title("Penalty Breakdown per Task")
plt.ylabel("Penalty Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("penalty_breakdown_chart.png")