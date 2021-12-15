import geopandas
from DataTypeParser import DataTypeParser
from ...DataTypes.MagneticData import MagneticData

class ParserCSV(DataTypeParser):
    def __init__(self):
        super(ParserCSV, self).__init__(data_type_name = 'CSV')

    def read_file(self, filename,
                  delimiter='\t',
                  ignore_rows_num=0,
                  lon_table_name='LON',
                  lat_table_name='LAT',
                  alt_table_name='ALT',
                  crs='epsg:4326'):


    def read_files(self, filenames):
        pass