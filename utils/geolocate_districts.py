from shapely.geometry import Point
import pandas as pd
import geopandas as gpd

class GeolocateDistricts:
    def __init__(self, df_housing, gdf):
        self.df_housing = df_housing
        self.gdf = gdf

    def locate_points(self, output_file):
        for index_housing, row_housing in self.df_housing.iterrows():
            point = Point(row_housing['Latitude'], row_housing['Longitude'])
            found = False
            for index_geo, row_geo in self.gdf.iterrows():
                polygon = row_geo['geometry']
                if point.within(polygon):
                    found = True
                    print('FOUND for point', point, 'in', row_geo['NOMBRE'])
                    self.df_housing.loc[index_housing, 'district_geolocated'] = row_geo['NOMBRE']
                    break
            if not found:
                print('NOT FOUND for point', point)

        self.df_housing.to_csv(output_file, index=False)

if __name__ == "__main__":
    df_housing = pd.read_csv('./scrapers/csv/fotocasa_2023_located.csv')
    gdf = gpd.read_file('./data/gjson/distritos.geojson')
    geolocator = GeolocateDistricts(df_housing, gdf)
    geolocator.locate_points('./scrapers/csv/fotocasa_2023_located_districts.csv')