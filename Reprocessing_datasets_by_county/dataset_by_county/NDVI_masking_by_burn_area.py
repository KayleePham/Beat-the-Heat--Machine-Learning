# NOTES: this runs without errors for me (Makoto). Haven't done checking except until line 38

# Directory setup notes: in the same dir as this .py file, there should be
# the PreprocessingAuxiliaryFunctions.py, and 2 data folders: 
# input_data_files (all the NDVI images) and burn_area_files. Within the burn_are_files
# there should be 2 essential folders, burn_date and QA. If all is correct, you shouldn't
# need to reconfigure anything because of the function that uses relative paths 
# (af.create_abs_path_from_relative('rel_path')). If you have questions or want to verify the setup
# Please send me a message on discord

# Import libraries
import os
import glob
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
import pandas as pd
import datetime as dt

from PreprocessingAuxiliaryFunctions import PreprocessingAuxiliaryFunctions as auxFuncts  # helper functions

def main():

    af = auxFuncts()  # helper function object

    # Get County Shapes
    CA_counties_geodf = af.read_geojson_geodf()
    shapes = af.extract_shapes_from_county_geometry(CA_counties_geodf)
 
     # Setting up input directories
    out_dir = af.create_abs_path_from_relative('output')
    BAinDir = af.create_abs_path_from_relative('burn_area_files\\burn_date')  # i think this is being used for BA and QA
    NDVI_inDir = af.create_abs_path_from_relative('input_data_files')
    BA_burn_date_dir = af.create_abs_path_from_relative('burn_area_files\\burn_date')
    BA_QA_dir = af.create_abs_path_from_relative('burn_area_files\\QA')

    # BAinDir = 'C:/Users/SASUKE/Desktop/Spring2021/COMP491/NDVI_BA_ALL/'  # Path to the Burn Area Files
    # NDVI_inDir = 'C:/Users/SASUKE/Desktop/Spring2021/COMP491/NDVI_BA_ALL/'  #Path to NDVI files
    # changing working directory
    os.chdir(NDVI_inDir)                                                             # Change to working directory
    out_dir = os.path.normpath(os.path.split(BAinDir)[0] + os.sep + 'output') + '\\'  # Create and set output directory
    if not os.path.exists(out_dir): os.makedirs(out_dir)


    # create references to files
    EVIFiles        = glob.glob('MOD13A1.006__500m_16_days_NDVI_**.tif')          # Search for and create a list of EVI files
    EVIqualityFiles = glob.glob('MOD13A1.006__500m_16_days_VI_Quality**.tif')     # Search the directory for the associated quality .tifs
    EVIlut          = glob.glob('MOD13A1-006-500m-16-days-VI-Quality-lookup.csv') # Search for look up table 

    EVI_v6_QA_lut = pd.read_csv(EVIlut[0])                                    # Read in the lut

    EVIgoodQuality = af.extracting_good_quality_vals_from_lut(EVI_v6_QA_lut)

    os.chdir(BA_burn_date_dir)                                                             # Change to working directory
    BAFiles = glob.glob('MCD64A1.006_Burn_Date_**.tif') # Search for and create a list of BA files
    os.chdir(BA_QA_dir) 
    BAqualityFiles =glob.glob('MCD64A1.006_QA_**.tif')    # Search the directory for the associated quality .tifs
    # lut = glob.glob('-006-QA-lookup.csvMCD64A1')    
    os.chdir(NDVI_inDir)  # LUTs are in NDVI folder
    lut = glob.glob('MCD64A1-006-QA-lookup.csv')                 # Search for look up table 
    v6_BAQA_lut = pd.read_csv(lut[0])     # Read in the lut
    # Include good quality based on MODLAND
    v6_BAQA_lut = v6_BAQA_lut[v6_BAQA_lut['Valid data'].isin([True])]


    # Special circumstances unburned
    SP =["Too few training observations or insufficient spectral separability between burned and unburned classes"]
    v6_BAQA_lut = v6_BAQA_lut[~v6_BAQA_lut['Special circumstances unburned'].isin(SP)]
    v6_BAQA_lut

    BAgoodQuality = list(v6_BAQA_lut['Value']) # Retrieve list of possible QA values from the quality dataframe
    BAVal = tuple(range(1, 367, 1))



    #* set up loop per county
    #* loop per data image

    #* loop idea: 
        #* open one NDVI image 
        #*     mask one county, store data, mask county 2, store data, etc...


    NDVI_result = []
    for i in range(0, len(EVIFiles)):
        EVI = gdal.Open(EVIFiles[i])                    # Read file in, starting with MOD13Q1 version 6 #* in dir input_files
        EVIquality = gdal.Open(EVIqualityFiles[i])                       # Open the first quality file
        
        
        EVIBand = EVI.GetRasterBand(1)                  # Read the band (layer)
        EVIData = EVIBand.ReadAsArray().astype('float') # Import band as an array with type float
        
        EVIqualityData = EVIquality.GetRasterBand(1).ReadAsArray()       # Read in as an array
        EVIquality = None 

        # creates file name
        # File name metadata:
        EVIproductId = EVIFiles[i].split('_')[0]                                      # First: product name
        EVIlayerId = EVIFiles[i].split(EVIproductId + '_')[1].split('_doy')[0]        # Second: layer name
        EVIyeardoy = EVIFiles[i].split(EVIlayerId+'_doy')[1].split('_aid')[0]         # Third: date
        EVIaid = EVIFiles[i].split(EVIyeardoy+'_')[1].split('.tif')[0]                # Fourth: unique ROI identifier (aid)
        EVIdate = dt.datetime.strptime(EVIyeardoy, '%Y%j').strftime('%m/%d/%Y')       # Convert YYYYDDD to MM/DD/YYYY
        EVI_year = dt.datetime.strptime(EVIyeardoy, '%Y%j').year                      #* getting m and y of NDVI tif file to be compared to BA file
        EVI_month = dt.datetime.strptime(EVIyeardoy, '%Y%j').month   
        
        ##INSERT FOR LOOP TO SELECT EACH COUNTY SHAPE
        for x in range(0,len(shapes)):
            # Mask NDVI file by Shape


            # Mask NDVI QA file by Shape

            # Mask BA file by Shape

            # Mask BA QA file by Shape            
                

            

            # BA_burn_date_dir = af.go_to_parent_dir
            # BA_burn_date_dir = af.create_abs_path_from_relative('burn_area_files\\burn_date')
            os.chdir(BA_burn_date_dir)                                                             # Change to working directory

            #* getting name of file
            BAFileName = getBAFile(BAFiles, EVI_month, EVI_year)


            # BA_QA_dir = af.go_to_parent_dir
            # BA_QA_dir = af.create_abs_path_from_relative('QA')
            os.chdir(BA_QA_dir)                                                             # Change to working directory

            # af.go_to_parent_dir
            # af.create_abs_path_from_relative('QA')
            BAQualityFileName = getBAFile(BAqualityFiles, EVI_month, EVI_year)

            if not BAFileName in (None, ''):
                os.chdir(BA_burn_date_dir)                                                             # Change to working directory
                BA = gdal.Open(BAFileName)                                   # Read file in, starting with MCD64A1 version 6
                BABand = BA.GetRasterBand(1)                                 # Read the band (layer)
                BAData = BABand.ReadAsArray().astype('float')                # Import band as an array with type float  
                
                os.chdir(BA_QA_dir)  
                BAquality = gdal.Open(BAQualityFileName)                     # Open the first quality file
                BAqualityData = BAquality.GetRasterBand(1).ReadAsArray()     # Read in as an array
                BAquality = None 

                # File Metadata
                BA_meta = BA.GetMetadata()                        # Store metadata in dictionary
                EVI_meta = EVI.GetMetadata()                      # Store metadata in dictionary

                # Band metadata
                BAFill = BABand.GetNoDataValue()                  # Returns fill value
                BAStats = BABand.GetStatistics(True, True)        # returns min, max, mean, and standard deviation
                BA = None                                         # Close the GeoTIFF file

                # Band metadata
                EVIFill = EVIBand.GetNoDataValue()                # Returns fill value
                EVIStats = EVIBand.GetStatistics(True, True)      # returns min, max, mean, and standard deviation
                EVI = None                                        # Close the GeoTIFF file

                BAscaleFactor = float(BA_meta['scale_factor'])    # Search the metadata dictionary for the scale factor 
                BAData[BAData == BAFill] = np.nan                 # Set the fill value equal to NaN for the array
                BAScaled = BAData * BAscaleFactor                 # Apply the scale factor using simple multiplication

                EVIscaleFactor = float(EVI_meta['scale_factor'])  # Search the metadata dictionary for the scale factor 
                EVIData[EVIData == EVIFill] = np.nan              # Set the fill value equal to NaN for the array
                EVIScaled = EVIData * EVIscaleFactor              # Apply the scale factor using simple multiplication

                BA_masked = np.ma.MaskedArray(BAScaled, np.in1d(BAqualityData, BAgoodQuality, invert = True))    # Apply QA mask to the BA data
                EVI_masked = np.ma.MaskedArray(EVIScaled, np.in1d(EVIqualityData, EVIgoodQuality, invert = True))# Apply QA mask to the EVI data
                EVI_BA = np.ma.MaskedArray(EVI_masked, np.in1d(BA_masked, BAVal, invert = True)) # Mask array, include only BurnArea
                EVI_mean = np.mean(EVI_BA.compressed())
            
                NDVI_result.append([EVIdate,EVI_mean])

            os.chdir(NDVI_inDir)  # changes back to NDVI input dir for steps in beg of loop
 
    
    result_df = pd.DataFrame(NDVI_result, columns=["Date","NDVI"])


    result_df['Date'] = pd.to_datetime(result_df['Date'], format='%m/%d/%Y')
    result_df = result_df.set_index('Date')
    result_series = result_df.resample('D').mean()

    result_series["NDVI"] = result_series["NDVI"].interpolate(method='linear')
    os.chdir(out_dir)
    result_series.to_csv('NDVI2019_2020.csv', index = True)
    print(result_series)   # Export statistics to CSV



# monthly
def getBAFile(BAF, month, year):
    for x in BAF:
        # File name metadata:
        BAproductId = x.split('_')[0]                                     # First: product name
        BAlayerId = x.split(BAproductId + '_')[1].split('_doy')[0]        # Second: layer name
        BAyeardoy = x.split(BAlayerId+'_doy')[1].split('_aid')[0]         # Third: date
        file_year = dt.datetime.strptime(BAyeardoy, '%Y%j').year            #* compares the date of the NDVI and BA to grab the right file, m and y are for NDVI tif
        file_month = dt.datetime.strptime(BAyeardoy, '%Y%j').month
        if file_year==year  and file_month == month:
            return(x) 


if __name__ == "__main__": # helps with "prototyping/forward declaring" functions
    # execute only if run as a script
    main()