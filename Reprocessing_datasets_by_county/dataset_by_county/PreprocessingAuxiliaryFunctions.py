import geopandas as gpd
import os

class PreprocessingAuxiliaryFunctions:
    def __init__(self):
        pass

    def read_geojson(self):
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

    def read_geojson_geodf(self):
        """ Loading county boundaries via geojson - returns arr of county geometry shapes """
        # source: https://gis.data.ca.gov/datasets/8713ced9b78a4abb97dc130a691a8695_0?geometry=-146.754%2C31.049%2C-91.251%2C43.258&page=7
        CA_cnty_geojson_link = 'https://opendata.arcgis.com/datasets/8713ced9b78a4abb97dc130a691a8695_0.geojson'
        return gpd.read_file(CA_cnty_geojson_link)
    
    def extract_shapes_from_county_geometry(self, county_geodf):
        # * storing all boundaries in list var shapes
        return [x for x in county_geodf['geometry']]

        shapes = [x for x in county_geodf['geometry']]
        county_shapes = []
        for i in range(58):
            county_shapes.append(shapes[i])
        return county_shapes

    def extracting_good_quality_vals_from_lut(self, lut):
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

    def create_abs_path_from_relative(self,relative_dir_path):
        """ Creates relative path from current directory to input file: 'input_data_files' in project dir """
        absolutepath = os.path.abspath(__file__)
        fileDirectory = os.path.dirname(absolutepath)
        return os.path.join(fileDirectory, relative_dir_path)  #Navigate to relative_dir_path directory

    def go_to_parent_dir(self):
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)