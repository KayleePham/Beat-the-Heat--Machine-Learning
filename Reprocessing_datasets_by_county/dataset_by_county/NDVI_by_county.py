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


def main():
    shapes = read_geojson()  # read in list of county boundaries

    # NDVI_inDir = (r'C:\Users\Student\Documents\School\Senior design\dataset_by_county\input_data_files')  #Path to NDVI files
    #* note: dir setup for files should be as follows:
    #* \GitHub\Beat-the-Heat--Machine-Learning\Reprocessing_datasets_by_county\dataset_by_county\NDVI_by_county.py
    #* within the 'dataset_by_county' folder, also include the NDVI dataset in a folder named 'input_data_files'
    NDVI_inDir = create_abs_path_to_dataset('input_data_files')  # need parameter? maybe refractor function to take out that feature
    os.chdir(NDVI_inDir)                 # Change to working directory


    EVIFiles        = glob.glob('MOD13A1.006__500m_16_days_NDVI_**.tif')             # Search for and create a list of EVI files
    EVIqualityFiles = glob.glob('MOD13A1.006__500m_16_days_VI_Quality**.tif')  # Search the directory for the associated quality .tifs
    EVIlut          = glob.glob('MOD13A1-006-500m-16-days-VI-Quality-lookup.csv')      # Search for look up table 
    EVI_v6_QA_lut   = pd.read_csv(EVIlut[0])   

    EVIgoodQuality = extracting_good_quality_vals_from_lut(EVI_v6_QA_lut)
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

    # EVI_masked = good_quality_pixels()

    # EVI_masked

    # plt.figure(figsize=(9, 9))
    # plt.imshow(EVIScaled)

def read_geojson():
    """ Loading county boundaries via geojson - returns arr of county geometry shapes """
    # source: https://gis.data.ca.gov/datasets/8713ced9b78a4abb97dc130a691a8695_0?geometry=-146.754%2C31.049%2C-91.251%2C43.258&page=7
    CA_cnty_geojson_link = 'https://opendata.arcgis.com/datasets/8713ced9b78a4abb97dc130a691a8695_0.geojson'
    CA_county_boundaries_gdf = gpd.read_file(CA_cnty_geojson_link)

    # * storing all boundaries in list var shapes
    shapes = [x for x in CA_county_boundaries_gdf['geometry']]
    county_shapes = []
    for i in range(58):
        county_shapes.append(shapes[i])
    return county_shapes

def create_abs_path_to_dataset(relative_dir_path):
    """ Creates relative path from current directory to input file: 'input_data_files' in project dir """
    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    return os.path.join(fileDirectory, relative_dir_path)  #Navigate to relative_dir_path directory

def extracting_good_quality_vals_from_lut(lut):
    """ Returns good quality values via look up table (LUT) """
    # Include good quality based on MODLAND
    lut = lut[lut['MODLAND'].isin(['VI produced with good quality', 'VI produced, but check other QA'])]

    # Exclude lower quality VI usefulness
    VIU =["Lowest quality","Quality so low that it is not useful","L1B data faulty","Not useful for any other reason/not processed"]
    lut = lut[~lut['VI Usefulness'].isin(VIU)]

    lut = lut[lut['Aerosol Quantity'].isin(['Low','Average'])]   # Include low or average aerosol
    lut = lut[lut['Adjacent cloud detected'] == 'No' ]           # Include where adjacent cloud not detected
    lut = lut[lut['Mixed Clouds'] == 'No' ]                      # Include where mixed clouds not detected
    lut = lut[lut['Possible shadow'] == 'No' ]                   # Include where possible shadow not detected

    EVIgoodQuality = list(lut['Value']) # Retrieve list of possible QA values from the quality dataframe
    return EVIgoodQuality

if __name__ == "__main__":
    # execute only if run as a script
    main()