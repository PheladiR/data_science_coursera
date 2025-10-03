#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# -------------------------------------------------------------------
# Load the dataset
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/"
    "historical_automobile_sales.csv"
)

# Initialize the Dash app
app = dash.Dash(__name__)

# List of years for dropdown
year_list = [i for i in range(1980, 2024)]

# -------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
            style={'color': '#503D36', 'font-size': 24, 'textAlign': 'center'}),

    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={
                'width': '80%',
                'margin': 'auto',
                'font-size': '18px'
            }
        )
    ], style={'margin-bottom': '20px'}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980,
            placeholder='Select Year',
            style={'width': '50%', 'margin': 'auto'}
        )
    ], style={'margin-bottom': '20px'}),

    # TASK 2.3: Add a division for output display
    html.Div(id='output-container',
             className='chart-grid',
             style={'display': 'flex', 'flexDirection': 'column'})
])

# -------------------------------------------------------------------
# TASK 2.4: Creating Callbacks

# Enable/disable year dropdown based on selection
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def toggle_year_dropdown(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# Callback for plotting
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output(selected_statistics, input_year):
    # TASK 2.5: Create and display graphs for Recession Report Statistics
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(
            yearly_rec, x='Year', y='Automobile_Sales',
            title="Average Automobile Sales fluctuation over Recession Period"))

        # Plot 2 Calculate the average number of vehicles sold by vehicle type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(
            avg_sales, x='Vehicle_Type', y='Automobile_Sales',
            title="Average number of vehicles sold by vehicle type"))

        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(
            exp_rec, values='Advertising_Expenditure', names='Vehicle_Type',
            title="Total expenditure share by vehicle type during recessions"))

        # Plot 4 Bar chart for the effect of unemployment rate on vehicle type and sales
        R_chart4 = dcc.Graph(figure=px.bar(
            recession_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
            labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
            title="Effect of Unemployment Rate on Vehicle Type and Sales"))

        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})
        ]

    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]

        # Plot 1 Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas, x='Year', y='Automobile_Sales', title="Average Automobile Sales Over Years"))

        # Plot 2 Total Monthly Automobile sales using line chart
        mas = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(
            mas, x='Month', y='Automobile_Sales', title="Average Monthly Automobile Sales"))

        # Plot 3 Average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
            title=f"Average Vehicles Sold by Vehicle Type in {input_year}"))

        # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data, values='Advertising_Expenditure', names='Vehicle_Type',
            title=f"Total Advertisement Expenditure for Each Vehicle in {input_year}"))

        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    return None

# -------------------------------------------------------------------
# Run App
if __name__ == '__main__':
    app.run(debug=True)

