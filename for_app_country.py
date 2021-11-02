import pandas as pd
import requests
import json
from datetime import datetime
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import os
from dash import callback_context
import webbrowser
import dash_auth


df_merged = pd.read_pickle('df_merged_reduced.pkl' )


external_stylesheets = [dbc.themes.BOOTSTRAP]
VALID_USERNAME_PASSWORD_PAIRS = {'linnaeus': 'hldesign'}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.title = 'Industry_Phd'
auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)

def for_in(cntry='FI',window=3):
    erp = df_merged[df_merged['ship_country_iso_name']== cntry.upper()]
    erp=erp.sort_values(by=['completed_at'])
    if cntry == 'FI':
        fig = px.line(erp, y='no_orders_FI', x='completed_at',height=600,color_discrete_sequence =['blue'])
        fig.update_layout(title_x=0.5,plot_bgcolor='black',paper_bgcolor='black',xaxis_title="Date",yaxis_title='No of Orders')
        fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        fig.update_yaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        return fig
    elif cntry == 'NO':
        fig = px.line(erp, y='no_orders_NO', x='completed_at',height=600,color_discrete_sequence =['blue'])
        fig.update_layout(title_x=0.5,plot_bgcolor='black',paper_bgcolor='black',xaxis_title="Date",yaxis_title='No of Orders')
        fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        fig.update_yaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        return fig
    elif cntry == 'DK':
        fig = px.line(erp, y='no_orders_DK', x='completed_at',height=600,color_discrete_sequence =['blue'])
        fig.update_layout(title_x=0.5,plot_bgcolor='black',paper_bgcolor='black',xaxis_title="Date",yaxis_title='No of Orders')
        fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        fig.update_yaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        return fig
    
    else:
        fig = px.line(erp, y='no_orders_SE', x='completed_at',height=600,color_discrete_sequence =['blue'])
        fig.update_layout(title_x=0.5,plot_bgcolor='black',paper_bgcolor='black',xaxis_title="Date",yaxis_title='No of Orders')
        fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        fig.update_yaxes(title_font=dict(size=18, family='Courier', color='crimson'),tickfont=dict(family='Rockwell', color='crimson', size=14))
        return fig

colors = {
    'background': '#111111',
    'bodyColor':'#F2DFCE',
    'text': '#7FDBFF'
}
def get_page_heading_style():
    return {'backgroundColor': colors['background']}


def get_page_heading_title():
    return html.H1(children='Industry_PhD',
                                        style={
                                        'textAlign': 'center',
                                        'color': colors['text']
                                    })

def get_page_heading_subtitle():
    return html.Div(children='Visualize klippkungen data',
                                         style={
                                             'textAlign':'center',
                                             'color':colors['text']
                                         })

def generate_page_header():
    main_header =  dbc.Row(
                            [
                                dbc.Col(get_page_heading_title(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    subtitle_header = dbc.Row(
                            [
                                dbc.Col(get_page_heading_subtitle(),md=12)
                            ],
                            align="center",
                            style=get_page_heading_style()
                        )
    header = (main_header,subtitle_header)
    return header

def get_product_list():
    return df_merged['product_name'].unique()
def dates():
    return df_merged['completed_at'].unique()
def country(): 
    return df_merged['ship_country_iso_name'].unique()

def create_dropdown_list(product_name_lst):
    dropdown_list = []
    for product in sorted(product_name_lst):
        tmp_dict = {'label':product,'value':product}
        dropdown_list.append(tmp_dict)
    return dropdown_list
def get_country_dropdown(id):
    return html.Div([
                        html.Label('Select Country',style={'margin-bottom': 10, 'color':'maroon'}),
                        dcc.Dropdown(id='my-id'+str(id),
                            options=create_dropdown_list(country()),
                            value='NO'
                        ),
                        html.Div(id='my-div'+str(id))
                    ])

def graph1():
    return dcc.Graph(id='graph1',figure=for_in('NO'), config={'scrollZoom': True})

def get_slider():
    return html.Div([  
                        dcc.Slider(
                            id='my-slider',
                            min=1,
                            max=15,
                            step=None,
                            marks={
                                1: '1',
                                3: '3',
                                5: '5',
                                7: '1-Week',
                                14: 'Fortnight'
                            },
                            value=3,
                        ),
                        html.Div([html.Label('Select Moving Average Window')],id='my-div'+str(id),style={'textAlign':'center'})
                    ])

def generate_card_content(card_header,card_value):
    card_head_style = {'textAlign':'center','fontSize':'150%'}
    card_body_style = {'textAlign':'center','fontSize':'200%'}
    card_header = dbc.CardHeader(card_header,style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5(f"{int(card_value):,}", className="card-title",style=card_body_style),
            html.P(
                
                className="card-text",style={'textAlign':'center'}
            ),
        ]
    )
    card = [card_header,card_body]
    return card

def generate_cards(cntry='NO'):
    for_out = df_merged[df_merged['ship_country_iso_name'] == cntry]
    conf_cntry_total = for_out['admin_reference'].nunique()
    dead_cntry_total = int(for_out['total'].sum())
    recv_cntry_total = for_out['product_name'].value_counts()[:1]
    if cntry == 'NO':
        sweq = for_out[for_out['no_orders_NO']<1300]
        avg_order_per_day= sum(sweq['no_orders_NO'])/len(sweq['no_orders_NO'])
    elif cntry == 'SE':
        avg_order_per_day = sum(for_out['no_orders_SE'])/len(for_out['no_orders_SE'])
    elif cntry == 'FI':
        avg_order_per_day = sum(for_out['no_orders_FI'])/len(for_out['no_orders_FI'])
    else:
        avg_order_per_day = sum(for_out['no_orders_DK'])/len(for_out['no_orders_DK'])
    city_no_orders = for_out['ship_city'].value_counts()[:1]
    cards = html.Div(
        [
            dbc.Row(
                [
                    
                dbc.Col(dbc.Card(generate_card_content("Total No of Orders",conf_cntry_total), color="success", inverse=True),md=dict(size=2,offset=1)),
                dbc.Col(dbc.Card(generate_card_content("Average Orders Per Day",avg_order_per_day),color="pink", inverse=True),md=dict(size=2)),
                dbc.Col(dbc.Card(generate_card_content(for_out.ship_city.mode(),city_no_orders),color="dark", inverse=True),md=dict(size=2)),
                dbc.Col(dbc.Card(generate_card_content("Revenue Generated in SEK",dead_cntry_total), color="warning", inverse=True),md=dict(size=2)),
                dbc.Col(dbc.Card(generate_card_content(for_out.product_name.mode(),recv_cntry_total),color="dark", inverse=True),md=dict(size=2)),
            
                ],
                className="mb-4",
            ),
        ],id='card1'
    )
    return cards



def map_sweden(): 
    sweden_map = html.Div([html.Img(src='https://www.nicepng.com/png/full/799-7991579_netherlands-prediction-preview-sweden-round-flag-png.png', 
                                            height='60', width='160')], className="ten columns padded"),html.Div([html.Button("SWEDEN", id='btn-nclicks-1', n_clicks=0, style={'margin-top': 10})])
    return sweden_map

def map_finland():
    finland_map= html.Div([
                    html.Img(src='https://cdn-icons-png.flaticon.com/512/197/197585.png', height='60', width='160')
                    ], className="ten columns padded"),html.Div([html.Button("FINLAND", id='btn-nclicks-2', n_clicks=0, style={'margin-top': 10})])
         
    return finland_map 

def map_denmark():
    denmark_map= html.Div([
                    html.Img(src='https://www.fg-a.com/flags/denmark-button-1.png', height='60', width='160')
                    ], className="ten columns padded"),html.Div([html.Button("DENMARK",id='btn-nclicks-3', n_clicks=0,style={'margin-top': 10})]),
         
    return denmark_map 

def map_norway():
    norway_map=  html.Div([
                    html.Img(src='https://www.nicepng.com/png/full/382-3826444_norway-flag-button.png', height='60', width='160')
                    ], className="ten columns padded"),html.Div([html.Button("NORWAY",id='btn-nclicks-4', n_clicks=0,style={'margin-top': 10})]),
         
    return norway_map 

def currency_converter():
    currency = html.Div(
        [
            html.I("Currency Excahnge",style={'margin-bottom': 15, 'color':'maroon'}),
            html.Br(),
            dcc.Input(id="input1", type="number", placeholder="SEK to EUR", debounce=True, style={'marginRight':'10px'}),
            dcc.Input(id="input2", type="number", placeholder="SEK to DKK", debounce=True,style={'marginRight':'10px', 'color':'maroon'}),
            dcc.Input(id="input3", type="number", placeholder="SEK to NOK", debounce=True),
            html.Div(id="output",style={'margin-top': 10, 'color':'maroon'}),
        ])

    return currency



def get_logo():
    logo = html.Div(
        [
            dbc.Row(
                [
                    html.I("Maps",style={'margin-bottom': 10, 'color':'maroon'}),
                    html.Br(),
                    dbc.Col(map_sweden()),
                    dbc.Col(map_finland()),
                    dbc.Col(map_denmark()),
                    dbc.Col(map_norway())
                ]),
                        
        html.Div(id='container-button-timestamp')
        ], style={'margin-top': 40}, className="row gs-header")
    return logo

def extra_features():
    optns = html.Div(
        [
            html.I("More Options",style={'margin-top': 40, 'color':'maroon'}),
            html.Br(),
            html.Button("More Currency Conversions",id='btn-nclicks-5', n_clicks=0,style={'margin-top': 10, 'marginRight':20}),
            html.Button("Go to Cities Page",id='btn-nclicks-6', n_clicks=0,style={'marginRight': 20}),
            html.Button("Go to Products Page",id='btn-nclicks-7', n_clicks=0,style={'marginRight': 20}),
            html.Div(id='container-button')
        ],style={'margin-top': 30})

    return optns

def generate_layout():
    page_header = generate_page_header()
    layout = dbc.Container(
        [
            page_header[0],
            page_header[1],
            html.Hr(),
            generate_cards(),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(get_country_dropdown(id=1),md=dict(size=4,offset=4))                    
                ]
            
            ),
            dbc.Row(
                [                
                    
                    dbc.Col(graph1(),md=dict(size=6,offset=3))
        
                ],
                align="center",

            ),
             dbc.Row(
                [
       
                    dbc.Col(currency_converter(),md=dict(size=5,offset=4))
                    
                ]
            ),
            
            dbc.Row(
                [
       
                    dbc.Col(get_logo(),md=dict(size=4,offset=4))
                ]
            ),
            dbc.Row(
                [
       
                    dbc.Col(extra_features(),md=dict(size=4,offset=4))
                ]
            ),
 
          
        ],fluid=True,style={'backgroundColor': 'black'}
    )
    return layout

app.layout = generate_layout()


@app.callback(Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks'),
    Input('btn-nclicks-4', 'n_clicks'))
def displayClick(btn1, btn2, btn3,btn4):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        return webbrowser.open('Sweden_Map.html')
    elif 'btn-nclicks-2' in changed_id:
        return webbrowser.open('Finland_Map.html')
    elif 'btn-nclicks-3' in changed_id:
        return webbrowser.open('Denmark_Map.html')
    elif 'btn-nclicks-4' in changed_id:
        return webbrowser.open('Norway_Map.html')

@app.callback(Output('container-button', 'children'),
    Input('btn-nclicks-5', 'n_clicks'),
    Input('btn-nclicks-6', 'n_clicks'),
    Input('btn-nclicks-7', 'n_clicks'))
def displayClick_1(btn5, btn6, btn7):
    print(btn5, btn6, btn7)
    changed = [k['prop_id'] for k in callback_context.triggered][0]
    if 'btn-nclicks-5' in changed:
        return html.I("Kailash",style={'margin-top': 40, 'color':'maroon'})
    elif 'btn-nclicks-6' in changed:
        return webbrowser.open('https://www.xe.com/')
    elif 'btn-nclicks-7' in changed:
        return webbrowser.open('https://www.xe.com/')



@app.callback(
    [Output(component_id='graph1',component_property='figure'), #line chart
    Output(component_id='card1',component_property='children')], #overall card numbers
    [Input(component_id='my-id1',component_property='value')])

def update_output_div(input_value1):
    print(input_value1)
    return for_in(input_value1),generate_cards(input_value1)
@app.callback(
    Output("output", "children"),
    Input("input1", "value"),
    Input("input2", "value"),Input("input3", "value")
)

def update_output(input1, input2, input3):
    lst = [input1, input2,input3]
    print(lst)
    if lst.count(None) <= 1:
        return 'Please Select Single Currency'
    elif input1 == None: 
        if input2==None:
            if input3== None:
                return 'Please Select the  currency'
            elif input3 > 0:
                if input1==None:
                    if input2== None:
                        return "{} NOK".format(int(input3)*0.98)
                else:
                    return 'Please Select Singile Currency' 
        elif input2 > 0:
            if input1==None:
                if input3== None:
                    return "{} DKK".format(int(input2)*0.75)
        else:
            return 'Please Select Singile Currency'
    elif input1 > 0:
        if input2==None:
            if input3== None:
                return "{} EUR".format(int(input1)*0.10)

if __name__ == '__main__':
    app.run_server(debug=True)