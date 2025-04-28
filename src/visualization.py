from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
import pandas as pd

def plot_data(train_df, ideal_df, selected_ideals, test_results):
    # Create figure
    p = figure(title="Training, Optimal Functions and Test Data", x_axis_label='x', y_axis_label='y')
    
    # Plotting training data
    for k in range(1, 5):
        p.scatter(x=train_df['x'], y=train_df[f'y{k}'], legend_label=f'Treinamento y{k}', 
                  color='blue', alpha=0.5, size=5)  
    
    # Plot selected ideal functions
    colors = ['red', 'green', 'orange', 'purple']
    for idx, ideal_col in enumerate(selected_ideals):
        p.line(ideal_df['x'], ideal_df[ideal_col], legend_label=f'Ideal {ideal_col}', 
               color=colors[idx], line_width=2)
    
    # Ensure test_results has no NaN values ​​in x or y
    test_results = test_results.dropna(subset=['x', 'y'])
    
    # Plot test data
    ideal_to_color = {ideal: colors[idx] for idx, ideal in enumerate(selected_ideals)}
    test_results['color'] = test_results['ideal_func'].map(lambda x: ideal_to_color.get(x, 'gray'))
    
    # Create ColumnDataSource for test data
    source = ColumnDataSource(test_results)
    p.scatter(x='x', y='y', source=source, color='color', legend_label='Teste', size=5)
    
    # Display the chart
    show(p)