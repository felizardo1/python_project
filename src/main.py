import pandas as pd
from sqlalchemy import create_engine
from data_processor import TrainingProcessor, TestProcessor
from visualization import plot_data
from exceptions import DataConsistencyError

def main():
    # Carregar os dados
    train_df = pd.read_csv('data/train.csv')
    ideal_df = pd.read_csv('data/ideal.csv')
    test_df = pd.read_csv('data/test.csv')
    
    # Verificar consistência dos dados
    if len(train_df) != len(ideal_df) or not (train_df['x'] == ideal_df['x']).all():
        raise DataConsistencyError("Os valores de x em train.csv e ideal.csv devem ser iguais.")
    
    # Configurar o banco de dados SQLite
    engine = create_engine('sqlite:///my_database.db')
    
    # Salvar os dados no banco
    train_df.to_sql('training', engine, index=False, if_exists='replace')
    ideal_df.to_sql('ideal', engine, index=False, if_exists='replace')
    test_df.to_sql('test', engine, index=False, if_exists='replace')
    
    # Processar dados de treinamento
    train_proc = TrainingProcessor(engine)
    selected_ideals = train_proc.select_ideal_functions(train_df, ideal_df)
    max_devs = train_proc.calculate_max_deviations(train_df, ideal_df, selected_ideals)
    
    # Mapear os dados de teste
    test_proc = TestProcessor(engine)
    test_results = test_proc.map_test_data(test_df, ideal_df, selected_ideals, max_devs)
    
    # Verificar test_results
    print("Verificando test_results:")
    print(test_results.head())
    print("Valores NaN em test_results:", test_results.isna().sum())
    
    test_results.to_sql('test_results', engine, index=False, if_exists='replace')
    
    # Gerar visualização
    plot_data(train_df, ideal_df, selected_ideals, test_results)

if __name__ == '__main__':
    main()