import geopandas
import pandas as pd
import geopandas as gpd


class MagneticData:

    def read_magnetic_csv(self, filename,
                          delimiter='\t',
                          ignore_rows_num=0,
                          lon_table_name='LON',
                          lat_table_name='LAT',
                          alt_table_name='ALT',
                          crs='epsg:4326'):
        input_df = pd.read_csv(filename, delimiter=delimiter)
        input_gdf = gpd.GeoDataFrame(input_df,
                                     geometry=gpd.points_from_xy(input_df[lon_table_name], input_df[lat_table_name],
                                                                 input_df[alt_table_name]))
        return input_gdf
