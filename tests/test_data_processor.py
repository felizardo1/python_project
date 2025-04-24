import unittest
import pandas as pd
from src.data_processor import TrainingProcessor

class TestDataProcessor(unittest.TestCase):
    def test_select_ideal_functions(self):
        train_df = pd.DataFrame({'x': [1, 2], 'y1': [2, 4], 'y2': [3, 6]})
        ideal_df = pd.DataFrame({'x': [1, 2], 'y1': [2, 4], 'y2': [5, 10]})
        processor = TrainingProcessor(None)
        selected = processor.select_ideal_functions(train_df, ideal_df)
        self.assertEqual(len(selected), 2)
        self.assertIn('y1', selected)

if __name__ == '__main__':
    unittest.main()