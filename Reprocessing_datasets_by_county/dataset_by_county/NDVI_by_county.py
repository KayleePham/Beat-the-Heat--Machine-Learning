# NOTES: this file runs smoothly on my machine (no errors and no output)
#   if it doesn't run on yours, it might be because of the dir setup (see below)

# Directory setup notes: in the same dir as this .py file, there should be
# the PreprocessingAuxiliaryFunctions.py, and 2 data folders: 
# input_data_files (all the NDVI images) and burn_area_files. Within the burn_are_files
# there should be 2 essential folders, burn_date and QA. If all is correct, you shouldn't
# need to reconfigure anything because of the function that uses relative paths 
# (af.create_abs_path_from_relative('rel_path')). If you have questions or want to verify the setup
# Please send me a message on discord

import fiona
import rasterio
import rasterio.mask
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import os
import sys
import glob
from osgeo import gdal
import numpy as np
import scipy.ndimage
import datetime as dt

from PreprocessingAuxiliaryFunctions import PreprocessingAuxiliaryFunctions as auxFuncts

def main():
    af = auxFuncts()

    CA_counties_geodf = af.read_geojson_geodf()
    shapes = af.extract_shapes_from_county_geometry(CA_counties_geodf)
    print(CA_counties_geodf)
    print(shapes)
    # shapes = af.read_geojson()  # read in list of county boundaries

    # NDVI_inDir = (r'C:\Users\Student\Documents\School\Senior design\dataset_by_county\input_data_files')  #Path to NDVI files
    #* note: dir setup for files should be as follows:
    #* \GitHub\Beat-the-Heat--Machine-Learning\Reprocessing_datasets_by_county\dataset_by_county\NDVI_by_county.py
    #* within the 'dataset_by_county' folder, also include the NDVI dataset in a folder named 'input_data_files'
    NDVI_inDir = af.create_abs_path_from_relative('input_data_files')  # need parameter? maybe refractor function to take out that feature
    os.chdir(NDVI_inDir)                 # Change to working directory


    EVIFiles        = glob.glob('MOD13A1.006__500m_16_days_NDVI_**.tif')             # Search for and create a list of EVI files
    EVIqualityFiles = glob.glob('MOD13A1.006__500m_16_days_VI_Quality**.tif')  # Search the directory for the associated quality .tifs
    EVIlut          = glob.glob('MOD13A1-006-500m-16-days-VI-Quality-lookup.csv')      # Search for look up table 
    EVI_v6_QA_lut   = pd.read_csv(EVIlut[0])   

    EVIgoodQuality = af.extracting_good_quality_vals_from_lut(EVI_v6_QA_lut)
    # print(EVIqualityFiles)  # debugging output

    EVI = gdal.Open(EVIFiles[0])                    # Read file in, starting with MOD13Q1 version 6
    EVIBand = EVI.GetRasterBand(1)                  # Read the band (layer)
    EVIData = EVIBand.ReadAsArray().astype('float') # Import band as an array with type float
        
    EVIquality = gdal.Open(EVIqualityFiles[0])                       # Open the first quality file
    EVIqualityData = EVIquality.GetRasterBand(1).ReadAsArray()       # Read in as an array
    EVIquality = None 
            
    # File name metadata:
    EVIproductId = EVIFiles[0].split('_')[0]                                      # First: product name
    EVIlayerId = EVIFiles[0].split(EVIproductId + '_')[1].split('_doy')[0]        # Second: layer name
    EVIyeardoy = EVIFiles[0].split(EVIlayerId+'_doy')[1].split('_aid')[0]         # Third: date
    EVIaid = EVIFiles[0].split(EVIyeardoy+'_')[1].split('.tif')[0]                # Fourth: unique ROI identifier (aid)
    EVIdate = dt.datetime.strptime(EVIyeardoy, '%Y%j').strftime('%m/%d/%Y')       # Convert YYYYDDD to MM/DD/YYYY
    EVI_year = dt.datetime.strptime(EVIyeardoy, '%Y%j').year
    EVI_month = dt.datetime.strptime(EVIyeardoy, '%Y%j').month 

    EVI_meta = EVI.GetMetadata()                      # Store metadata in dictionary
    EVIFill = EVIBand.GetNoDataValue()                # Returns fill value
    EVIStats = EVIBand.GetStatistics(True, True)      # returns min, max, mean, and standard deviation
    EVI = None 

    EVIscaleFactor = float(0.0001)  # Search the metadata dictionary for the scale factor 
    EVIData[EVIData == EVIFill] = np.nan              # Set the fill value equal to NaN for the array
    EVIScaled = EVIData * EVIscaleFactor 

    EVI_masked = np.ma.MaskedArray(EVIScaled, np.in1d(EVIqualityData, EVIgoodQuality, invert = True))# Apply QA mask to the EVI data
    print(EVI_masked.compressed())


    # EVI_masked

    # plt.figure(figsize=(9, 9))
    # plt.imshow(EVIScaled)



if __name__ == "__main__":
    # execute only if run as a script
    main()