import os
import glob
import pickle
import time
from datetime import datetime, date

import xarray as xr
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt







class GNSSRDatacubeReader:

    def __init__(self, ds_path, chunk_format={'time':1, 'y':15}, var_name = 'mean_SM'):
               
        self.datacube = xr.open_dataset(ds_path,
                                        chunks=chunk_format
                                        )

        self.nc_attrs = self.datacube.attrs
        self.data_shape = self.datacube[var_name].shape
        self.shape_dict = {'time':self.data_shape[0],'sat_id':self.data_shape[1], 'y': self.data_shape[2], 'x':self.data_shape[3]}

    
    def read_volume(self, window, from_time_idx = None, to_time_idx = None, sat_combo=None, data_var='mean_SM'):
        # Window is inclusive of last pixel
        # Window in format [top_left_row, top_left_col, bottom_right_row, bottom_right_col]


        if sat_combo is None:
            sat_combo = [1,2,3,4,5,6,7,8]
        
        start_time_index = 0
        end_time_index = self.data_shape[0]
        if from_time_idx is not None:
            start_time_index = from_time_idx
        if to_time_idx is not None:
            end_time_index = to_time_idx + 1 # should be inclusive
        
        start_row_index = window[0]
        end_row_index   = window[2]+1
        start_col_index = window[1]
        end_col_index   = window[3]+1

        data_xr = self.datacube.data_vars[data_var].isel(
                                                y=slice(start_row_index, end_row_index),
                                                x=slice(start_col_index, end_col_index),
                                                sat_id=sat_combo,
                                                time=slice(start_time_index, end_time_index))

        return data_xr
    
    def read_volume_merged(self, window, from_time_idx = None, to_time_idx = None, data_var='mean_SM'):

        volume =  self.read_volume(window, from_time_idx = from_time_idx, to_time_idx = to_time_idx, data_var=data_var)

        volume_merged = volume.mean(dim='sat_id')

        return volume_merged
    




