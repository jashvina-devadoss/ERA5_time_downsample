#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:22:54 2020

@author: jashvina

This file tests the output data for bugs. Run whenever script is changed!
"""
import os
from download_ERA5_hourly import download_ERA5_hourly
from netcdf_time_downsample import windspeed, aggregate_files, time_downsample

def test_downsample_daily_yearly():
    '''
    Download ERA5 hourly data for the listed variables. 
    We expect 8 output files (2 years * 2 months * 2 days).
    '''
    
    # with one file for each day on the specified dates.
    varnames = ['total_precipitation',
               '10m_u_component_of_wind',
               '10m_v_component_of_wind',
               ]
    
    startyear = 2000
    endyear = 2001
    startmonth = 3
    endmonth = 4
    startday = 1
    endday = 2
    
    years = []
    for i in range(startyear, endyear+1):
        years.append(str(i))
    
    months = []
    for j in range(startmonth,endmonth+1):
        if j < 10:
            j = '0'+str(j)
        months.append(str(j))
    
    days = []
    for k in range(startday, endday+1):
        if k < 10:
            k = '0'+str(k)
        days.append(str(k))
    
    ERA5_download_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                        'Data/ERA5/Test/Outputs/00_downloads/'

    '''
    download_ERA5_hourly(varnames, years, months, days, output_dir = ERA5_download_dir)
    '''

    '''
    Downsample hourly files to daily timesteps, with 1 output file for month.
    '''
    
    # Get a list of downloaded files
    files = []
    for year in years:
        for filename in os.listdir(ERA5_download_dir):
            if filename.startswith(year) and filename.endswith('.nc'):
                files.append(filename)
            else:
                continue
    
    assert len(files) == 8
    print(files)
    
    var_lst = [['u10', 'v10'], 'tp']
    op_lst = ['max', 'sum']
    var_names = ['windspeed', 'totalprecip']
    # aggregate data to daily time steps
    timeres = '1D'
    windspeed = True
    daily_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                        'Data/ERA5/Test/Outputs/01_downsample/'

    # Run groups of files by date (in this case, we want one file per month)
    for year in years:
        for month in months:
            
            file_group = []
            
            for filename in files:
                if filename.startswith(year + '-' + month):
                    file_group.append(filename)
            file_group.sort()   
            
            time_downsample(input_dir = ERA5_download_dir, input_files = file_group,
                            var = var_lst, op = op_lst, time_res = timeres, 
                            output_dir = daily_dir, varnames = var_names,
                            wind_speed = windspeed)
    
    '''
    Aggregate the files to one file per year (with daily time steps)
    '''
    
    agg_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                        'Data/ERA5/Test/Outputs/02_aggregate/'
    
    # Get a list of downsampled files, and aggregate by year
    for year in years:
        file_group = []
        for filename in os.listdir(daily_dir):
            if filename.startswith(year) and filename.endswith('.nc'):
                file_group.append(filename)
        file_group.sort()
        fname = year + '_ERA5' + file_group[0].split('ERA5')[-1]
        aggregate_files(daily_dir, file_group, agg_dir + fname)
        
    '''
    Downsample by year, with one output file spanning years.
    '''
    
    yearly_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                 'Data/ERA5/Test/Outputs/03_downsample/'
                 
    var_lst = ['ws10', 'tp']
    op_lst = ['max', 'sum']
    var_names = ['windspeed', 'totalprecip']
    # aggregate data to yearly time steps
    timeres = '1Y'
    
    file_group = []
            
    for filename in os.listdir(agg_dir):
        if filename.endswith('.nc'):
            file_group.append(filename)
            file_group.sort()   
            
    # Downsample by year
    time_downsample(input_dir = agg_dir, input_files = file_group, 
                    var = var_lst, op = op_lst, time_res = timeres, 
                    output_dir = yearly_dir, varnames = var_names)
    
    

test_downsample_daily_yearly()