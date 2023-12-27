# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 14:41:17 2023


Correct the second barchart on the KPI tab. Need to be Quarter instead of Year.
Have a way to analyze only the most relevant suppliers and clients instead of all of them.

@author: pmbfe
"""

import dash
from dash import html
from dash import dcc
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

def init_dashboard(server):

    #Some styles and colors
    tab_selected_style = {'fontWeight': 'bold','borderTop':'1px solid #1AB0C7'}
    date_picker_style = {"marginBottom": "15px"}
    # colors = ['#0F6876','#1AB0C7','#E29041','#7F7F7F','#BAB0AC','#E2E2E2','#1C8356','#1CBE4F','#782AB6','#DEA0FD','#FC0080','#EECA3B','#EF553B','#8C564B','#1829ec','#18ecd7']
    colors = ['#0F6876', '#1AB0C7', '#E29041', '#7F7F7F', '#BAB0AC', '#E2E2E2', '#1C8356', '#1CBE4F', '#782AB6', '#DEA0FD', '#FC0080', '#EECA3B', '#EF553B', '#8C564B', '#1829EC', '#18ECD7', '#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1', '#955251', '#B565A7', '#009B77', '#DD4124', '#D65076', '#45B8AC', '#EFC050', '#5B5EA6', '#A67B5B', '#C4A647', '#CF6766', '#6F9FD8', '#0A495D', '#BC243C', '#F87217', '#404E5A', '#4B0082', '#8F9779', '#A1CAF1', '#F1A7FE', '#ECD540', '#FFD700', '#FF7F50', '#FFD801', '#FF4500', '#FF8C00', '#FF69B4', '#FFA07A', '#FF6347', '#FF0000', '#FF1493', '#FF69B4', '#FF00FF', '#FFC0CB', '#FFDAB9', '#FFD700', '#FFE4B5', '#FFE4C4', '#FFE4E1', '#FFEBCD', '#FFEFD5', '#FFFAF0', '#FFFAFA', '#FFFF00', '#FFFFE0', '#FFFFF0', '#FFFFFF', '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3', '#DCDCDC', '#F5F5F5', '#F8F8FF', '#F0F8FF', '#FAEBD7', '#FAF0E6', '#FFF0F5', '#FFF5EE', '#F5FFFA', '#F0FFFF', '#F0FFF0', '#FFFAF0', '#FFFFF0', '#F0F0F0', '#FAFAFA', '#E6E6FA', '#F0F0FF', '#F5F5DC', '#FFF8DC', '#FAFAD2', '#FFFAFA', '#F5FFFD', '#F5F5F0']    
    
    external_stylesheets = [dbc.themes.MATERIA]
    
    # dash_app = dash.Dash(__name__,server=server,routes_pathname_prefix="/dashapp/",external_stylesheets=external_stylesheets)
    dash_app = dash.Dash(server=server,routes_pathname_prefix="/dashapp/",external_stylesheets=external_stylesheets)

    dash_app.title = 'FELICE SAFT Auto Analytics'
    
    row0 = dbc.Row([dbc.Col(html.Div(children=[html.Div(children=html.Img(src='/static/logo_felice XXI.JPG',style={'width':'100px','height':'auto'}))]),width='auto'),
                    dbc.Col(html.H4(children='SAFT Auto-Analytics para Fundbox'),align='center',width='auto'),
                    dbc.Col(html.Div(dbc.Button('Update',id='update',class_name="btn btn-dark",n_clicks=0)),align='center',width='auto'),
                    dbc.Col(html.A("Voltar",href="/options",target="_self"),align='center')],
                   style={'margin':'0 0 30px 0'})

    
    dash_app.layout = html.Div([row0,html.Div(id='dashboard-content')])

    @dash_app.callback(
        Output("dashboard-content", "children"), [Input("update", "n_clicks")]
    )
    def on_button_click(n):
        if n >0:

            # KPIs
            # df_kpi=pd.read_excel('static/data.xlsx',sheet_name='kpi2')
            # df_kpi['Year'] = df_kpi['Year'].astype(str)    
            df_kpi=pd.read_excel('static/db/kpi.xlsx',usecols=[i for i in range(1,8)])
            df_kpi['Ano'] = df_kpi['Ano'].astype(str)
            df_kpi['TrimAno']= df_kpi['Trim']+df_kpi['Ano']
            df_kpi_pvt = df_kpi.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='KPI',values='Valor',aggfunc='sum')
            df_kpi_pvt.reset_index(inplace=True)  
            
            df_kpi_pvt['Data']=pd.to_datetime(df_kpi_pvt['Data'])
            df_kpi_pvt.sort_values('Data',inplace=True)
            kpi_empresas = df_kpi_pvt.drop_duplicates(subset=['Nome'],keep='last')
            kpi_empresas = round(kpi_empresas,4)
            kpi_empresas.drop(columns=['Data','Trim','Ano'],inplace=True)
           
            # Info for tab1 Resumo
    
            # kpi_empresas = pd.read_excel('static/data.xlsx',sheet_name='kpi')
            dropdown0 = dcc.Dropdown(id='sort-by', options=[{'label': col, 'value': col} for col in kpi_empresas.columns],
                                     placeholder='Ordernar por...',
                                     style={'width':'350px','fontSize':'14px',"marginBottom": "30px"})
            table = dbc.Table.from_dataframe(kpi_empresas, striped=True, bordered=True, hover=True,id='table_kpi')
            tab1 = dcc.Tab(label='Resumo',value='tab-1', children=[dropdown0,table],selected_style=tab_selected_style)
            
            # Info for tab2 Analise Individual
            list_empresas = kpi_empresas['Nome']
            dropdown = dcc.Dropdown(id='empresa-dropdown',options=[{'label': y, 'value': y} for y in list_empresas],
                                    # value=list_empresas.iloc[0],
                                     placeholder='Selecionar...',
                                    style={'width':'350px','fontSize':'14px',"marginBottom": "30px"})
            row2_1 = html.Div(id='output_initial')
            tab2 = dcc.Tab(label='Análise Individual',value='tab-2', children=[dropdown,row2_1], selected_style=tab_selected_style)
            
            
                            
            row1 = dcc.Tabs(id='tabs',children=[tab1,tab2],style={'width':'350px','height':'20px',"display": "flex",
                                                                  "alignItems": "center", "justifyContent": "center",
                                                                  "marginBottom": "20px",'fontSize':'14px'})
            # content = html.Div([row0,row1])
                # return content
    
            return row1
            # dash_app.layout = html.Div([row0,row1])
            # dash_app.layout = html.Div([
            #     dcc.Interval(
            #         id='graph-update',
            #         interval=1000,  # Update every 1 second
            #         n_intervals=0,
            #         ),
            #     html.Div(id='dashboard-content')
            # ])
            # dash_app.layout = content

    
    
    # A PARTIR DAQUI COPIEI AGORA
    #Define the callback to sort the table of the KPI in tab Resumo
    @dash_app.callback(Output('table_kpi', 'children'),
                       Input('sort-by', 'value'))
    def sort_table(sort_by):
        
        df_kpi=pd.read_excel('static/db/kpi.xlsx',usecols=[i for i in range(1,8)])
        df_kpi['Ano'] = df_kpi['Ano'].astype(str)
        df_kpi['TrimAno']= df_kpi['Trim']+df_kpi['Ano']
        df_kpi_pvt = df_kpi.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='KPI',values='Valor',aggfunc='sum')
        df_kpi_pvt.reset_index(inplace=True)  

        df_kpi_pvt['Data']=pd.to_datetime(df_kpi_pvt['Data'])
        df_kpi_pvt.sort_values('Data',inplace=True)
        kpi_empresas = df_kpi_pvt.drop_duplicates(subset=['Nome'],keep='last')
        kpi_empresas = round(kpi_empresas,4)
        kpi_empresas.drop(columns=['Data','Trim','Ano'],inplace=True)

        
        sorted_df = kpi_empresas.sort_values(by=sort_by,ascending=False)
        return [
            html.Thead(
                html.Tr([html.Th(col) for col in sorted_df.columns])
            ),
            html.Tbody(
                [
                    html.Tr(
                        [html.Td(sorted_df.iloc[i][col]) for col in sorted_df.columns]
                    )
                    for i in range(len(sorted_df))
                ]
            )
        ]

               

    # Define the callback to update the info in Tab 2 Análise individual
    @dash_app.callback(Output('output_initial', 'children'),
                       Input('empresa-dropdown', 'value'))
    def update_tab_analise_individual(value):

        df = pd.read_excel('static/db/pcl.xlsx',usecols=[i for i in range(1,9)])
        df['Ano'] = df['Ano'].astype(str)
        df['TrimAno']= df['Trim']+df['Ano']
        
        # KPIs
        # df_kpi=pd.read_excel('static/data.xlsx',sheet_name='kpi2')
        # df_kpi['Year'] = df_kpi['Year'].astype(str)    
        df_kpi=pd.read_excel('static/db/kpi.xlsx',usecols=[i for i in range(1,8)])
        df_kpi['Ano'] = df_kpi['Ano'].astype(str)
        df_kpi['TrimAno']= df_kpi['Trim']+df_kpi['Ano']
        df_kpi_pvt = df_kpi.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='KPI',values='Valor',aggfunc='sum')
        df_kpi_pvt.reset_index(inplace=True)  
        
        # Rubricas de custos (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_custos=pd.read_excel('static/db/custos.xlsx',usecols=[i for i in range(1,9)])
        df_custos['Ano'] = df_custos['Ano'].astype(str)
        df_custos['TrimAno']= df_custos['Trim']+df_custos['Ano']
        df_custos_pvt = df_custos.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Net_Debit_Amt',aggfunc='sum')
        df_custos_pvt.reset_index(inplace=True)
        # filtered_arr = np.array([elem[0] if elem[1] == '' else elem[1] for elem in df_custos_pvt])
        # df_custos_pvt.columns = filtered_arr
        
        # Rubricas de proveitos (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_proveitos=pd.read_excel('static/db/proveitos.xlsx',usecols=[i for i in range(1,9)])
        df_proveitos['Ano'] = df_proveitos['Ano'].astype(str)
        df_proveitos['TrimAno']= df_proveitos['Trim']+df_proveitos['Ano']
        df_proveitos_pvt = df_proveitos.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Net_Credit_Amt',aggfunc='sum')
        df_proveitos_pvt.reset_index(inplace=True)
        # filtered_arr = np.array([elem[0] if elem[1] == '' else elem[1] for elem in df_proveitos_pvt])
        # df_proveitos_pvt.columns = filtered_arr
        
        # Rubricas de fornecedores (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_fornecedores=pd.read_excel('static/db/fornecedores.xlsx',usecols=[i for i in range(1,9)])
        df_fornecedores['Ano'] = df_fornecedores['Ano'].astype(str)
        df_fornecedores['TrimAno']= df_fornecedores['Trim']+df_fornecedores['Ano']
        df_fornecedores_pvt = df_fornecedores.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Credit_Amt',aggfunc='sum')
        df_fornecedores_pvt.reset_index(inplace=True)
        # filtered_arr = np.array([elem[0] if elem[1] == '' else elem[1] for elem in df_fornecedores_pvt])
        # df_fornecedores_pvt.columns = filtered_arr
        
        # Rubricas de clientes (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_clientes=pd.read_excel('static/db/clientes.xlsx',usecols=[i for i in range(1,9)])
        df_clientes['Ano'] = df_clientes['Ano'].astype(str)
        df_clientes['TrimAno']= df_clientes['Trim']+df_clientes['Ano']
        df_clientes_pvt = df_clientes.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Debit_Amt',aggfunc='sum')
        df_clientes_pvt.reset_index(inplace=True)
        # filtered_arr = np.array([elem[0] if elem[1] == '' else elem[1] for elem in df_clientes_pvt])
        # df_clientes_pvt.columns = filtered_arr

        # RUbricas de investimentos (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_investimentos = pd.read_excel('static/db/investimentos.xlsx',usecols=[i for i in range(1,9)])
        df_investimentos['Ano'] = df_investimentos['Ano'].astype(str)
        df_investimentos['TrimAno']= df_investimentos['Trim']+df_investimentos['Ano']
        df_investimentos_pvt = df_investimentos.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Amount',aggfunc='sum')
        df_investimentos_pvt.reset_index(inplace=True)


        df_kpi_pvt['Data']=pd.to_datetime(df_kpi_pvt['Data'])
        df_kpi_pvt.sort_values('Data',inplace=True)
        kpi_empresas = df_kpi_pvt.drop_duplicates(subset=['Nome'],keep='last')
        kpi_empresas = round(kpi_empresas,4)
        kpi_empresas.drop(columns=['Data','Trim','Ano'],inplace=True)
        
        # Prepare info for tab2.1 KPI's inside Analise Individual
        temp_df_kpi = df_kpi_pvt[df_kpi_pvt['Nome']==value]
        
        tab21_info = html.Div([dcc.DatePickerRange(
                id='date-picker-range1',
                min_date_allowed=temp_df_kpi['Data'].min(),
                max_date_allowed=temp_df_kpi['Data'].max(),
                initial_visible_month=temp_df_kpi['Data'].min(),
                start_date=temp_df_kpi['Data'].min(),
                end_date=temp_df_kpi['Data'].max(),
                style=date_picker_style
            ),
            html.Div([
            html.H6 ('Evolução Anual dos KPIs'),
            dcc.Graph(
                id='yearly-bar-chart-kpi',
                figure={
                    'data': [
                        go.Bar(
                            x=temp_df_kpi['TrimAno'],
                            y=temp_df_kpi['CurrentRatio'],
                            name='Current Ratio',
                            marker={'color':colors[0]}
                        ),
                        go.Bar(
                            x=temp_df_kpi['TrimAno'],
                            y=temp_df_kpi['DebtToAssets'],
                            name='Debt-to-Assets',
                            marker={'color':colors[1]}
                        ),
                        go.Bar(
                            x=temp_df_kpi['TrimAno'],
                            y=temp_df_kpi['NetDebtToEBITDA'],
                            name='Net Debt-to-EBITDA',
                            marker={'color':colors[2]}
                        ),
                        go.Bar(
                            x=temp_df_kpi['TrimAno'],
                            y=temp_df_kpi['EBITDAMargin'],
                            name='EBITDA Margin',
                            marker={'color':colors[3]}
                        ),
                        go.Bar(
                            x=temp_df_kpi['TrimAno'],
                            y=temp_df_kpi['ReturnOnAssets'],
                            name='Return-on-Assets',
                            marker={'color':colors[4]}
                        ),
                        go.Bar(
                            x=temp_df_kpi['TrimAno'],
                            y=temp_df_kpi['ReturnOnEquity'],
                            name='Return-on-Equity',
                            marker={'color':colors[5]}
                        ),
                        go.Bar(
                            x=temp_df_kpi['TrimAno'],
                            y=temp_df_kpi['CFOtoSales'],
                            name='CFO-to-Sales',
                            marker={'color':colors[6]}
                        )
                    ],
                    'layout': go.Layout(
                        barmode='group'
                    )
                }
            )
        ]),
        
        # Second bar chart
        html.Div([
            html.H6('KPIs: fotografia do ano'),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': y, 'value': y} for y in temp_df_kpi['Ano'].unique()],
                value=temp_df_kpi['Ano'].min(),
                style={'width':'350px','fontSize':'14px',"marginBottom": "30px"}
            ),
            dcc.Graph(
                id='yearly2-bar-chart-kpi'
                )
            ])
        ])
        
        tab21 = dcc.Tab(label='KPIs',value='tab-21', children=[tab21_info],selected_style=tab_selected_style)
        
        # Prepare info for tab2.2 Demonstração Resultados inside Analise Individual
        temp_df = df[df['Nome']==value]
        if temp_df.empty==False:

        
            temp_df['Data']=pd.to_datetime(temp_df['Data'])
            temp_df.sort_values('Data',inplace=True)
            
            tab22_info = html.Div([dcc.DatePickerRange(
                    id='date-picker-range2',
                    min_date_allowed=temp_df['Data'].min(),
                    max_date_allowed=temp_df['Data'].max(),
                    initial_visible_month=temp_df['Data'].min(),
                    start_date=temp_df['Data'].min(),
                    end_date=temp_df['Data'].max(),
                    style=date_picker_style
                ),
                html.Div([
                html.H6 ('Evolução trimestral dos Proveitos, Custos e Lucros'),
                dcc.Graph(
                    id='quarterly-bar-chart',
                    figure={
                        'data': [
                            go.Bar(
                                x=temp_df['TrimAno'],
                                y=temp_df['Proveitos'],
                                name='Proveitos',
                                marker={'color':colors[0]}
                            ),
                            go.Bar(
                                x=temp_df['TrimAno'],
                                y=temp_df['Custos'],
                                name='Custos',
                                marker={'color':colors[1]}
                            ),
                            go.Bar(
                                x=temp_df['TrimAno'],
                                y=temp_df['Lucros'],
                                name='Lucros',
                                marker={'color':colors[2]}
                            )
                        ],
                        'layout': go.Layout(
                            barmode='group'
                        )
                    }
                )
            ]),
            
            # Second bar chart
            html.Div([
                html.H6('Proveitos, Custos e Lucros num período específico'),
                dcc.Dropdown(
                    id='quarter-dropdown',
                    options=[{'label': y, 'value': y} for y in np.append(temp_df['Trim'].unique(),['Ano Inteiro'])],
                    value=temp_df['Trim'].min(),
                    style={'width':'350px','fontSize':'14px',"marginBottom": "30px"}
                ),
                dcc.Graph(
                    id='quarterly2-bar-chart'
                    )
                ])
            ])
            tab22 = dcc.Tab(label='Demonstração de Resultados',value='tab-22', children=[tab22_info],selected_style=tab_selected_style)
        
        else:
            tab22 = dcc.Tab(label='Demonstração de Resultados',value='tab-22', children=[html.H6('Não existem custos e proveitos.')],selected_style=tab_selected_style)

        
        #value='Empresa 1'
        # Prepare info for tab2.3 Custos inside Analise Individual
        temp_df = df_custos_pvt[df_custos_pvt['Nome']==value]
        if temp_df.empty==False:

            temp_df['Data']=pd.to_datetime(temp_df['Data'])
            temp_df.sort_values('Data',inplace=True)
            temp_df.dropna(axis='columns',how='all',inplace=True)
    
            
            
            tab23_info = html.Div([dcc.DatePickerRange(
                    id='date-picker-range3',
                    min_date_allowed=temp_df['Data'].min(),
                    max_date_allowed=temp_df['Data'].max(),
                    initial_visible_month=temp_df['Data'].min(),
                    start_date=temp_df['Data'].min(),
                    end_date=temp_df['Data'].max(),
                    style=date_picker_style
                ),
                html.Div([
                html.H6 ('Evolução trimestral dos Custos'),
                dcc.Graph(
                    id='quarterly-bar-chart_costs',
                    figure={
                        'data': [go.Bar(
                                    x=temp_df['TrimAno'],
                                    y=temp_df[j],
                                    name=j,
                                    marker={'color':colors[i]}
                                ) for i,j in enumerate(temp_df.columns[5:])],
                            'layout': go.Layout(barmode='group')}
                )
            ]),
            
            # Second bar chart
            html.Div([
                html.H6('Custos num período específico'),
                dcc.Dropdown(
                    id='quarter-dropdown2',
                    options=[{'label': y, 'value': y} for y in np.append(temp_df['Trim'].unique(),['Ano Inteiro'])],
                    value=temp_df['Trim'].min(),
                    style={'width':'350px','fontSize':'14px',"marginBottom": "30px"}
                ),
                dcc.Graph(
                    id='quarterly3-bar-chart'
                    )
                ])
            ])
            tab23 = dcc.Tab(label='Custos',value='tab-23', children=[tab23_info],selected_style=tab_selected_style)
        else:
            tab23 = dcc.Tab(label='Custos',value='tab-23', children=[html.H6('Não existem custos.')],selected_style=tab_selected_style)

         
        # Prepare info for tab2.4 Proveitos inside Analise Individual
       
        temp_df = df_proveitos_pvt[df_proveitos_pvt['Nome']==value]
        if temp_df.empty==False:
      
            temp_df['Data']=pd.to_datetime(temp_df['Data'])
            temp_df.sort_values('Data',inplace=True)
            temp_df.dropna(axis='columns',how='all',inplace=True)
    
    
            
            tab24_info = html.Div([dcc.DatePickerRange(
                    id='date-picker-range4',
                    min_date_allowed=temp_df['Data'].min(),
                    max_date_allowed=temp_df['Data'].max(),
                    initial_visible_month=temp_df['Data'].min(),
                    start_date=temp_df['Data'].min(),
                    end_date=temp_df['Data'].max(),
                    style=date_picker_style
                ),
                html.Div([
                html.H6 ('Evolução trimestral dos Proveitos'),
                dcc.Graph(
                    id='quarterly-bar-chart_revenues',
                    figure={
                        'data': [go.Bar(
                                    x=temp_df['TrimAno'],
                                    y=temp_df[j],
                                    name=j,
                                    marker={'color':colors[i]}
                                ) for i,j in enumerate(temp_df.columns[5:])],
                            'layout': go.Layout(barmode='group')}
                )
            ]),
            
            # Second bar chart
            html.Div([
                html.H6('Proveitos num período específico'),
                dcc.Dropdown(
                    id='quarter-dropdown3',
                    options=[{'label': y, 'value': y} for y in np.append(temp_df['Trim'].unique(),['Ano Inteiro'])],
                    value=temp_df['Trim'].min(),
                    style={'width':'350px','fontSize':'14px',"marginBottom": "30px"}
                ),
                dcc.Graph(
                    id='quarterly4-bar-chart'
                    )
                ])
            ])
            tab24 = dcc.Tab(label='Proveitos',value='tab-24', children=[tab24_info],selected_style=tab_selected_style)
        
        else:
            tab24 = dcc.Tab(label='Proveitos',value='tab-24', children=[html.H6('Não existem proveitos.')],selected_style=tab_selected_style)

        
        # Prepare info for tab2.5 Fornecedores inside Analise Individual
        temp_df = df_fornecedores_pvt[df_fornecedores_pvt['Nome']==value]
        if temp_df.empty==False:

            temp_df['Data']=pd.to_datetime(temp_df['Data'])
            temp_df.sort_values('Data',inplace=True)
            temp_df.dropna(axis='columns',how='all',inplace=True)
    
    
            
            tab25_info = html.Div([dcc.DatePickerRange(
                    id='date-picker-range5',
                    min_date_allowed=temp_df['Data'].min(),
                    max_date_allowed=temp_df['Data'].max(),
                    initial_visible_month=temp_df['Data'].min(),
                    start_date=temp_df['Data'].min(),
                    end_date=temp_df['Data'].max(),
                    style=date_picker_style
                ),
                html.Div([
                html.H6 ('Evolução trimestral dos Fornecedores'),
                dcc.Graph(
                    id='quarterly-bar-chart_suppliers',
                    figure={
                        'data': [go.Bar(
                                    x=temp_df['TrimAno'],
                                    y=temp_df[j],
                                    name=j,
                                    marker={'color':colors[i]}
                                ) for i,j in enumerate(temp_df.columns[5:])],
                            'layout': go.Layout(barmode='group')}
                )
            ]),
            
            # Second bar chart
            html.Div([
                html.H6('Fornecedores num período específico'),
                dcc.Dropdown(
                    id='quarter-dropdown4',
                    options=[{'label': y, 'value': y} for y in np.append(temp_df['Trim'].unique(),['Ano Inteiro'])],
                    value=temp_df['Trim'].min(),
                    style={'width':'350px','fontSize':'14px',"marginBottom": "30px"}
                ),
                dcc.Graph(
                    id='quarterly5-bar-chart'
                    )
                ])
            ])
            tab25 = dcc.Tab(label='Fornecedores',value='tab-25', children=[tab25_info],selected_style=tab_selected_style)
        else:
            tab25 = dcc.Tab(label='Fornecedores',value='tab-25', children=[html.H6('Não existem fornecedores.')],selected_style=tab_selected_style)

        
        # Prepare info for tab2.6 Clientes inside Analise Individual
        temp_df = df_clientes_pvt[df_clientes_pvt['Nome']==value]
        if temp_df.empty==False:

            temp_df['Data']=pd.to_datetime(temp_df['Data'])
            temp_df.sort_values('Data',inplace=True)
            temp_df.dropna(axis='columns',how='all',inplace=True)
    
    
            
            tab26_info = html.Div([dcc.DatePickerRange(
                    id='date-picker-range6',
                    min_date_allowed=temp_df['Data'].min(),
                    max_date_allowed=temp_df['Data'].max(),
                    initial_visible_month=temp_df['Data'].min(),
                    start_date=temp_df['Data'].min(),
                    end_date=temp_df['Data'].max(),
                    style=date_picker_style
                ),
                html.Div([
                html.H6 ('Evolução trimestral dos Clientes'),
                dcc.Graph(
                    id='quarterly-bar-chart_clients',
                    figure={
                        'data': [go.Bar(
                                    x=temp_df['TrimAno'],
                                    y=temp_df[j],
                                    name=j,
                                    marker={'color':colors[i]}
                                ) for i,j in enumerate(temp_df.columns[5:])],
                            'layout': go.Layout(barmode='group')}
                )
            ]),
            
            # Second bar chart
            html.Div([
                html.H6('Clientes num período específico'),
                dcc.Dropdown(
                    id='quarter-dropdown5',
                    options=[{'label': y, 'value': y} for y in np.append(temp_df['Trim'].unique(),['Ano Inteiro'])],
                    value=temp_df['Trim'].min(),
                    style={'width':'350px','fontSize':'14px',"marginBottom": "30px"}
                ),
                dcc.Graph(
                    id='quarterly6-bar-chart'
                    )
                ])
            ])
            tab26 = dcc.Tab(label='Clientes',value='tab-26', children=[tab26_info],selected_style=tab_selected_style)
        
        else:
            tab26 = dcc.Tab(label='Clientes',value='tab-26', children=[html.H6('Não existem clientes.')],selected_style=tab_selected_style)

        
        # Prepare info for tab2.7 Investimentos inside Analise Individual
        temp_df = df_investimentos_pvt[df_investimentos_pvt['Nome']==value]
        if temp_df.empty==False:

            temp_df['Data']=pd.to_datetime(temp_df['Data'])
            temp_df.sort_values('Data',inplace=True)
            temp_df.dropna(axis='columns',how='all',inplace=True)
    
    
            
            tab27_info = html.Div([dcc.DatePickerRange(
                    id='date-picker-range7',
                    min_date_allowed=temp_df['Data'].min(),
                    max_date_allowed=temp_df['Data'].max(),
                    initial_visible_month=temp_df['Data'].min(),
                    start_date=temp_df['Data'].min(),
                    end_date=temp_df['Data'].max(),
                    style=date_picker_style
                ),
                html.Div([
                html.H6 ('Evolução trimestral dos Investimentos'),
                dcc.Graph(
                    id='quarterly-bar-chart_investments',
                    figure={
                        'data': [go.Bar(
                                    x=temp_df['TrimAno'],
                                    y=temp_df[j],
                                    name=j,
                                    marker={'color':colors[i]}
                                ) for i,j in enumerate(temp_df.columns[5:])],
                            'layout': go.Layout(barmode='group')}
                )
            ]),
            
            # Second bar chart
            html.Div([
                html.H6('Investimentos num período específico'),
                dcc.Dropdown(
                    id='quarter-dropdown6',
                    options=[{'label': y, 'value': y} for y in np.append(temp_df['Trim'].unique(),['Ano Inteiro'])],
                    value=temp_df['Trim'].min(),
                    style={'width':'350px','fontSize':'14px',"marginBottom": "30px"}
                ),
                dcc.Graph(
                    id='quarterly7-bar-chart'
                    )
                ])
            ])
            tab27 = dcc.Tab(label='Investimentos',value='tab-27', children=[tab27_info],selected_style=tab_selected_style)
        else:
            tab27 = dcc.Tab(label='Investimentos',value='tab-27', children=[html.H6('Não existem investimentos.')],selected_style=tab_selected_style)

        
        
        
        
        
        # Compile all the tabs in one dcc.Tabs instantce:
            
        row0 = dcc.Tabs(id='tabs2', children=[tab21,tab22,tab23,tab24,tab25,tab26,tab27],
                        style={'height':'20px',"display": "flex","alignItems": "center","justifyContent": "center",
                                "marginBottom": "20px",'fontSize':'14px'})
        
        # row0 = dcc.Tabs(id='tabs2', children=[tab21,tab22,tab23,tab24,tab25,tab26,tab27],
        #                 style={'height':'20px',"display": "flex","alignItems": "center","justifyContent": "center",
        #                        "marginBottom": "20px"})

        
        return row0 


    # Define the callback to update the info in Tab 2 Análise individual, KPI
    @dash_app.callback(
        [Output('yearly-bar-chart-kpi', 'figure'), Output('yearly2-bar-chart-kpi', 'figure')],
        [Input('year-dropdown', 'value'),
         Input('date-picker-range1', 'start_date'),
         Input('date-picker-range1', 'end_date'),
         Input('empresa-dropdown', 'value')])

    def update_charts_kpi(year, start_date, end_date,value):
        
        # KPIs
        # df_kpi=pd.read_excel('static/data.xlsx',sheet_name='kpi2')
        # df_kpi['Year'] = df_kpi['Year'].astype(str)    
        df_kpi=pd.read_excel('static/db/kpi.xlsx',usecols=[i for i in range(1,8)])
        df_kpi['Ano'] = df_kpi['Ano'].astype(str)
        df_kpi['TrimAno']= df_kpi['Trim']+df_kpi['Ano']
        df_kpi_pvt = df_kpi.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='KPI',values='Valor',aggfunc='sum')
        df_kpi_pvt.reset_index(inplace=True)  

        
        temp_df_kpi = df_kpi_pvt[df_kpi_pvt['Nome']==value]
        temp_df_kpi['Data']=pd.to_datetime(temp_df_kpi['Data'])
        temp_df_kpi.sort_values('Data',inplace=True)

        filtered_df = temp_df_kpi[(temp_df_kpi['Data']>=start_date) & (temp_df_kpi['Data']<=end_date)] 

        # Update the time series bar chart
        quarterly_bar_data = [
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['CurrentRatio'],
                name='Current Ratio',
                marker={'color':colors[0]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['DebtToAssets'],
                name='Debt-to-Assets',
                marker={'color':colors[1]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['NetDebtToEBITDA'],
                name='Net Debt-to-EBITDA',
                marker={'color':colors[2]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['EBITDAMargin'],
                name='EBITDA Margin',
                marker={'color':colors[3]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['ReturnOnAssets'],
                name='Return-on-Assets',
                marker={'color':colors[4]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['ReturnOnEquity'],
                name='Return-on-Equity',
                marker={'color':colors[5]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['CFOtoSales'],
                name='CFO-to-Sales',
                marker={'color':colors[6]}
            )
        ]
        quarterly_bar_layout = go.Layout(
            xaxis=dict(title='Trimestre'),
            yaxis=dict(title='Valor'),
            barmode='group',
            margin=dict(t=50)
        )

        year_df = filtered_df[filtered_df['TrimAno']==year]
        
        quarter_bar_data = go.Figure()
        for i,year in enumerate(year_df['Ano'].unique()):
            quarter_bar_data.add_trace(go.Bar(x=['KPI 1', 'KPI 2', 'KPI 3', 'KPI 4','KPI 5'], 
                                              y=year_df.loc[year_df['Year']==year][['KPI 1', 'KPI 2', 'KPI 3', 'KPI 4','KPI 5']].values[0],
                                              name=str(year),marker={'color':colors[i]}))
            quarter_bar_data.update_xaxes(type='category')

        quarter_bar_data.update_layout(title='Dados de: '+year, barmode='group')            
            
        quarter_bar_figure = go.Figure(data=quarter_bar_data)#, layout=quarter_bar_layout)
        yearly_bar_figure = go.Figure(data=quarterly_bar_data, layout=quarterly_bar_layout)

        return yearly_bar_figure, quarter_bar_figure




    # Define the callback to update the info in Tab 2 Análise individual, Demonstração Resultados
    @dash_app.callback(
        [Output('quarterly-bar-chart', 'figure'), Output('quarterly2-bar-chart', 'figure')],
        [Input('quarter-dropdown', 'value'),
         Input('date-picker-range2', 'start_date'),
         Input('date-picker-range2', 'end_date'),
         Input('empresa-dropdown', 'value')])

    def update_charts_dr(quarter, start_date, end_date,value):

        df = pd.read_excel('static/db/pcl.xlsx',usecols=[i for i in range(1,9)])
        df['Ano'] = df['Ano'].astype(str)
        df['TrimAno']= df['Trim']+df['Ano']


        temp_df = df[df['Nome']==value]
        temp_df.dropna(axis='columns',inplace=True)
        temp_df['Data']=pd.to_datetime(temp_df['Data'])
        temp_df.sort_values('Data',inplace=True)

        filtered_df = temp_df[(temp_df['Data']>=start_date) & (temp_df['Data']<=end_date)]

        # Update the time series bar chart
        quarterly_bar_data = [
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['Proveitos'],
                name='Proveitos',
                marker={'color':colors[0]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['Custos'],
                name='Custos',
                marker={'color':colors[1]}
            ),
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df['Lucros'],
                name='Lucros',
                marker={'color':colors[2]}
            )
        ]
        quarterly_bar_layout = go.Layout(
            xaxis=dict(title='Trimestre'),
            yaxis=dict(title='Valor'),
            barmode='group',
            margin=dict(t=50)
        )

        
        x1 = ['Proveitos', 'Custos', 'Lucros']
        if quarter != 'Ano Inteiro':
            quarter_df = filtered_df[filtered_df['Trim']==quarter]
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=x1, y=quarter_df.loc[quarter_df['Ano']==year][x1].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

        else:
            quarter_df = filtered_df.groupby(['Ano'],as_index=False).sum()
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=x1, y=quarter_df.loc[quarter_df['Ano']==year][x1].values[0], name=str(year),
                                                  marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

        
            
        quarter_bar_figure = go.Figure(data=quarter_bar_data)#, layout=quarter_bar_layout)
        yearly_bar_figure = go.Figure(data=quarterly_bar_data, layout=quarterly_bar_layout)

        return yearly_bar_figure, quarter_bar_figure

    # Define the callback to update the info in Tab 2 Análise individual, Custos
    @dash_app.callback(
        [Output('quarterly-bar-chart_costs', 'figure'), Output('quarterly3-bar-chart', 'figure')],
        [Input('quarter-dropdown2', 'value'),
         Input('date-picker-range3', 'start_date'),
         Input('date-picker-range3', 'end_date'),
         Input('empresa-dropdown', 'value')])

    def update_charts_custos(quarter, start_date, end_date,value):
        
        # Rubricas de custos (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_custos=pd.read_excel('static/db/custos.xlsx',usecols=[i for i in range(1,9)])
        df_custos['Ano'] = df_custos['Ano'].astype(str)
        df_custos['TrimAno']= df_custos['Trim']+df_custos['Ano']
        df_custos_pvt = df_custos.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Net_Debit_Amt',aggfunc='sum')
        df_custos_pvt.reset_index(inplace=True)

        
        # value = 'Empresa 2'
        # value = df_custos_pvt['Nome'].iloc[1]
        temp_df = df_custos_pvt[df_custos_pvt['Nome']==value]
        temp_df.dropna(axis='columns',how='all',inplace=True)
        temp_df['Data']=pd.to_datetime(temp_df['Data'])
        temp_df.sort_values('Data',inplace=True)

        filtered_df = temp_df[(temp_df['Data']>=start_date) & (temp_df['Data']<=end_date)]

        # Update the time series bar chart
        quarterly_bar_data = [
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df[j],
                name=j,
                marker={'color':colors[i]}
            ) for i,j in enumerate(temp_df.columns[5:])]
        quarterly_bar_layout = go.Layout(
            xaxis=dict(title='Trimestre'),
            yaxis=dict(title='Valor'),
            barmode='group',
            margin=dict(t=50)
        )
        # quarter = 'Ano Inteiro'
        
        if quarter != 'Ano Inteiro':
            quarter_df = filtered_df[filtered_df['Trim']==quarter]
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=temp_df.columns[5:], y=quarter_df.loc[quarter_df['Ano']==year][temp_df.columns[5:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

        else:
            quarter_df = filtered_df.groupby(['Ano'],as_index=False).sum()
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=quarter_df.columns[1:], y=quarter_df.loc[quarter_df['Ano']==year][quarter_df.columns[1:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

            
        quarter_bar_figure = go.Figure(data=quarter_bar_data)#, layout=quarter_bar_layout)
        yearly_bar_figure = go.Figure(data=quarterly_bar_data, layout=quarterly_bar_layout)

        return yearly_bar_figure, quarter_bar_figure

    # Define the callback to update the info in Tab 2 Análise individual, Proveitos
    @dash_app.callback(
        [Output('quarterly-bar-chart_revenues', 'figure'), Output('quarterly4-bar-chart', 'figure')],
        [Input('quarter-dropdown3', 'value'),
         Input('date-picker-range4', 'start_date'),
         Input('date-picker-range4', 'end_date'),
         Input('empresa-dropdown', 'value')])

    def update_charts_proveitos(quarter, start_date, end_date,value):

        # Rubricas de proveitos (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_proveitos=pd.read_excel('static/db/proveitos.xlsx',usecols=[i for i in range(1,9)])
        df_proveitos['Ano'] = df_proveitos['Ano'].astype(str)
        df_proveitos['TrimAno']= df_proveitos['Trim']+df_proveitos['Ano']
        df_proveitos_pvt = df_proveitos.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Net_Credit_Amt',aggfunc='sum')
        df_proveitos_pvt.reset_index(inplace=True)


        temp_df = df_proveitos_pvt[df_proveitos_pvt['Nome']==value]
        temp_df.dropna(axis='columns',how='all',inplace=True)
        temp_df['Data']=pd.to_datetime(temp_df['Data'])
        temp_df.sort_values('Data',inplace=True)

        filtered_df = temp_df[(temp_df['Data']>=start_date) & (temp_df['Data']<=end_date)]

        # Update the time series bar chart
        quarterly_bar_data = [
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df[j],
                name=j,
                marker={'color':colors[i]}
            ) for i,j in enumerate(temp_df.columns[5:])]
        quarterly_bar_layout = go.Layout(
            xaxis=dict(title='Trimestre'),
            yaxis=dict(title='Valor'),
            barmode='group',
            margin=dict(t=50)
        )

        if quarter != 'Ano Inteiro':
            quarter_df = filtered_df[filtered_df['Trim']==quarter]
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=temp_df.columns[5:], y=quarter_df.loc[quarter_df['Ano']==year][temp_df.columns[5:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

        else:
            quarter_df = filtered_df.groupby(['Ano'],as_index=False).sum()
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=quarter_df.columns[1:], y=quarter_df.loc[quarter_df['Ano']==year][quarter_df.columns[1:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            
            
        quarter_bar_figure = go.Figure(data=quarter_bar_data)#, layout=quarter_bar_layout)
        yearly_bar_figure = go.Figure(data=quarterly_bar_data, layout=quarterly_bar_layout)

        return yearly_bar_figure, quarter_bar_figure

    # Define the callback to update the info in Tab 2 Análise individual, Fornecedores
    @dash_app.callback(
        [Output('quarterly-bar-chart_suppliers', 'figure'), Output('quarterly5-bar-chart', 'figure')],
        [Input('quarter-dropdown4', 'value'),
         Input('date-picker-range5', 'start_date'),
         Input('date-picker-range5', 'end_date'),
         Input('empresa-dropdown', 'value')])

    def update_charts_fornecedores(quarter, start_date, end_date,value):

        # Rubricas de fornecedores (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_fornecedores=pd.read_excel('static/db/fornecedores.xlsx',usecols=[i for i in range(1,9)])
        df_fornecedores['Ano'] = df_fornecedores['Ano'].astype(str)
        df_fornecedores['TrimAno']= df_fornecedores['Trim']+df_fornecedores['Ano']
        df_fornecedores_pvt = df_fornecedores.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Credit_Amt',aggfunc='sum')
        df_fornecedores_pvt.reset_index(inplace=True)

        
        temp_df = df_fornecedores_pvt[df_fornecedores_pvt['Nome']==value]
        temp_df.dropna(axis='columns',how='all',inplace=True)
        temp_df['Data']=pd.to_datetime(temp_df['Data'])
        temp_df.sort_values('Data',inplace=True)

        filtered_df = temp_df[(temp_df['Data']>=start_date) & (temp_df['Data']<=end_date)]

        # Update the time series bar chart
        quarterly_bar_data = [
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df[j],
                name=j,
                marker={'color':colors[i]}
            ) for i,j in enumerate(temp_df.columns[5:])]
        quarterly_bar_layout = go.Layout(
            xaxis=dict(title='Trimestre'),
            yaxis=dict(title='Valor'),
            barmode='group',
            margin=dict(t=50)
        )

        if quarter != 'Ano Inteiro':
            quarter_df = filtered_df[filtered_df['Trim']==quarter]
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=temp_df.columns[5:], y=quarter_df.loc[quarter_df['Ano']==year][temp_df.columns[5:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

        else:
            quarter_df = filtered_df.groupby(['Ano'],as_index=False).sum()
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=quarter_df.columns[1:], y=quarter_df.loc[quarter_df['Ano']==year][quarter_df.columns[1:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            
            
        quarter_bar_figure = go.Figure(data=quarter_bar_data)#, layout=quarter_bar_layout)
        yearly_bar_figure = go.Figure(data=quarterly_bar_data, layout=quarterly_bar_layout)

        return yearly_bar_figure, quarter_bar_figure

    # Define the callback to update the info in Tab 2 Análise individual, Clientes
    @dash_app.callback(
        [Output('quarterly-bar-chart_clients', 'figure'), Output('quarterly6-bar-chart', 'figure')],
        [Input('quarter-dropdown5', 'value'),
         Input('date-picker-range6', 'start_date'),
         Input('date-picker-range6', 'end_date'),
         Input('empresa-dropdown', 'value')])

    def update_charts_clientes(quarter, start_date, end_date,value):

        # Rubricas de clientes (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_clientes=pd.read_excel('static/db/clientes.xlsx',usecols=[i for i in range(1,9)])
        df_clientes['Ano'] = df_clientes['Ano'].astype(str)
        df_clientes['TrimAno']= df_clientes['Trim']+df_clientes['Ano']
        df_clientes_pvt = df_clientes.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Debit_Amt',aggfunc='sum')
        df_clientes_pvt.reset_index(inplace=True)


        
        temp_df = df_clientes_pvt[df_clientes_pvt['Nome']==value]
        temp_df.dropna(axis='columns',how='all',inplace=True)
        temp_df['Data']=pd.to_datetime(temp_df['Data'])
        temp_df.sort_values('Data',inplace=True)

        filtered_df = temp_df[(temp_df['Data']>=start_date) & (temp_df['Data']<=end_date)]

        # Update the time series bar chart
        quarterly_bar_data = [
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df[j],
                name=j,
                marker={'color':colors[i]}
            ) for i,j in enumerate(temp_df.columns[5:])]
        quarterly_bar_layout = go.Layout(
            xaxis=dict(title='Trimestre'),
            yaxis=dict(title='Valor'),
            barmode='group',
            margin=dict(t=50)
        )

        if quarter != 'Ano Inteiro':
            quarter_df = filtered_df[filtered_df['Trim']==quarter]
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=temp_df.columns[5:], y=quarter_df.loc[quarter_df['Ano']==year][temp_df.columns[5:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

        else:
            quarter_df = filtered_df.groupby(['Ano'],as_index=False).sum()
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=quarter_df.columns[1:], y=quarter_df.loc[quarter_df['Ano']==year][quarter_df.columns[1:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            
            
        quarter_bar_figure = go.Figure(data=quarter_bar_data)#, layout=quarter_bar_layout)
        yearly_bar_figure = go.Figure(data=quarterly_bar_data, layout=quarterly_bar_layout)

        return yearly_bar_figure, quarter_bar_figure
    
    
    # Define the callback to update the info in Tab 2 Análise individual, Investimentos
    @dash_app.callback(
        [Output('quarterly-bar-chart_investments', 'figure'), Output('quarterly7-bar-chart', 'figure')],
        [Input('quarter-dropdown6', 'value'),
         Input('date-picker-range7', 'start_date'),
         Input('date-picker-range7', 'end_date'),
         Input('empresa-dropdown', 'value')])

    def update_charts_investimentos(quarter, start_date, end_date,value):

        # Rubricas de clientes (funções que organizam os dados como nos dá jeito para os gráficos da aplicação)
        df_investimentos=pd.read_excel('static/db/investimentos.xlsx',usecols=[i for i in range(1,9)])
        df_investimentos['Ano'] = df_investimentos['Ano'].astype(str)
        df_investimentos['TrimAno']= df_investimentos['Trim']+df_investimentos['Ano']
        df_investimentos_pvt = df_investimentos.pivot_table(index=['Nome', 'Data', 'Trim', 'Ano','TrimAno'],columns='AccountDescription',values='Amount',aggfunc='sum')
        df_investimentos_pvt.reset_index(inplace=True)
        
        temp_df = df_investimentos_pvt[df_investimentos_pvt['Nome']==value]
        temp_df.dropna(axis='columns',how='all',inplace=True)
        temp_df['Data']=pd.to_datetime(temp_df['Data'])
        temp_df.sort_values('Data',inplace=True)

        
        filtered_df = temp_df[(temp_df['Data']>=start_date) & (temp_df['Data']<=end_date)]

        # Update the time series bar chart
        quarterly_bar_data = [
            go.Bar(
                x=filtered_df['TrimAno'],
                y=filtered_df[j],
                name=j,
                marker={'color':colors[i]}
            ) for i,j in enumerate(temp_df.columns[5:])]
        quarterly_bar_layout = go.Layout(
            xaxis=dict(title='Trimestre'),
            yaxis=dict(title='Valor'),
            barmode='group',
            margin=dict(t=50)
        )

        if quarter != 'Ano Inteiro':
            quarter_df = filtered_df[filtered_df['Trim']==quarter]
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=temp_df.columns[5:], y=quarter_df.loc[quarter_df['Ano']==year][temp_df.columns[5:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            

        else:
            quarter_df = filtered_df.groupby(['Ano'],as_index=False).sum()
            quarter_bar_data = go.Figure()
            for i,year in enumerate(quarter_df['Ano'].unique()):
                quarter_bar_data.add_trace(go.Bar(x=quarter_df.columns[1:], y=quarter_df.loc[quarter_df['Ano']==year][quarter_df.columns[1:]].values[0],
                                                  name=str(year),marker={'color':colors[i]}))
                quarter_bar_data.update_xaxes(type='category')

            quarter_bar_data.update_layout(title='Dados de: '+quarter, barmode='group')            
            
        quarter_bar_figure = go.Figure(data=quarter_bar_data)#, layout=quarter_bar_layout)
        yearly_bar_figure = go.Figure(data=quarterly_bar_data, layout=quarterly_bar_layout)

        return yearly_bar_figure, quarter_bar_figure
    
    return dash_app.server
    # return dash_app

