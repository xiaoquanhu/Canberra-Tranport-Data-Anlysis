import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import dash
import dash_core_components as dcc
import dash_html_components as html

graphs = {}
months_lsit = [m[1]
               for m in json.load(open('output/months_index.json'))['months']]
for i in months_lsit:
    df = pd.read_csv(f'output/{i}_Hourly_delay_average.csv')
    graphs[f'bar{i}'] = px.bar(df, x='time', y='delay',
                               hover_data=['delay'], color='delay',
                               text='delay',
                               labels={'average delay': 'seconds'}, height=400)
    graphs[f'bar{i}'].update_xaxes(showline=True, linewidth=2,
                                   linecolor='black', mirror=True)
    graphs[f'bar{i}'].update_yaxes(showline=True, linewidth=2,
                                   linecolor='black', mirror=True)
    graphs[f'bar{i}'].update_layout(title_text=f'{i}_average_delay_analysis')

    dff = pd.read_csv(f'output/{i}_trips_analysis.csv')
    graphs[f'stack{i}'] = go.Figure()
    graphs[f'stack{i}'].add_trace(
        go.Bar(name='complete trips', x=dff['date'].tolist(), y=dff['complete_trips'].tolist()))
    graphs[f'stack{i}'].add_trace(
        go.Bar(name='missed trips', x=dff['date'].tolist(), y=dff['missed_trips'].tolist()))
    graphs[f'stack{i}'].add_trace(
        go.Bar(name='partial trips', x=dff['date'].tolist(), y=dff['partial_trips'].tolist()))
    graphs[f'stack{i}'].add_trace(
        go.Bar(name='no_record trips', x=dff['date'].tolist(), y=dff['no_record_trips'].tolist()))

    graphs[f'stack{i}'].update_xaxes(showline=True, linewidth=2,
                                     linecolor='black', mirror=True)
    graphs[f'stack{i}'].update_yaxes(showline=True, linewidth=2,
                                     linecolor='black', mirror=True)
    graphs[f'stack{i}'].update_layout(barmode='stack')
    graphs[f'stack{i}'].update_layout(title_text=f'{i}_trips_analysis')

    dfarr = pd.read_csv(f'output/{i}_arrival_analysis.csv')
    graphs[f'group{i}'] = go.Figure()
    graphs[f'group{i}'].add_trace(
        go.Bar(name='data lost', x=dfarr['date'].tolist(), y=dfarr['data_lost'].tolist()))
    graphs[f'group{i}'].add_trace(
        go.Bar(name='actual arrivals', x=dfarr['date'].tolist(), y=dfarr['arrivals'].tolist()))
    graphs[f'group{i}'].add_trace(
        go.Bar(name='schedule arrivals', x=dfarr['date'].tolist(), y=dfarr['schedule_arrival'].tolist()))
    graphs[f'group{i}'].update_xaxes(showline=True, linewidth=2,
                                     linecolor='black', mirror=True)
    graphs[f'group{i}'].update_yaxes(showline=True, linewidth=2,
                                     linecolor='black', mirror=True)
    graphs[f'group{i}'].update_layout(barmode='group')
    graphs[f'group{i}'].update_layout(title_text=f'{i}_arrival_analysis')

    for string in ['Peak', 'Daily']:
        instance = json.load(open(f'output/{i}_{string}_delay.json'))
        graphs[f'{string}{i}'] = go.Figure()
        for k in instance:
            graphs[f'{string}{i}'].add_trace(go.Box(
                y=[instance[k][tid] for tid in instance[k]],
                name=k,
                notched=True))
        graphs[f'{string}{i}'].update_layout(
            title_text=f'{i}_{string}_delay_analysis')

# for name in graphs:
#     graphs[name].write_image(f'graphs/{name}.pdf')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

forchildren = [html.H1(
    children='Canberra Light Rail Performance Analysis Dashboard',
    style={
        'textAlign': 'center',
        'color': colors['text']
    }
),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    })]

df = pd.read_csv("output/payment_results.csv")
table = go.Figure()
table.add_trace(
    go.Table(
        header=dict(
            values=["Month", "AOTRA", "PSA", "ESA", "LSA", "MA", "CS", "MHS",
                    "PCSR", "TPS", "SE", "LSR", "SL", "SS", "SC"],
            font=dict(size=20),
            align="left"
        ),
        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:]],
            font=dict(size=12),
            align="left")
    )
)
table.update_layout(
    title_text='Payment Mechanism Results:')

forchildren.append(dcc.Graph(
    id='paymentresult',
    figure=table))

missed_jj = json.load(open(f'output/missed_results.json'))
forchildren.append(html.Div(children='Missed head ways', style={
    'textAlign': 'center',
    'color': colors['text']
}))
for m in missed_jj:
    forchildren.append(html.Div(children=f'{m}: {missed_jj[m]}', style={
        'textAlign': 'left',
        'color': colors['text']
    }))
forchildren.append(html.Div(children="     ",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="     ",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="Definitions: ",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="AOTRA(Availability and On Time Running Adjustment)=PSA - ESA - LSA",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="PSA(Passenger Service Availability)= [minimum {99.5%, MA}] /99.5%", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="MA = (CS + [MHS * 0.70] + PCSR) TPS", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="CS = the number of Completed Services in the Payment Month",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="MHS = the number of Missed Headway Services in the Payment Month",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="PCSR = the Partially Completed Services Result for the Payment Month",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="TPS = the number of Total Scheduled Services in the Payment Month",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="PCSR = ∑[(AAd / SAd) x TPCSd x 0.70]", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="AAd = the actual number of arrivals at Stops by Passenger Services in the relevant day (d) in the Payment Month", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="SAd = the number of scheduled arrivals at Stops by Passenger Services for the relevant day (d) in the Payment Month", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="TPCSd = the total number of Passenger Services for the relevant day (d) in the Payment Month for which Partially Completed Services were provided", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="ESA(Early Services Adjustment) = (SE / SS) x 0.70",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="SE = the number of Early Departures at Stops by Passenger Services for the relevant Payment Month", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="SS = the number of times that Completed Services departed from Measuring Stops in the relevant Payment Monthd", style={
                   'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="LSA(Late Services Adjustment) = (1 - [(minimum {98%, (1 - LSR)}) /98%]) x 0.35",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="LSR = SL/SC",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="SL = the number of Late Arrivals in the relevant Payment Month",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="SC = the number of times that Completed Services arrived at Measuring Stops in the relevant Payment Month",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="Completed Service: Passenger Service or Special Event Service arrives at the Terminating Stop no later than the Scheduled Arrival Time of \
    the next Passenger Service or Special Event Service (as applicable) following that Passenger Service;  in the case of the last Passenger Service \
         of that day, that Passenger Service arrives at the Terminating Stop no later than 15 minutes after the last Scheduled Arrival Time of that day",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="Missed Headway Servic: departs from the designated Originating Stop, stops at all Stops and arrives at the designated Terminating Stop,\
    but arrives at the Terminating Stop or any Measuring Stop later than the Scheduled Arrival Time of the next Passenger Service or Special Event Service (as applicable) following that Passenger Service;\
        in the case of the last Passenger Service of that day, departs from the designated Originating Stop, stops at all Stops and arrives at the designated Terminating Stop,\
             but arrives at the Terminating Stop or any Measuring Stop later than 15 minutes after the last Scheduled Arrival Time of that day",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="Partially Completed Service: not arrives at one or more of the Stops in accordance with the Timetabley",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="Early Departure: the departure of a Completed Service from a Measuring Stop more than 30 seconds before the Scheduled Departure Time",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="Late Arrival: the arrival of a Completed Service at a Measuring Stop more than 120 seconds after the Scheduled Arrival Time at that Measuring Stop, and excludes Special Events Services",
                            style={'textAlign': 'left', 'color': colors['text']}))
forchildren.append(html.Div(children="Measuring Stop means a Stop at which Early Departures and Late Arrivals are measured. Each of the following Stops is a Measuring Stop:\
(a) each Originating Stop;\
(b) each Terminating Stop;\
(c) Dickson; and\
(d) Well Station Drive.",
                            style={'textAlign': 'left', 'color': colors['text']}))

for st in ['stack', 'group', 'bar', 'Peak', 'Daily']:
    if st == 'stack':
        forchildren.append(html.Div(children='Below is the monthly trips anlysis:', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
        forchildren.append(html.Div(children='X axis is date, Y  axis is number of trips (completed, missed, partial and no record)', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
    elif st == 'group':
        forchildren.append(html.Div(children='Below is the monthly arrival anlysis', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
        forchildren.append(html.Div(children='X axis is date, Y  axis is number of arrivals (actual, data-lost, scheduled)', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
    elif st == 'bar':
        forchildren.append(html.Div(children='Below is the monthly average delay', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
        forchildren.append(html.Div(children='X axis is time period, Y  axis is average seconds of all delay in the this month', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
    elif st == 'Peak':
        forchildren.append(html.Div(children='Below is the monthly Peak time box analysis', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
        forchildren.append(html.Div(children='X axis is date, Y axis is average delay seconds of each trip of peak time in the this month', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
    else:
        forchildren.append(html.Div(children='Below is the monthly delay time box analysis', style={
            'textAlign': 'center',
            'color': colors['text']}))
        forchildren.append(html.Div(children='X axis is date, Y axis is average delay seconds of each trip in the this month', style={
            'textAlign': 'center',
            'color': colors['text']
        }))
    for i in months_lsit:
        forchildren.append(dcc.Graph(
            id=f'{st}{i}',
            figure=graphs[f'{st}{i}']))


app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=forchildren)

if __name__ == '__main__':
    app.run_server(debug=True)
