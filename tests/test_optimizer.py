import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optimizer.sa_optimizer import simulated_annealing

def test_sa_runs():
    df = pd.read_csv('data/box_placement_data.csv')
    result = simulated_annealing(df)
    assert isinstance(result, tuple)
    assert len(result[0]) == len(df)
