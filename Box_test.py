import pandas as pd

# Load the output file
csv_path = 'data/optimized_box_data.csv'  # Replace if needed
df = pd.read_csv(csv_path)

# Set container size
container = {'width': 20, 'height': 15, 'depth': 20}

# Convert to list of dicts
boxes = df.to_dict(orient='records')

# Check for duplicate box_id
duplicate_ids = df['box_id'][df['box_id'].duplicated()].unique()
if len(duplicate_ids) > 0:
    print(f"❌ Duplicate box_id found: {duplicate_ids}")
else:
    print("✅ No duplicate box_id")

# Check boundary violations
violations = []
for box in boxes:
    if (box['x'] + box['width'] > container['width'] or
        box['y'] + box['height'] > container['height'] or
        box['z'] + box['depth'] > container['depth']):
        violations.append(box['box_id'])

if violations:
    print(f"❌ Boxes out of boundary: {violations}")
else:
    print("✅ No boundary violations")

# Check for overlapping boxes
def is_overlapping(a, b):
    return not (
        a['x'] + a['width'] <= b['x'] or b['x'] + b['width'] <= a['x'] or
        a['y'] + a['height'] <= b['y'] or b['y'] + b['height'] <= a['y'] or
        a['z'] + a['depth'] <= b['z'] or b['z'] + b['depth'] <= a['z']
    )

overlap_pairs = []
for i in range(len(boxes)):
    for j in range(i + 1, len(boxes)):
        if is_overlapping(boxes[i], boxes[j]):
            overlap_pairs.append((boxes[i]['box_id'], boxes[j]['box_id']))

if overlap_pairs:
    print(f"❌ Overlapping box pairs: {overlap_pairs}")
else:
    print("✅ No overlapping boxes")
