#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 2020

@author: jashvina

This file contains a function to iteratively download hourly ERA5 data.  
Iterating prevents the ESA server from timing out; the small individual 
file size allows for a large overall data transfer.

To use this script, ERA5 CDS API must be installed on the local machine.  
Find instructions under 4 - Download ERA5 family data through the CDS API
https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5#HowtodownloadERA5-First:InstallCDSAPIonyourmachine

"""

import cdsapi
import os

def download_ERA5_hourly(varnames, years, months, days, output_dir, filename_suffix = None):
    '''
    This script downloads ERA5 hourly data, with one file with 24 hours of data
    for each day.

    Parameters
    ----------
    varnames : list of strings
        List of ERA5 variables. Names can be found under "Show API request":
            https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=form
    years : list of strings
        List with each year of interest from 1981-present in 'YYYY' format.
    months : list of strings
        List with each month of interest in 'MM' format..
    days : list of strings
        List with each day of interest in 'DD' format..
    output_dir : str
        filepath for output files
    filename_suffix: str (optional)
        optional string to add to the end of filename (e.g. describing variables)

    Returns
    -------
    ERA5 hourly data, with one file for each day, saved to the output directory.

    '''
    os.chdir(output_dir)
    c = cdsapi.Client()
    
    # File naming
    if filename_suffix == None:
        fn_suffix = ''
    else:
        fn_suffix = '_' + filename_suffix
    
    for year in years:
        for month in months:
            for day in days:
                c.retrieve(
                    'reanalysis-era5-land',
                    {
                        'format': 'netcdf',
                        'time': [
                            '00:00', '01:00', '02:00',
                            '03:00', '04:00', '05:00',
                            '06:00', '07:00', '08:00',
                            '09:00', '10:00', '11:00',
                            '12:00', '13:00', '14:00',
                            '15:00', '16:00', '17:00',
                            '18:00', '19:00', '20:00',
                            '21:00', '22:00', '23:00',
                        ],
                        'day': day,
                        
                        'month': month,
                        
                        'year': year,
                        
                    'variable': varnames
                    },
                    '{}-{}-{}_ERA5_hourly{}.nc'.format(year, month, day, fn_suffix))