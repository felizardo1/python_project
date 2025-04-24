from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import pandas as pd

def plot_data(train_df, ideal_df, selected_ideals, test_results):
    # Criar figura
    p = figure(title="Dados de Treinamento, Funções Ideais e Teste", x_axis_label='x', y_axis_label='y')
    
    # Plotar dados de treinamento
    for k in range(1, 5):
        p.scatter(x=train_df['x'], y=train_df[f'y{k}'], legend_label=f'Treinamento y{k}', 
                  color='blue', alpha=0.5, size=5)  # Substituído circle por scatter
    
    # Plotar funções ideais selecionadas
    colors = ['red', 'green', 'orange', 'purple']
    for idx, ideal_col in enumerate(selected_ideals):
        p.line(ideal_df['x'], ideal_df[ideal_col], legend_label=f'Ideal {ideal_col}', 
               color=colors[idx], line_width=2)
    
    # Garantir que test_results não tenha valores NaN em x ou y
    test_results = test_results.dropna(subset=['x', 'y'])
    
    # Plotar dados de teste
    ideal_to_color = {ideal: colors[idx] for idx, ideal in enumerate(selected_ideals)}
    test_results['color'] = test_results['ideal_func'].map(lambda x: ideal_to_color.get(x, 'gray'))
    
    # Criar ColumnDataSource para os dados de teste
    source = ColumnDataSource(test_results)
    p.scatter(x='x', y='y', source=source, color='color', legend_label='Teste', size=5)
    
    # Exibir o gráfico
    show(p)