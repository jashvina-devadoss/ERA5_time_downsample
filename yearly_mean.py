#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:52:56 2020

@author: jashvina

This script calculates yearly means.
Inputs:
    (1) Directory with netcdf files (each with one yearly value per variable)
        An example input is the output from downsample_monthly_to_yearly.py
Output:
    (1) One file with the mean of all yearly values.
"""

import os
import xarray as xr
from netcdf_time_downsample import aggregate_files
    
def mean_annual():
    # Inputs:
        
    #Directory with yearly netCDF files
    yearly_dir = '/Users/jashvina/jashvina/GoogleDrive/My Drive/2019_2020_wind_extremes/Data/ERA5/monthly_to_yearly/yearly/'

    start_year = 1982
    end_year = 2019
    
    aggregate_filepath = '/Users/jashvina/jashvina/GoogleDrive/My Drive/2019_2020_wind_extremes/Data/ERA5/monthly_to_yearly/{}_{}_yearly_aggregate.nc'.format(start_year, end_year)    
    
    # Variable name(s) in input file:
    var = ['tp']
    
    # Variable names for output file name
    var_name = 'precip'    

    output_dir = '/Users/jashvina/jashvina/GoogleDrive/My Drive/2019_2020_wind_extremes/Data/ERA5/'  
                  
    ############################                  
    
    years = []
    for i in range(start_year, end_year+1):
        years.append(str(i))
    
    filepaths= []
    
    for file in os.listdir(yearly_dir):
        for year in years:
            if file.startswith(year):
                filepaths.append('{}{}'.format(yearly_dir,file))
    
    
    aggregate_files(filepaths, aggregate_filepath)
    
    #Compute longterm mean
    agg = xr.open_dataset(aggregate_filepath)
    longterm_mean = agg.mean(dim = 'time')
    for v in var:
        longterm_mean[v].attrs = agg[v].attrs
    
    longterm_mean.to_netcdf(path = '{}{}_{}_ERA5_mean_annual_{}.nc'.format(output_dir, years[0], years[-1], var_name), 
                            mode = 'w', format = 'NETCDF4', engine = 'netcdf4')
 

mean_annual()