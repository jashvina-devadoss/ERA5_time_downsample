#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 2020

@author: jashvina

This file contains a function for sub-file time down-sampling of netCDF files,
outputting yearly files with the new time step. It includes an option for 
calculating wind speed.  

"""
import xarray as xr
import numpy as np
import os
import netCDF4

def windspeed(u, v):
    ''' Calculate wind speed from u and v directions. '''
    return np.sqrt(u**2 + v**2)
    

def time_downsample(input_dir, startyear, endyear, var, op, time_res, 
                    output_dir, varnames = None, wind_speed = False):
    '''
    This function downsamples the time step within netCDF files and concatenates 
    the new downsampled data, outputting one netCDF file per year.
    
    An example input could be 1,000 netCDF files with hourly data, with one 
    file per day for 3+ years. This function could be used to get daily 
    per-pixel sums, with one file per year.
    
    input_dir:  File path to directory with input netCDF files.
    
    startyear:  int, first year of input data
    
    endyear:    int, last year of input data
    
    var:        list of strings, variable names in input netCDF files
    
    op:         list of strings ('sum', 'max', or 'mean'), reduction operations 
                for each variable in ordered pairs (1st operation is performed 
                on 1st variable, etc.)
                
    time_res:   str, Set desired new time resolution with Pandas datetime syntax 
                (e.g. "1D" for daily resolution, "2H" for two-hour resolution) 
                https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html
                The new resolution must be less than the total time span in 
                each input file (e.g. if input files have a month of data, 
                the coarsest possible new time resolution is a month). To 
                create a longer timespan in each individual file, merge files 
                by applying xr.concat() to the list of input files (xarray 
                DataSets) over the time dimension.
                
    output_dir: Filepath for output netCDF files (one file per year with
                variables reducced to the downsampled time resolution).
    
    varnames:   list of strings (optional), include variables names in output 
                file names.
                
    wind_speed: boolean, whether to calculate wind speed from u and v 
                directions.  If True, set the first element in the list var to 
                be a nested list with two elements for [u,v] wind directions.
    '''
    years = []
    for y in range(startyear, endyear+1):
        years.append(str(y))
    
    for year in years:
        
        # Get all ERA5 daily files for one year (assumes filename starts with year in YYYY format)
        files = []
        for filename in os.listdir(input_dir):
            if filename.startswith(year) and filename.endswith('.nc'):
                files.append(filename)
            else:
                continue
    
        # Create aggregate data for the specified time resolution
        agg_lst = []
        for file in files:
            ds = xr.open_dataset(input_dir + file)
    
            for index, v in enumerate(var):
                
                # When index = 0, create a new aggregate Dataset
                if index == 0:
    
                    if wind_speed == True:
                        # Calculate wind speed and take time aggregates
                        ws = 'ws' + v[0][1:]
    
                        ds[ws] = windspeed(ds[v[0]], ds[v[1]])
                        ds[ws].attrs['units'] = 'm s**-1'
                        ds[ws].attrs['long_name'] = v[0][1:] + ' meter wind speed'
    
                        # Resample by time, using selected aggregation method
                        if op[index] == 'max':
                            ds_agg = ds[ws].resample(time = time_res).max().to_dataset()
                        elif op[index] == 'sum':
                            ds_agg = ds[ws].resample(time = time_res).sum().to_dataset()
                        elif op[index] == 'mean':
                            ds_agg = ds[ws].resample(time = time_res).mean().to_dataset()
    
                    else:
                        # Resample by time, using selected aggregation method
                        if op[index] == 'max':
                            ds_agg = ds[v].resample(time = time_res).max().to_dataset()
                        elif op[index] == 'sum':
                            ds_agg = ds[v].resample(time = time_res).sum().to_dataset()
                        elif op[index] == 'mean':
                            ds_agg = ds[v].resample(time = time_res).mean().to_dataset()
    
                        # Get attributes from original dataset
                        ds_agg[v].attrs = ds[v].attrs
    
                else:
                    # When index > 0, add the new aggregate DataArray to the existing aggregate DataSet
                    # Resample by time, using selected aggregation method
                    if op[index] == 'max':
                        ds_agg[v] = ds[v].resample(time = time_res).max()
                    elif op[index] == 'sum':
                        ds_agg[v] = ds[v].resample(time = time_res).sum()
                    elif op[index] == 'mean':
                        ds_agg[v] = ds[v].resample(time = time_res).mean()
    
                    # Get attributes from original dataset
                    ds_agg[v].attrs = ds[v].attrs
    
            agg_lst.append(ds_agg)
            del ds_agg
        # Combine aggregate data into one file per year
        agg = xr.concat(agg_lst, dim = 'time')
        
        # File naming
        if time_res == '1M':
            time_res_name = 'monthly'
        elif time_res == '1D':
            time_res_name = 'daily'
        elif time_res == '1H':
            time_res_name = 'hourly'
        else:
            time_res_name = time_res
        
        varnames_str = ''
        if varnames:
            for i in varnames:
                varnames_str = varnames_str + '_' + i
        
        output_filepath = '{}{}_ERA5_{}{}.nc'.format(output_dir, year, 
                                                     time_res_name, 
                                                     varnames_str)
        
        # Write out file
        agg.to_netcdf(output_filepath, mode = 'w', format = 'NETCDF4')
