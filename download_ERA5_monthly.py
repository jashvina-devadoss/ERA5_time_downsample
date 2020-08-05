#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:40:42 2020

@author: jashvina

This file contains a function to iteratively download monthly ERA5 data.  
Iterating prevents the ESA server from timing out; the small individual 
file size allows for a large overall data transfer.

To use this script, ERA5 CDS API must be installed on the local machine.  
Find instructions under 4 - Download ERA5 family data through the CDS API
https://confluence.ecmwf.int/display/CKB/How+to+download+ERA5#HowtodownloadERA5-First:InstallCDSAPIonyourmachine

"""

import cdsapi
import os

def download_ERA5_monthly(varnames, years, output_dir, filename_suffix = None):
    '''
    This script downloads ERA5 monthly data, with one file for each year.

    Parameters
    ----------
    varnames : list of strings
        List of ERA5 variables. Names can be found under "Show API request":
            https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=form
    years : list of strings
        List with each year of interest from 1981-present in 'YYYY' format.
    output_dir : str
        filepath for output files
    filename_suffix: str (optional)
        optional string to add to the end of filename (e.g. describing variables)

    Returns
    -------
    ERA5 downloads, with one file for each year, saved to the output directory.

    '''
    os.chdir(output_dir)
    c = cdsapi.Client()
    
    for year in years:

        c.retrieve(
            'reanalysis-era5-single-levels-monthly-means',
            {
                'format': 'netcdf',
                'product_type': 'monthly_averaged_reanalysis',
                'variable': 'total_precipitation',
                'year': [
                    year
                ],
                'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                ],
                'time': '00:00',
            },
           '{}_ERA5_monthly_{}.nc'.format(year, filename_suffix))