#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue August 4

@author: jashvina

This file downsamples the time step of ERA5 netCDF files, aggregating variables.

Intermediate outputs:
    (1) Monthly total precipitation in monthly files
Final output:
    (4) Yearly total precipitation for all years in one file.
    
"""
from download_ERA5_monthly import download_ERA5_monthly
from netcdf_time_downsample import time_downsample, aggregate_files
import os

def monthly_to_yearly():
    
    # Download ERA5 monthly in the year range.
    varnames = ['total_precipitation']
    
    syear = 1982
    eyear = 2020
    
    years = []
    for i in range(syear, eyear+1):
        years.append(str(i))
        
    
    # ERA5 download directory (1 file per year with monthly data)
    monthly_dir = '/Users/jashvina/jashvina/GoogleDrive/My Drive/2019_'\
                    '2020_wind_extremes/Data/ERA5/monthly_to_yearly/monthly/' 
                        
    download_ERA5_monthly(varnames, years, output_dir = monthly_dir,
                  filename_suffix = 'totalprecip')   
    
    var_lst = ['tp']
    op_lst = ['sum']
    var_name = ['totalprecip']
    # aggregate data to yearly time steps
    time_res = '1Y'

    # Directory for daily files
    # 1 file per year with daily data
    yearly_dir = '/Users/jashvina/jashvina/GoogleDrive/My Drive/2019_2020_wind_'\
          'extremes/Data/ERA5/monthly_to_yearly/yearly/'
          
    time_downsample(input_dir = monthly_dir, startyear = syear, 
                    endyear = eyear, var = var_lst, op = op_lst, time_res = time_res, 
                    output_dir = yearly_dir, varnames = var_name)
    
    
monthly_to_yearly()