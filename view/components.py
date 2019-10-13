import dash_core_components as dcc
import plotly.graph_objects as go
import dash_table
from datetime import datetime as dt, timedelta
import dash_html_components as html

from drive.drive import document, find_max_day


title = html.H3(children='Aksigorta DWH Operations', style={
    'textAlign': 'center'
})

plan_dur_pie = dcc.Graph(
    id = 'plan-dur-pie',
    figure={
        'data': [
            go.Pie()
        ],
        'layout': {
            'title': 'Plan Durations'
        }
    }
)

__columns = [
    'plan', 'preriod', 'start', 'end', 'status', 'duration'
]
plan_dur_table = dash_table.DataTable(
    id='table',
    style_data={'tr:hover': { 'background': 'yellow' } },
    style_cell={'textAlign': 'left'},
    columns=[{"name": c.capitalize(), "id": c} for c in __columns],
    sort_action="native",
    sort_mode="single",
    style_as_list_view=True,
    style_data_conditional=[{
        "if": { 'filter_query': '{status} eq "Error"' },
        "fontWeight": "bold"
    }]
)

date_picker = dcc.DatePickerSingle(
    id='date-picker-single',
    min_date_allowed=dt(2019, 10, 1),
    max_date_allowed=(dt.today() - timedelta(days=2)),
    display_format='YYYYMMDD',
    date= dt.strptime(find_max_day(), "%Y%m%d")
)


__plan_names = []

for sheet in document:
    for record in sheet['data']:
        if record['plan'] not in __plan_names:
            __plan_names.append(record['plan'])

plan_dropdown = dcc.Dropdown(
    id='plan-dropdown',
    options=[{'label': p, 'value': p} for p in __plan_names],
    value=__plan_names[0]
)

tab1_content = html.Div([
    date_picker,
    plan_dur_pie,
    plan_dur_table
], style={'padding': 10})

tab2_content = html.Div([
    plan_dropdown,
    dcc.Graph(id='plan-trend'),
], style={'padding': 10})