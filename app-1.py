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


### bar chart example
x = ['Consumer', 'Corporate', 'Home Office']
y = [81.4, 57.8, 36.03]

data2 = [go.Bar(
            x=x,
            y=y,
            text=y,
            textposition = 'auto',
            name='Top 3 Most Profitable Segments',
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5),
            ),
            opacity=0.6
        )]

fig2 = go.Figure(data = data2)

layout = go.Layout(
    xaxis=dict(tickangle=-45),
    barmode='group',
)
####
data3 = [go.Bar(
            x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
            name='Total Sales per Month',
            marker=dict(
                color='rgb(49,130,189)'
            ),
        )]
fig3 = go.Figure(data = data3)



superstore = "Superstore.xls"
superstore_df = pd.read_excel(superstore)
superstore_df['year'] = superstore_df['Order Date'].dt.year
opts = [{'label' : 'Select a year', 'value': ""}] +\
     [{'label' : i, 'value' : i} for i in list(superstore_df.year.unique())] # dropdown options

# Step 3. Create a plotly figure
## function to filter and groupby df by year (e.g. 2013,df -> df)
def filter_year(y, df):
    df_filter = df[(df.year == y)][["City","State","Code","Latitude", "Longitude","Category", "Sales", "Profit"]]
    df_agg = df_filter.groupby(['State','Code']).sum().reset_index()
    return df_agg

## function to create data for plotly (df -> data)
def create_plotly(df):

    df_st = df.copy()

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
        colorscale=scl,
        autocolorscale=True,
        locations=df_st['Code'],
        z=df_st['Profit'].astype(float),
        locationmode='USA-states',
        text=df_st['text'],
        marker=go.choropleth.Marker(
            line=go.choropleth.marker.Line(
                color='rgb(255,255,255)',
                width=2
            )),
        colorbar=go.choropleth.ColorBar(title="Sale&Profit$$"))]
    return data

## layout
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



#fig = go.Figure(data=data, layout=layout)
#py.iplot(fig, filename='angled-text-bar')
# 

fig = go.Figure(data = create_plotly(filter_year(2013, superstore_df)), layout = layout)
# pyo.iplot(fig, filename = 'test')

# Step 4. Create a Dash layout
app.layout = html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1("Superstore USA"),
                    html.P("We're making your shopping experience easier with flyers, deals and online shopping. Browse your local store or shop select locations online with Click .!")
                         ], 
                    style = {'padding' : '50px' , 
                             'backgroundColor' : '#3aaab2'}),                   

                # dropdown
                html.P([
                    html.Label("Choose a year"),
                    dcc.Dropdown(id = 'opt', 
                                 options = opts,
                                 value = opts[0])
                        ], style = {'width': '170px',
                                    'fontSize' : '15px',
                                    'padding-left' : '95px',
                                    'display': 'inline-block'}),
                #   adding a plot
                dcc.Graph(id = 'plot', figure = fig),                                   
                dcc.Graph(id = 'plot2', figure = fig2),
                dcc.Graph(id = 'plot3', figure = fig3)
                      ])

# Step 5. Add callback functions

@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])
def update_figure(input1):

    fig = go.Figure(data =  create_plotly(filter_year(input1, superstore_df)), layout = layout)
    return fig


# Step 6. Add the server clause
if __name__ == '__main__':
    app.run_server(debug = True)
