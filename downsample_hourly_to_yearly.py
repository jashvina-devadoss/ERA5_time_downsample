#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 4:42:01 2020

@author: jashvina

This file downloads ERA5 hourly data and outputs monthly and yearly data
"""
import os
from download_ERA5_hourly import download_ERA5_hourly
from netcdf_time_downsample import aggregate_files, time_downsample

def downsample_daily_yearly():
    '''
    (1) Download ERA5 hourly data, month by month, with daily files.
    (2) Downsample hourly files to daily timesteps, with 1 output file for month.
    (3) Downsample to monthly timesteps, with one output file per month.
    
    (4) Aggregate file to one file per year with monthly timesteps.
    (5) Downsample to yearly timesteps, with one output file for the time period.
    '''
    
    # with one file for each day on the specified dates.
    varnames = ['total_precipitation',
               '10m_u_component_of_wind',
               '10m_v_component_of_wind',
               ]
    
    startyear = 1982
    endyear = 2019
    startmonth = 1
    endmonth = 12
    startday = 1
    endday = 31
    
    years = []
    for i in range(startyear, endyear+1):
        years.append([str(i)])
    
    months = []
    for j in range(startmonth,endmonth+1):
        if j < 10:
            j = '0'+str(j)
        months.append([str(j)])
    
    days = []
    for k in range(startday, endday+1):
        if k < 10:
            k = '0'+str(k)
        days.append(str(k))
    
    for year in years:
        for month in months:
    
            ERA5_download_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                                'Data/ERA5/daily_to_yearly/00_hourly_download/'
        
            download_ERA5_hourly(varnames, year, month, days, output_dir = ERA5_download_dir)
        
        
            '''
            (2) Downsample hourly files to daily timesteps, with 1 output file for month.
            '''
            
            # Get a list of downloaded files
            files = []
            
            for filename in os.listdir(ERA5_download_dir):
                # Recall that years is a list of lists. year[0] is a str
                if filename.startswith(year[0]) and filename.endswith('.nc'):
                    files.append(filename)
                else:
                    continue
            
            var_lst = [['u10', 'v10'], 'tp']
            op_lst = ['max', 'sum']
            var_names = ['windspeed', 'totalprecip']
            # aggregate data to daily time steps
            timeres = '1D'
            ws = True
            daily_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                                'Data/ERA5/daily_to_yearly/01_month_daily/'
        
            # Run groups of files by date (in this case, we want one file per month)
            downloaded_files = []
                    
            for filename in files:
                    downloaded_files.append(filename)
                    # MUST SORT FILES to keep dates in order
                    downloaded_files.sort()   
                    
                    
            time_downsample(input_dir = ERA5_download_dir, input_files = downloaded_files,
                            var = var_lst, op = op_lst, time_res = timeres, 
                            output_dir = daily_dir, varnames = var_names,
                            wind_speed = ws)
        
            # Delete downloads (to save storage space)
            for file in downloaded_files:
                path = ERA5_download_dir + file
                os.remove(path)
        
            
            '''
            (3) Downsample to monthly timesteps, with one output file per month.
            '''
            
            monthly_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                                'Data/ERA5/daily_to_yearly/02_monthly/'
                         
            var_lst = ['ws10', 'tp']
            op_lst = ['max', 'sum']
            var_names = ['maxwindspeed', 'totalprecip']
            # aggregate data to monthly time steps
            timeres = '1M'
            
            daily_files = []
                    
            for filename in os.listdir(daily_dir):
                if filename.endswith('.nc'):
                    daily_files.append(filename)
                    daily_files.sort()   
                    
            # Downsample by year
            time_downsample(input_dir = daily_dir, input_files = daily_files, 
                            var = var_lst, op = op_lst, time_res = timeres, 
                            output_dir = monthly_dir, varnames = var_names)
        
            # Delete daily time step files to save storage space
            for file in daily_files:
                path = daily_dir + file
                os.remove(path)
        
        
        '''
        (4) Aggregate files to 1 file per year with monthly timesteps.
        '''
        year_monthly_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                            'Data/ERA5/daily_to_yearly/03_year_monthly/'
            
        monthly_files = []
        for filename in os.listdir(monthly_dir):
            # Remember that `year` is a list, since `years` is a list of lists
            if filename.startswith(year[0]) and filename.endswith('.nc'):
                monthly_files.append(filename)
                
        monthly_files.sort()
        fname = year[0] + '_ERA5' + monthly_files[0].split('ERA5')[-1]
        
        aggregate_files(monthly_dir, monthly_files, year_monthly_dir + fname)

        # Delete monthly time step files to save storage space
        for file in monthly_files:
            path = monthly_dir + file
            os.remove(path)

            
    '''
    (5) Downsample to yearly timesteps.
    '''
    yearly_dir = '/Users/jashvina/jashvina/Projects/2019_2020_wind_extremes/' \
                            'Data/ERA5/daily_to_yearly/04_yearly/'
    
    var_lst = ['ws10', 'tp']
    op_lst = ['max', 'sum']
    var_names = ['maxwindspeed', 'totalprecip']
    # aggregate data to yearly time steps
    timeres = '1Y'
    
    year_monthly_files = []
            
    for filename in os.listdir(year_monthly_dir):
        if filename.endswith('.nc'):
            year_monthly_files.append(filename)
            year_monthly_files.sort()   
            
    # Downsample by year
    time_downsample(input_dir = year_monthly_dir, input_files = year_monthly_files, 
                    var = var_lst, op = op_lst, time_res = timeres, 
                    output_dir = yearly_dir, varnames = var_names)
    
downsample_daily_yearly()