from __future__ import print_function

from datetime import datetime as dt, timedelta
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash

from drive.drive import document
from view.components import tab1_content, tab2_content


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True


def find_sheet(document, day):
    for sheet in document:
        if sheet['meta']['day'] == day:
            return sheet

def main():

    app.layout = html.Div([
        html.H6(children='Aksigorta DWH Operations', style={
            'textAlign': 'center'
        }),
        dcc.Tabs(
            id="tabs-with-classes",
            value='tab-1',
            parent_className='custom-tabs',
            className='custom-tabs-container',
            children=[
                dcc.Tab(
                    label='Daily',
                    value='tab-1',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
                dcc.Tab(
                    label='Trends',
                    value='tab-2',
                    className='custom-tab',
                    selected_className='custom-tab--selected'
                ),
            ]),
            html.Div(id='tabs-content-classes')
    ])



    @app.callback(
        Output('plan-dur-pie', 'figure'),
        [Input('date-picker-single', 'date')])
    def update_pie(date):
        date = dt.strptime(date[:10], '%Y-%m-%d')
        if date is not None:
            day = date.strftime("%Y%m%d")
            sheet = find_sheet(document, day)
            data = sheet['data']
            return {
                'data': [
                    go.Pie(labels=[plan['plan'] for plan in data], values=[plan['duration'] for plan in data])
                ]
            }

    @app.callback(
        Output('table', 'data'),
        [Input('date-picker-single', 'date')])
    def update_table(date):
        date = dt.strptime(date[:10], '%Y-%m-%d')
        if date is not None:
            day = date.strftime("%Y%m%d")
            sheet = find_sheet(document, day)
            data = sheet['data']
            return data


    @app.callback(
        Output('tabs-content-classes', 'children'),
        [Input('tabs-with-classes', 'value')])
    def render_content(tab):
        if tab == 'tab-1':
            return tab1_content
        elif tab == 'tab-2':
            return tab2_content


    @app.callback(
        dash.dependencies.Output('plan-trend', 'figure'),
        [dash.dependencies.Input('plan-dropdown', 'value')])
    def update_plan_trend(plan_name):
        dates = []
        durations = []
        for sheet in document:
            for r in sheet['data']:
                if r['plan'] == plan_name:
                    dates.append(str(sheet['meta']['day']))
                    durations.append(r['duration'])

        return {
            'data': [go.Scatter(y=durations, x=[ dt.strptime(d, '%Y%m%d') for d in dates])],
            'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                height=600,
                xaxis={"title":"Date",
                    'rangeselector': {'buttons': list([
                        {'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                        {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                        {'step': 'all'}])},
                    'rangeslider': {'visible': True}, 'type': 'date'},
                yaxis={"title":"Duration (minutes)"})}


    app.run_server(debug=True)

if __name__ == '__main__':
    main()