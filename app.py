# -*- coding: utf-8 
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
#from shapely import wkt
#from shapely.geometry import Polygon, Point
import geopandas as gpd
import folium
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


url = 'https://raw.githubusercontent.com/eric-r-cooper/my_insight_app/master/APP_DATA.csv'


#df = pd.read_csv(url, error_bad_lines=False)
t1 = pd.read_csv('https://raw.githubusercontent.com/eric-r-cooper/nyc_lead_water_service/master/APP_DATA_address.csv',error_bad_lines=False)
t2 = pd.read_csv('https://raw.githubusercontent.com/eric-r-cooper/nyc_lead_water_service/master/APP_DATA_yr.csv',error_bad_lines=False)
t3 = pd.read_csv('https://raw.githubusercontent.com/eric-r-cooper/nyc_lead_water_service/master/APP_DATA_lat.csv',error_bad_lines=False)
t4 = pd.read_csv('https://raw.githubusercontent.com/eric-r-cooper/nyc_lead_water_service/master/APP_DATA_lon.csv',error_bad_lines=False)
df = t1.merge(t2)
df = df.merge(t3)
df = df.merge(t4)
df.drop(columns=['Unnamed: 0'],inplace=True)

df['Prediction'].replace(1,'Lead Service Line',inplace=True)
df['Prediction'].replace(0,'Non-Lead Service Line',inplace=True)
df.rename(columns={'latitude':'Latitude','longitude':'Longitude','YearBuilt':'Construction Year','zip':'Zip Code'},inplace=True)
df = df[['Prediction','Address','Borough','Zip Code','Construction Year','Latitude','Longitude']]
ny_map = folium.Map(location=[40.682, -73.945],tiles='Stamen Toner' ,zoom_start=10)


boros = ["Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='NYC Lead Water Service Lines'


#app.layout = dt.DataTable(
#    id='table',
#    columns=[{"name": i, "id": i} for i in df.columns],
#    data=df.to_dict('records'),
#)


app.layout = html.Div(children=[
    html.H1(children='New York City Lead Service Line Locator'),


    html.Label(["Select Service Line Material:", dcc.RadioItems(id="service",options=[{'label': 'All', 'value': 'All'}, {'label': 'Lead Service Line', 'value': 'Lead'},{'label': 'Non-Lead Service Line', 'value': 'No Lead'}], labelStyle={'display': 'inline-block'})]),        
    html.Label(["Select Borough:", dcc.RadioItems(id="boro",options=[{'label': i, 'value': i} for i in boros],labelStyle={'display': 'inline-block'})]),
    html.Label(["Select Zip Code:",dcc.Dropdown(id="zip")]),
    #html.Label(["Select Your Street Address:",dcc.Dropdown(id="staddr")]),
    html.Div(id='prediction'),
    html.Iframe(id='map', srcDoc=ny_map._repr_html_(), width='50%',height='400',style={'width': '49%', 'display': 'inline-block'}),
    dt.DataTable(id='table',columns=[{"name": i, "id": i} for i in df.columns],data=df.head().to_dict('records'),page_size=50)
    #html.Div(id='prediction')
])


@app.callback(
    dash.dependencies.Output("table", "data"),
    [dash.dependencies.Input("zip","value"), dash.dependencies.Input("service","value")],
)
def update_options(value,service):
    df_service=df
    if (service == 'No Lead'): df_service = df[df['Prediction']=='Non-Lead Service Line']
    elif (service == 'Lead'): df_service = df[df['Prediction']=='Lead Service Line']
    return df_service[df_service['Zip Code']==value].to_dict('records')


#@app.callback(
#    dash.dependencies.Output("boro", "options"),
#    [dash.dependencies.Input("service","value")],
#)
#def update_options(value):
#    if (value == 'No Lead'): df_service = df[df['Prediction']=='Non-Lead Service Line']
#    if (value == 'Lead'): df_service = df[df['Prediction']=='Lead Service Line']
#    return [{'label': i, 'value': i} for i in boros]




@app.callback(
    dash.dependencies.Output("zip", "options"),
    [dash.dependencies.Input("boro","value"), dash.dependencies.Input("service","value")],
)
def update_options(value1,value2):
    df_service=df
    if (value2 == 'No Lead'): df_service = df[df['Prediction']=='Non-Lead Service Line']
    elif (value2 == 'Lead'): df_service = df[df['Prediction']=='Lead Service Line']
    return [{'label': i , 'value': i} for i in df_service[df_service['Borough']==value1]['Zip Code'].unique()]


#@app.callback(
#    dash.dependencies.Output("staddr", "options"),
#    [dash.dependencies.Input("zip","value"),dash.dependencies.Input(component_id = 'service',component_property = "value")],
#)
#def update_options(value1, value2):
#    if (value2 == 'No Lead'): df_service = df[df['Prediction']=='Non-Lead Service Line']
#    else: df_service = df[df['Prediction']=='Lead Service Line']
#    return [{'label': i , 'value': i} for i in df_service[df_service['Zip Code']==value1]['Address'].unique()]


@app.callback(
    dash.dependencies.Output(component_id='prediction', component_property='children'),
    [dash.dependencies.Input(component_id='zip', component_property='value')]
)
def update_output_div(input_value1):
    if isinstance(input_value1, type(None)): return ['']
    return ['Select an address in the table below to find its location.']


@app.callback(
    dash.dependencies.Output(component_id='map', component_property='srcDoc'),
    [dash.dependencies.Input('table','active_cell'), dash.dependencies.Input('table','data')]
)
def update_output_div(input_value1, input_value2):
    active_cell_row_index = ''
    if input_value1:
        #active_cell_row_index = int(input_value1['row'])
        input_value2 = pd.DataFrame(input_value2)
        r = input_value2.iloc[int(input_value1['row'])]
        addr = r.Address
        a = folium.Map(location=[40.682, -73.945],tiles='Stamen Toner' ,zoom_start=10)
        a = ny_map._repr_html_()	
        if isinstance(input_value1, type(None)): return(ny_map._repr_html_())
        new_map = folium.Map(location=[40.682, -73.945],tiles='Stamen Toner' ,zoom_start=10)
        lat = r.Latitude
        lon = r.Longitude
        if (r.Prediction == 'Lead Service Line'): marker = folium.Marker(location=[lat, lon],icon=folium.Icon(color='red'))
        #if (df[df['Address']==addr].iloc[0]['Prediction'] == 'Lead'): marker = folium.Marker(location=[lat, lon],icon=folium.Icon(color='red'))
        else: marker = folium.Marker(location=[lat, lon],icon=folium.Icon(color='blue'))
        marker.add_to(new_map)
        b = new_map._repr_html_()
        return(new_map._repr_html_())
    return(ny_map._repr_html_())

if __name__ == '__main__':
    app.run_server(debug=True)
