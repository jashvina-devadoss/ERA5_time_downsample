#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 20:56:07 2020

@author: jashvina

This file downsamples the time step of ERA5 netCDF files, aggregating variables
into yearly output files.

Inputs: one file per day with hourly time steps over multiple years 
        ERA5 total hourly precipitation and hourly wind speed
Outputs: Downsampled daily data with one file per year
         ERA5 total daily precipitation and maximum daily wind speed

"""
from download_ERA5_hourly import download_ERA5_hourly
from netcdf_time_downsample import windspeed, time_downsample

def main():
    
    # Download ERA5 hourly data for all months and days in the year range.
    varnames = ['total_precipitation', 
               '10m_u_component_of_wind',
               '10m_v_component_of_wind', 
               ]
    
    syear = 1982
    eyear = 2020
    
    years = []
    for i in range(syear, eyear+1):
        years.append(str(i))
        
    months = []
    for j in range(1,13):
        if j < 10:
            j = '0'+str(j)
        months.append(str(j))
        
    days = []
    for k in range(1,32):
        if k < 10:
            k = '0'+str(k)
        days.append(str(k))
    
    ERA5_download_dir = '/Users/jashvina/jashvina/GoogleDrive/My Drive/2019_'\
                        '2020_wind_extremes/Data/ERA5/unaggregated/'
                        
                        
    download_ERA5_hourly(varnames, years, months, days, output_dir = ERA5_download_dir)
    
    var_lst = [['u10', 'v10'], 'tp']
    op_lst = ['max', 'sum']
    vn = ['windspeed', 'totalprecip']
    # aggregate data to daily time steps
    tr = '1D'
    ws = True
    out_dir = '/Users/jashvina/jashvina/GoogleDrive/My Drive/2019_2020_wind_'\
              'extremes/Data/ERA5/daily_totalprecip_maxwindspeed/'
    time_downsample(input_dir = ERA5_download_dir, startyear = syear, 
                    endyear = eyear, var = var_lst, op = op_lst, time_res = tr, 
                    output_dir = out_dir, varnames = vn, wind_speed = ws)
    
if __name__ == '__main__':
    main()