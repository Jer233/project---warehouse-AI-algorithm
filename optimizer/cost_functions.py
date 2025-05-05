import pandas as pd

def volumn_priority_cost(order, df):
    """Cost function that prioritizes placing larger volumn boxes earlier."""

    total_penalty = 0
    for idx, box_id in enumerate(order):
        dims = df[df['box_id'] == box_id][['original_width', 'original_height', 'original_depth']].values[0]
        volumn = dims[0] * dims[1] * dims[2]
        penalty = volumn * (len(order) - idx)
        total_penalty += penalty
    return total_penalty

