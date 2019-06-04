import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import plotly.offline as pyo
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

# Step 1. Launch the application
app = dash.Dash()

# Step 2. Import the dataset
#df = pd.read_csv(filepath)
superstore = "Superstore.xls"
superstore_df = pd.read_excel(superstore)

Superstore = superstore_df[["City","State","Code","Latitude", "Longitude","Category", "Sales", "Profit"]]
Superstore_agg = Superstore.groupby(['State','Code']).sum().reset_index()

# Step 3. Create a plotly figure

df_st = Superstore_agg.copy()

for col in df_st.columns:
    df_st[col] = df_st[col].astype(str)

scl = [
    [0.0, 'rgb(242,240,247)'],
    [0.2, 'rgb(218,218,235)'],
    [0.4, 'rgb(188,189,220)'],
    [0.6, 'rgb(158,154,200)'],
    [0.8, 'rgb(117,107,177)'],
    [1.0, 'rgb(84,39,143)']
]

df_st['text'] = df_st['State'] + '<br>' + \
    'Profit' + df_st['Profit'] + ' Sales ' + df_st['Sales']

data = [go.Choropleth(
    colorscale = scl,
    autocolorscale = True,
    locations = df_st['Code'],
    z = df_st['Profit'].astype(float),
    locationmode = 'USA-states',
    text = df_st['text'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(255,255,255)',
            width = 2
        )),
    colorbar = go.choropleth.ColorBar(
        title = "Sale&Profit$$")
)]

layout = go.Layout(
    title = go.layout.Title(
        text = 'Superstore'
    ),
    geo = go.layout.Geo(
        scope = 'usa',
        projection = go.layout.geo.Projection(type = 'albers usa'),
        showlakes = True,
        lakecolor = 'rgb(255, 255, 255)'),
)

fig = go.Figure(data = data, layout = layout)
# pyo.iplot(fig, filename = 'test')

# Step 4. Create a Dash layout
app.layout = html.Div([
                dcc.Graph(id = 'plot_id', figure = fig)
                      ])

# Step 5. Add callback functions


# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = True)