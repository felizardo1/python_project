import pandas as pd
from sqlalchemy import create_engine
from data_processor import TrainingProcessor, TestProcessor
from visualization import plot_data
from exceptions import DataConsistencyError

def main():
    # Load the data
    train_df = pd.read_csv('data/train.csv')
    ideal_df = pd.read_csv('data/ideal.csv')
    test_df = pd.read_csv('data/test.csv')
    
    # Check data consistency
    if len(train_df) != len(ideal_df) or not (train_df['x'] == ideal_df['x']).all():
        raise DataConsistencyError("The x values ​​in train.csv and ideal.csv must be equal.")
    
    # Setting up the SQLite database
    engine = create_engine('sqlite:///my_database.db')
    
    # Saving data in the database
    train_df.to_sql('training', engine, index=False, if_exists='replace')
    ideal_df.to_sql('ideal', engine, index=False, if_exists='replace')
    test_df.to_sql('test', engine, index=False, if_exists='replace')
    
    # Processing training data
    train_proc = TrainingProcessor(engine)
    selected_ideals = train_proc.select_ideal_functions(train_df, ideal_df)
    max_devs = train_proc.calculate_max_deviations(train_df, ideal_df, selected_ideals)
    
    # Map the test data
    test_proc = TestProcessor(engine)
    test_results = test_proc.map_test_data(test_df, ideal_df, selected_ideals, max_devs)
    
    # To check test_results
    print("Checking test_results:")
    print(test_results.head())
    print("NaN values ​​in test_results:", test_results.isna().sum())
    
    test_results.to_sql('test_results', engine, index=False, if_exists='replace')
    
    # Generate visualization
    plot_data(train_df, ideal_df, selected_ideals, test_results)

if __name__ == '__main__':
    main()