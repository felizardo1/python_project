import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self, engine):
        self.engine = engine

class TrainingProcessor(DataProcessor):
    def select_ideal_functions(self, train_df, ideal_df):
        selected_ideals = []
        for k in range(1, 5):  # Para y1, y2, y3, y4
            y_train = train_df[f'y{k}']
            sses = [((y_train - ideal_df[f'y{i}']) ** 2).sum() for i in range(1, 51)]
            best_idx = sses.index(min(sses))
            selected_ideals.append(f'y{best_idx + 1}')
        return selected_ideals
    
    def calculate_max_deviations(self, train_df, ideal_df, selected_ideals):
        max_devs = []
        for k, ideal_col in enumerate(selected_ideals, start=1):
            y_train = train_df[f'y{k}']
            y_ideal = ideal_df[ideal_col]
            max_dev = (y_train - y_ideal).abs().max()
            max_devs.append(max_dev)
        return max_devs

class TestProcessor(DataProcessor):
    def map_test_data(self, test_df, ideal_df, selected_ideals, max_devs):
        results = []
        for _, row in test_df.iterrows():
            x_test, y_test = row['x'], row['y']
            candidates = []
            for k, ideal_col in enumerate(selected_ideals):
                y_ideal = np.interp(x_test, ideal_df['x'], ideal_df[ideal_col])
                dev = abs(y_test - y_ideal)
                if dev <= np.sqrt(2) * max_devs[k]:
                    candidates.append((dev, ideal_col))
            if candidates:
                best_dev, best_ideal = min(candidates, key=lambda x: x[0])
                results.append((x_test, y_test, best_dev, best_ideal))
            else:
                results.append((x_test, y_test, np.nan, None))
        return pd.DataFrame(results, columns=['x', 'y', 'delta_y', 'ideal_func'])