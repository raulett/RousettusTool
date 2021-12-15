import pandas as pd
import geopandas as gpd

filename = 'F:\\YandexDisk\\Work\\SibGIS\\QGisPRJ\\20211004_Voshod_Chita\\Magn\\20210922\\20210922_Magn_Voshod_1.txt'
var_filename = 'F:\\YandexDisk\\Work\\SibGIS\\QGisPRJ\\20211004_Voshod_Chita\\Var\\09280022.txt'
df = pd.read_csv(filename, delimiter='\t')
print(df)
print(df.dtypes)

# gdf = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['LON'], df['LAT'], df['ALT']))
# print(gdf)
# print(gdf.dtypes)
# print(gdf.geom_type)
# gdf.plot()