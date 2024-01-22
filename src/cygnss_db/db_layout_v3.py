from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_loading_spinners as dls
import dash_bootstrap_components as dbc

from datetime import date

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)




lef_date_range_picker = dcc.DatePickerRange(
    month_format='Y-M-D',
    end_date_placeholder_text='Y-M-D',
    start_date=date(2018, 8, 1),
    end_date=date(2018, 8, 1),
    min_date_allowed=date(2018, 8, 1),
    max_date_allowed=date(2021, 9, 30),
    minimum_nights=0,
    id='lef-date-range-picker',
 style={'textAlign':'center'}
)

rig_date_range_picker = dcc.DatePickerRange(
    month_format='Y-M-D',
    end_date_placeholder_text='Y-M-D',
    start_date=date(2018, 8, 1),
    end_date=date(2018, 12, 31),
    min_date_allowed=date(2018, 8, 1),
    max_date_allowed=date(2021, 9, 30),
    minimum_nights=0,
    id='rig-date-range-picker',
    style={'textAlign':'center'}
)


dlm_slider_date = dcc.Slider(
    id='dlm-sl-date',
    min=1,
    max=30,
    value=1,
    marks={1: '2018-08-01', 30: '2018-08-30'},
    tooltip={"placement": "bottom", "always_visible": False},
    step=1

)

dlm_checkboxes_timeseries_satellites = dcc.Checklist(
    options={'All': 'CYGNSS TS SM 36km (all sats)',
             'Selected': 'CYGNSS TS SM 36km (selected sats)',
             },
    value=[
        'All'],

    id='dlm-cl-ts-choices',
    # inline=True
)

lef_checkboxes_sat_combo_p1 = dcc.Checklist(
    options={'1': 'CYGNSS 1',
             '2': 'CYGNSS 2',
             '3': 'CYGNSS 3',
             '4': 'CYGNSS 4',
             # '5': 'CYGNSS 5',
             # '6': 'CYGNSS 6',
             # '7': 'CYGNSS 7',
             # '8': 'CYGNSS 8',
             },
    value=[
        '2'],

    id='lef-cl-sat-combo-p1',
    # inline=True
)

lef_checkboxes_sat_combo_p2 = dcc.Checklist(
    options={
        # '1': 'CYGNSS 1',
        #      '2': 'CYGNSS 2',
        #      '3': 'CYGNSS 3',
        #      '4': 'CYGNSS 4',
             '5': 'CYGNSS 5',
             '6': 'CYGNSS 6',
             '7': 'CYGNSS 7',
             '8': 'CYGNSS 8',
             },
    value=[
        ],

    id='lef-cl-sat-combo-p2',
    # inline=True
)


rig_checkboxes_sat_combo_p1 = dcc.Checklist(
    options={
        '1': 'CYGNSS 1',
             '2': 'CYGNSS 2',
             '3': 'CYGNSS 3',
             '4': 'CYGNSS 4',
             # '5': 'CYGNSS 5',
             # '6': 'CYGNSS 6',
             # '7': 'CYGNSS 7',
             # '8': 'CYGNSS 8',
             },
    value=[
        '1', '2', '3','4'],

    id='rig-cl-sat-combo-p1',
    # inline=True
)


rig_checkboxes_sat_combo_p2 = dcc.Checklist(
    options={
        # '1': 'CYGNSS 1',
        #      '2': 'CYGNSS 2',
        #      '3': 'CYGNSS 3',
        #      '4': 'CYGNSS 4',
             '5': 'CYGNSS 5',
             '6': 'CYGNSS 6',
             '7': 'CYGNSS 7',
             '8': 'CYGNSS 8',
             },
    value=[
        '5','6'],

    id='rig-cl-sat-combo-p2',
    # inline=True
)




# dlm_checkboxes_sat_combo = dcc.Checklist(
#                         options={'CYGNSS 1',
#                                  'CYGNSS 2',
#                                  'CYGNSS 3',
#                                 #  'CYGNSS 4',
#                                 #  'CYGNSS 5',
#                                 #  'CYGNSS 6',
#                                 #  'CYGNSS 7',
#                                 #  'CYGNSS 8',
#                                  },
#                         value=[
#                                'q'],

#                         id='dlm-cl-sat-combo',
#                         # inline=True
#                     )


# TODO make those 2 list of dicts like in the case of the dropdown
lef_ts_type_choice = dcc.RadioItems(
    id='lef-ts-type-choice',
    options={
        'density': 'Density   ',
        'scatter': 'Scatter   ',
        # 'pcp': 'PCP   ',

    },
    value='density',
    inline=True,
    style={'textAlign':'center'}
)

rig_ts_type_choice = dcc.RadioItems(
    id='rig-ts-type-choice',
    options={
        'density': 'Density   ',
        'scatter': 'Scatter   ',
        # 'pcp': 'PCP   ',
        # 'line': 'Line',

    },
    value='density',
    inline=True,
    style={'textAlign':'center'}
)


dlm_radio_grid_choice = dcc.RadioItems(
    id='dlm-ri-grid',
    options={

        # '9_EASE': '9 km',
        '25_EASE': '25 km',
        '36_EASE': '36 km',
    },
    value='36_EASE',
    inline=True
)



lef_dropdown_map_choice = dcc.Dropdown(
    id='lef-dd-choice',
    options=[
        # {'label': 'SM Retrievals', 'value': 'SM'},
        {'label': 'SM: Mean', 'value': 'mean'},
        {'label': 'SM: Std Deviation', 'value': 'std'},
        {'label': 'SM: Range', 'value': 'range'},
        {'label': 'SM: Max', 'value': 'max'},
        {'label': 'SM: Min', 'value': 'min'},
        {'label': 'N of Measurements', 'value': 'n_measurements'},
    ],
    value='mean'
)

rig_dropdown_map_choice = dcc.Dropdown(
    id='rig-dd-choice',
    options=[
        # {'label': 'SM Retrievals', 'value': 'SM'},
        {'label': 'SM: Mean', 'value': 'mean'},
        {'label': 'SM: Std Deviation', 'value': 'std'},
        {'label': 'SM: Range', 'value': 'range'},
        {'label': 'SM: Max', 'value': 'max'},
        {'label': 'SM: Min', 'value': 'min'},
        {'label': 'N of Measurements', 'value': 'n_measurements'},
    ],
    value='mean'
)


lef_imshow_map = dcc.Graph(
    id='lef-imshow-map',
    clickData={'points': [{'curveNumber': None, 'pointNumber': None, 'pointIndex': None, 'x': 321, 'y': 280,
                           'hovertext': None, 'marker.color': None,
                           'bbox': {'x0': None, 'x1': None, 'y0': None, 'y1': None}}]},
    config={'modeBarButtonsToAdd': ['select',
                                    'drawrect',
                                    'eraseshape'
                                    ]}
)

rig_imshow_map = dcc.Graph(
    id='rig-imshow-map',
    clickData={'points': [{'curveNumber': None, 'pointNumber': None, 'pointIndex': None, 'x': 321, 'y': 280,
                           'hovertext': None, 'marker.color': None,
                           'bbox': {'x0': None, 'x1': None, 'y0': None, 'y1': None}}]},
    config={'modeBarButtonsToAdd': ['select',
                                    'drawrect',
                                    'eraseshape'
                                    ]}
)

lef_hist = dcc.Graph(
    id='lef-hist',
    clickData={'points': [{'curveNumber': None, 'pointNumber': None, 'pointIndex': None, 'x': 1, 'y': 1,
                           'hovertext': None, 'marker.color': None,
                           'bbox': {'x0': None, 'x1': None, 'y0': None, 'y1': None}}]}
)

rig_hist = dcc.Graph(
    id='rig-hist',
    clickData={'points': [{'curveNumber': None, 'pointNumber': None, 'pointIndex': None, 'x': 1, 'y': 1,
                           'hovertext': None, 'marker.color': None,
                           'bbox': {'x0': None, 'x1': None, 'y0': None, 'y1': None}}]}
)


lef_ts_sm = dcc.Graph(id='lef-ts')
rig_ts_sm = dcc.Graph(id='rig-ts')

#################### LAYOUT


agg_title_row = dbc.Row(dbc.Col(
    html.Div(['CYGNSS SM Trackwise - Aggregate Measurements', html.P(id="agg-title")], style={'font-size': '26px'})
))


dlm_title_row = dbc.Row(dbc.Col(
    html.Div(['CYGNSS SM Data Explorer', html.P(id="dlm-title")], style={'font-size': '42px', 'textAlign':'center'})
))


dlm_options_row = dbc.Row(
    [
        #
        dbc.Col(
            [
                html.Div("Grid Choice"),
                html.Div(dlm_radio_grid_choice),
            ], width=12, style={'textAlign':'center'}
        ),


    ], justify='between', style ={"border-bottom": "4px solid black", 'margin-bottom':'20px'}
)


dlm_figures_row_date_picker = dlm_figures_row_opt = dbc.Row( #TODO rename
    [dbc.Col(
        html.Div([
            # html.Div(['Data Source Options', html.P()],
            #          style={'font-size': '20px', 'textAlign': 'center'}),
            # lef_date_range_picker,
            # lef_checkboxes_sat_combo,


        ])
    ),
        dbc.Col(
            html.Div([
# html.Div(['Data Source Options', html.P()],
#                      style={'font-size': '20px', 'textAlign': 'center'}),
                # rig_date_range_picker,
                # rig_checkboxes_sat_combo,



            ])
        )
    ]
)

dlm_figures_row_opt = dbc.Row(
    [dbc.Col(
        [html.Div([
            # lef_date_range_picker,
            # lef_checkboxes_sat_combo_p1,


        ])], width=3,
    ),
    dbc.Col(
        [html.Div([
            # lef_date_range_picker,
            # lef_checkboxes_sat_combo_p2,

        ])], width=3
    ),
    dbc.Col(
        html.Div([
            # rig_date_range_picker,
            # rig_checkboxes_sat_combo_p1,

        ])
    ),
        dbc.Col(
            html.Div([
                # rig_date_range_picker,
                # rig_checkboxes_sat_combo_p2,

            ])
        ),
    ]
)

dlm_figures_row_ts = dbc.Row(
    [dbc.Col(
            [html.Div([

                # lef_ts_type_choice,
                # dls.Moon(rig_ts_sm),
            ])
                ,html.Div([
                    html.Div(['SM Retrievals on Selected Volumes', html.P()],
                     style={'font-size': '20px', 'textAlign': 'center'}),
                lef_ts_type_choice,
                dls.Moon(lef_ts_sm),

            ])]
        ,style={'border-right':'2px solid black'}),
        dbc.Col(
            [html.Div([
                # rig_ts_type_choice,
                # dls.Moon(rig_ts_sm),
            ])
                ,html.Div([
                html.Div(['SM Retrievals on Selected Volumes', html.P()],
                     style={'font-size': '20px', 'textAlign': 'center'}),
                rig_ts_type_choice,
                dls.Moon(rig_ts_sm),
            ])]
        )
    ]
, style={ "border-top": "1px solid gray", 'margin-top': '20px'})


dlm_figures_row_map = dbc.Row(
    [dbc.Col(
        [html.Div([
            html.Div(['Aggregate Maps', html.P()]),
            dbc.Row([dbc.Col(width=4), dbc.Col([dbc.Row([dbc.Col(lef_checkboxes_sat_combo_p1),dbc.Col(lef_checkboxes_sat_combo_p2)]),
                                               lef_dropdown_map_choice,
                                                lef_date_range_picker],

                                               width=4), dbc.Col(width=4)]),

            # dls.Moon(lef_imshow_map),
        ])
            ,html.Div([
            # lef_dropdown_map_choice,
            dls.Moon(lef_imshow_map),
        ])]
    ,style={'margin-top': '10px', 'border-right':'2px solid black'}),
        dbc.Col(
            [html.Div([
                    html.Div(['Aggregate Maps', html.P()]),
                dbc.Row([dbc.Col(width=4), dbc.Col([dbc.Row([dbc.Col(rig_checkboxes_sat_combo_p1),dbc.Col(rig_checkboxes_sat_combo_p2)]),
                                                   rig_dropdown_map_choice,
                                                    rig_date_range_picker],

                                                   width=4), dbc.Col(width=4)]),
                # dls.Moon(lef_imshow_map),
            ])
                , html.Div([
                # lef_dropdown_map_choice,
                dls.Moon(rig_imshow_map),
            ])]
        ,style={'margin-top': '10px'})
    ]
    ,style={'font-size': '20px', 'textAlign': 'center', 'margin-top': '5px'}
)

dlm_figures_row_hist = dbc.Row(
    [dbc.Col(
        html.Div([
            dls.Moon(lef_hist),
        ])
    ,style={'border-right':'2px solid black'}),
        dbc.Col(
            html.Div([
                dls.Moon(rig_hist),

            ])
        )
    ]
)

fil_title_row = dbc.Row(dbc.Col(
    html.Div(['Filters', html.P(id="fil-title")], style={'font-size': '26px'})
))

tab1_contents = html.Div([
    dlm_title_row,
    dlm_options_row,
    # dlm_figures_row_date_picker,
    dlm_figures_row_opt,
    dlm_figures_row_map,
    dlm_figures_row_ts,
    dlm_figures_row_hist,
])


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_contents, label=" "),

    ]
)

app.layout = dbc.Container(tabs, fluid=True)
