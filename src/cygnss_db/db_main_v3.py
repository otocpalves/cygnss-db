import time

import pandas as pd
import numpy as np
import xarray as xr
import os
import glob
import pickle

import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt

from xhistogram.xarray import histogram

from pprint import pprint
from dash import Dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output
import dash.dependencies

import dash_loading_spinners as dls
import dash_bootstrap_components as dbc


from datetime import datetime, date, timedelta

from db_layout_v3 import app

from pprint import pprint

from io_maps import GNSSRDatacubeReader


gridded_ds_path = 'path/to/datacubes'



grid_choices = [
    # '9_EASE',
    '25_EASE',
    '36_EASE'
]




readers = {
}

for grid_choice in grid_choices:
    dataset_path = os.path.join(gridded_ds_path, f'CYGNSS_SM_Datacube_{grid_choice}.nc')
    readers[f'{grid_choice}'] = GNSSRDatacubeReader(ds_path=dataset_path,
                                                    chunk_format={'time': 1, 'y': 15},
                                                    var_name='mean_SM')

print('Loaded readers')





@app.callback(
    Output('lef-ts', 'figure'),
    [Input('lef-imshow-map', 'clickData'),
     Input('lef-imshow-map', "relayoutData"),
     Input('dlm-ri-grid', 'value'),
     Input('lef-cl-sat-combo-p1', 'value'),
     Input('lef-cl-sat-combo-p2', 'value'),
     Input('lef-date-range-picker', 'start_date'),
     Input('lef-date-range-picker', 'end_date'),
     Input('lef-ts-type-choice', 'value'),
     Input('lef-dd-choice', 'value')
     ]
)
def update_left_timeseries(clickData,
                           rect_data,
                           grid_choice,
                           sat_combo_p1,
                           sat_combo_p2,
                           # ts_choices,
                           start_date,
                           end_date,
                           ts_type,
                           agg_name):

    sat_combo = sat_combo_p1+sat_combo_p2

    return update_timeseries(clickData, rect_data, grid_choice, sat_combo, start_date, end_date, ts_type, agg_name)


@app.callback(
    Output('rig-ts', 'figure'),
    [Input('rig-imshow-map', 'clickData'),
     Input('rig-imshow-map', "relayoutData"),
     Input('dlm-ri-grid', 'value'),
     Input('rig-cl-sat-combo-p1', 'value'),
     Input('rig-cl-sat-combo-p2', 'value'),
     # Input('dlm-cl-ts-choices', 'value'),
     Input('rig-date-range-picker', 'start_date'),
     Input('rig-date-range-picker', 'end_date'),
     Input('rig-ts-type-choice', 'value'),
     Input('rig-dd-choice', 'value'),
     ]
)
def update_right_timeseries(clickData,
                           rect_data,
                           grid_choice,
                           sat_combo_p1,
                            sat_combo_p2,
                           start_date,
                           end_date,
                           ts_type,
                            agg_name
                            ):
    sat_combo = sat_combo_p1 + sat_combo_p2
    return update_timeseries(clickData, rect_data, grid_choice, sat_combo, start_date, end_date, ts_type, agg_name)






def update_timeseries(clickData,
                      rect_data,
                      grid_choice,
                      sat_combo,
                      start_date,
                      end_date,
                      ts_type,
                      agg_name):


    if (end_date is None) or (start_date is None):
        return None

    if 'shapes' not in rect_data:
        return go.Figure()

    sat_combo = [int(s)-1 for s in sat_combo]
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    def get_time_idx(input_date):
        return (input_date - datetime(2018, 8, 1, 0, 0, 0)).days

    dfq = pd.DataFrame()

    dc = readers[grid_choice].datacube

    #Querying hypervolumes
    xr_hypervolumes_sel = []
    for s in rect_data['shapes']:
        y0 = int(np.floor(s['y0']))
        y1 = int(np.ceil(s['y1']))

        x0 = int(np.floor(s['x0']))
        x1 = int(np.ceil(s['x1']))

        smaller_x = min(x0, x1)
        bigger_x = max(x0, x1)
        smaller_y = min(y0, y1)
        bigger_y = max(y0, y1)

        y_slice = slice(smaller_y, bigger_y + 1)
        x_slice = slice(smaller_x, bigger_x + 1)


        hv_sel = dc.isel(y=y_slice,
                         x=x_slice,
                         time=slice(get_time_idx(start_date), get_time_idx(end_date) + 1),
                         sat_id=sat_combo
                         ).mean(dim='sat_id')['mean_SM']

        xr_hypervolumes_sel.append(hv_sel)


    #
    def get_mean_ts(xr_hypervolumes):
        acc = np.zeros(len(xr_hypervolumes[0].time))
        n_ts_total = 0
        for hv in xr_hypervolumes:
            n_ts_hv = len(hv.x) * len(hv.y)
            acc += hv.mean(dim='x').mean(dim='y').to_numpy() * n_ts_hv
            n_ts_total += n_ts_hv

        return acc / n_ts_total

    def get_pcp_matrix(xr_hypervolumes):

        mat = None
        for hv in xr_hypervolumes:

            hv_flattened = np.array(hv.data.transpose(1, 2, 0).reshape(hv.shape[1] * hv.shape[2], hv.shape[0]))
            if mat is None:
                mat = hv_flattened
            else:
                mat = np.concatenate([mat, hv_flattened], axis=0)

        return mat

    def get_density_matrix(xr_hypervolumes):

        histograms = [histogram(hv, dim=['x', 'y'], bins=[np.linspace(0, 0.7, 50)]).to_numpy().T for hv in
                      xr_hypervolumes]
        dm = np.sum(histograms, axis=0)
        return dm

    if (ts_type == 'scatter') or (ts_type == 'line'):
        ts_all = get_mean_ts(xr_hypervolumes_sel)
        dfq['ts'] = ts_all
        dfq['timestamps'] = pd.date_range(start_date, end_date)
        dfx = dfq.copy()

        if ts_type == 'scatter':
            fig = px.scatter(x=dfx['timestamps'].to_numpy(), y=dfx['ts'].to_numpy(),

                                     ).update_layout(xaxis_title='Date', yaxis_title='SM (m³/m³)')
        fig.update_layout(yaxis_range=[0, 0.6])

    elif ts_type == 'density':
        dm = get_density_matrix(xr_hypervolumes_sel)
        dm = dm.astype(float)
        fig = px.imshow(img=np.where(dm==0,np.nan,dm),
                        origin='lower',  
                        color_continuous_scale='viridis_r',


                        x= pd.date_range(start_date, end_date),
                        y=np.linspace(0, 0.7, 50)[:-1],
                        labels={'x':'Date','y':'SM bin (m³/m³)'},
                        aspect='auto',

                        )

    elif ts_type == 'pcp':
        pcp_mat = np.round(get_pcp_matrix(xr_hypervolumes_sel),2)
        fig = px.parallel_coordinates(pd.DataFrame(pcp_mat).fillna(method='ffill').fillna(method='bfill'))
        fig.update_traces(line_colorbar_showticklabels=False, selector=dict(type='parcoords'))


    return fig








@app.callback(
    Output('lef-hist', 'figure'),
    [Input('lef-imshow-map', 'clickData'),
     Input('lef-imshow-map', "relayoutData"),
     Input('dlm-ri-grid', 'value'),
     Input('lef-cl-sat-combo-p1', 'value'),
     Input('lef-cl-sat-combo-p2', 'value'),
     # Input('dlm-cl-ts-choices', 'value'),
     Input('lef-date-range-picker', 'start_date'),
     Input('lef-date-range-picker', 'end_date'),
     Input('lef-ts-type-choice', 'value'),
     Input('lef-dd-choice', 'value')
     ]
)
def update_left_histogram(clickData,
                           rect_data,
                           grid_choice,
                           sat_combo_p1,
                          sat_combo_p2,
                           # ts_choices,
                           start_date,
                           end_date,
                           ts_type,
                           agg_name):
    sat_combo = sat_combo_p1 + sat_combo_p2
    return update_histogram(clickData, rect_data, grid_choice, sat_combo, start_date, end_date, ts_type, agg_name)





@app.callback(
    Output('rig-hist', 'figure'),
    [Input('rig-imshow-map', 'clickData'),
     Input('rig-imshow-map', "relayoutData"),

     Input('dlm-ri-grid', 'value'),
     Input('rig-cl-sat-combo-p1', 'value'),
     Input('rig-cl-sat-combo-p2', 'value'),
     # Input('dlm-cl-ts-choices', 'value'),
     Input('rig-date-range-picker', 'start_date'),
     Input('rig-date-range-picker', 'end_date'),
     Input('rig-ts-type-choice', 'value'),
     Input('rig-dd-choice', 'value'),
     ]
)
def update_right_histogram(clickData,
                           rect_data,
                           grid_choice,
                           sat_combo_p1,
                           sat_combo_p2,
                           # ts_choices,
                           start_date,
                           end_date,
                           ts_type,
                           agg_name
                            ):
    sat_combo = sat_combo_p1 + sat_combo_p2
    return update_histogram(clickData, rect_data, grid_choice, sat_combo, start_date, end_date, ts_type, agg_name)




def update_histogram(clickData,
                      rect_data,
                      grid_choice,
                      sat_combo,
                      start_date,
                      end_date,
                      ts_type,
                      agg_name):


    if (end_date is None) or (start_date is None):
        return None

    if 'shapes' not in rect_data:
        return go.Figure()

    sat_indices = [int(s)-1 for s in sat_combo]
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    def get_time_idx(input_date):
        return (input_date - datetime(2018, 8, 1, 0, 0, 0)).days

    dfq = pd.DataFrame()

    dc = readers[grid_choice].datacube

    #Querying hypervolumes
    xr_hypervolumes_sel = []
    xr_hypervolumes_all = []
    for s in rect_data['shapes']:
        y0 = int(np.floor(s['y0']))
        y1 = int(np.ceil(s['y1']))

        x0 = int(np.floor(s['x0']))
        x1 = int(np.ceil(s['x1']))

        smaller_x = min(x0, x1)
        bigger_x = max(x0, x1)
        smaller_y = min(y0, y1)
        bigger_y = max(y0, y1)

        y_slice = slice(smaller_y, bigger_y + 1)
        x_slice = slice(smaller_x, bigger_x + 1)


        hv_sel = dc.isel(y=y_slice,
                         x=x_slice,
                         time=slice(get_time_idx(start_date), get_time_idx(end_date) + 1),
                         sat_id=sat_indices
                         ).mean(dim='sat_id')['mean_SM']

        xr_hypervolumes_sel.append(hv_sel)

    flattened_hypervolumes = np.concatenate([hv.to_numpy().flatten() for hv in xr_hypervolumes_sel])




    df = pd.DataFrame()
    df['SM Retrievals'] = flattened_hypervolumes
    histo_fig = px.histogram(df['SM Retrievals'],
                             title=f"SM Retrivals histogram-{{{'.'.join([s for s in sat_combo])}}}",
                            labels={'x':"SM Retrievals (m³/m³)"}
                             )
    histo_fig.update_layout(margin={'l': 40, 'b': 40, 't': 27, 'r': 0}, hovermode='closest')

    return histo_fig

















@app.callback(

        Output('lef-imshow-map', 'figure')
    ,
    [
        Input('dlm-ri-grid', 'value'),
        Input('lef-cl-sat-combo-p1', 'value'),
        Input('lef-cl-sat-combo-p2', 'value'),
        Input('lef-date-range-picker', 'start_date'),
        Input('lef-date-range-picker', 'end_date'),
        Input('lef-dd-choice', 'value'),

    ]
)
def update_left_map(
        grid_name,
        sat_combo_p1,
        sat_combo_p2,
        # day,
        start_date_str,
        end_date_str,
        agg_name,

):
    sat_combo = sat_combo_p1 + sat_combo_p2
    return update_map(grid_name, sat_combo, start_date_str,end_date_str,agg_name)


@app.callback(

        Output('rig-imshow-map', 'figure')

    ,
    [
        Input('dlm-ri-grid', 'value'),
        Input('rig-cl-sat-combo-p1', 'value'),
        Input('rig-cl-sat-combo-p2', 'value'),

        Input('rig-date-range-picker', 'start_date'),
        Input('rig-date-range-picker', 'end_date'),
        Input('rig-dd-choice', 'value'),

    ]
)
def update_right_map(
        grid_name,
        sat_combo_p1,
        sat_combo_p2,
        start_date_str,
        end_date_str,
        agg_name,

):
    sat_combo = sat_combo_p1 + sat_combo_p2
    return update_map(grid_name, sat_combo, start_date_str, end_date_str, agg_name)


def update_map(
        grid_name,
        sat_combo,
        # day,
        start_date_str,
        end_date_str,
        agg_name,
):
    print('eeee')

    sat_indices = [int(s)-1 for s in sat_combo]
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    def get_time_idx(input_date):
        return (input_date - datetime(2018, 8, 1, 0, 0, 0)).days

    dc = readers[grid_choice].datacube

    t0 = time.perf_counter()



    agg_time_slice = slice(get_time_idx(start_date), get_time_idx(end_date) + 1)


    if agg_name == 'mean':
        agg_title = f'Mean SM between {start_date_str} and {end_date_str}'
        agg_sel = dc.isel(sat_id=sat_indices, time=agg_time_slice).mean(dim='sat_id').mean(dim='time')['mean_SM']
    elif agg_name == 'n_measurements':
        agg_title = f'N of Measurements between {start_date_str} and {end_date_str}'
        agg_sel = dc.isel(sat_id=sat_indices, time=agg_time_slice).mean(dim='sat_id').count(dim='time')['mean_SM']
    elif agg_name == 'range':
        agg_title = f'SM Range between {start_date_str} and {end_date_str}'
        agg_sel_max = dc.isel(sat_id=sat_indices, time=agg_time_slice).max(dim='sat_id').max(dim='time')['mean_SM']
        agg_sel_min = dc.isel(sat_id=sat_indices, time=agg_time_slice).min(dim='sat_id').min(dim='time')['mean_SM']
        agg_sel = agg_sel_max - agg_sel_min
    elif agg_name == 'std':
        agg_title = f'SM Std Deviation between {start_date_str} and {end_date_str}'
        agg_sel = dc.isel(sat_id=sat_indices, time=agg_time_slice).mean(dim='sat_id').std(dim='time')['mean_SM']
    elif agg_name == 'max':
        agg_title = f'Max SM between {start_date_str} and {end_date_str}'
        agg_sel = dc.isel(sat_id=sat_indices, time=agg_time_slice).mean(dim='sat_id').max(dim='time')['mean_SM']
    elif agg_name == 'min':
        agg_title = f'Min SM between {start_date_str} and {end_date_str}'
        agg_sel = dc.isel(sat_id=sat_indices, time=agg_time_slice).mean(dim='sat_id').min(dim='time')['mean_SM']

    colormaps = {
        'mean': 'cividis_r',
        'n_measurements': 'plasma',
        'range':'plasma',
        'std':'plasma',
        'max':'plasma',
        'min':'plasma'
    }

    z_sel = agg_sel.to_numpy().astype(np.float32)
    zmax = np.nanpercentile(z_sel, 99)
    zmin = np.nanpercentile(z_sel, 0.05)
    t0 = time.perf_counter()
    map_fig = px.imshow(img=z_sel,
                        origin=(0, 0),
                        color_continuous_scale=colormaps[agg_name],
                        zmin=zmin,
                        zmax=zmax,

                        aspect='auto',
                        title=f"CYGNSS Trackwise SM, {agg_title}, using CYGNSS-{{{'.'.join([s for s in sat_combo])}}}"
                        )
    map_fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r':20}, hovermode='closest', dragmode='drawrect')




    t1 = time.perf_counter()

    print(f'Plot time:{t1 - t0}')

    return map_fig











def nsats_to_sat_combo(n):
    return list(range(1, n + 1))


print('foi')
app.run_server(port=8090,
               dev_tools_ui=True,
               # debug=True,
               dev_tools_hot_reload=True,
               threaded=True
               )
