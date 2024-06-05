import pandas as pd
from shapely.geometry import Point
from geopy.distance import geodesic
from tqdm import tqdm

class PointFinder:
    """
    A class that finds points within a given cluster radius.

    Args:
        cluster_radius (float): The radius of the cluster in meters.
        housing_file (str): The path to the housing data file.
        points_file (str): The path to the points data file.
        output_file (str): The path to the output file.

    Attributes:
        cluster_radius (float): The radius of the cluster in meters.
        housing_file (str): The path to the housing data file.
        points_file (str): The path to the points data file.
        output_file (str): The path to the output file.
    """

    def __init__(self, cluster_radius, housing_file, points_file, output_file, category):
        self.cluster_radius = cluster_radius
        self.housing_file = housing_file
        self.points_file = points_file
        self.output_file = output_file
        self.category = category

    def find_points(self):
        """
        Finds points within the specified cluster radius and saves the results to a CSV file.
        """
        df_housing = pd.read_csv(self.housing_file)
        df_housing.columns = df_housing.columns.str.lower()
        df_housing['id'] = df_housing.index
        df_housing['point'] = df_housing.apply(lambda x: Point(x['longitude'], x['latitude']), axis=1)
        points_raw = pd.read_csv(self.points_file)
        df_category = points_raw[points_raw['category'] == self.category]
        df_final = []
        df_category = df_category.to_dict('records')

        for row in tqdm(df_housing.itertuples(), total=len(df_housing)):
            house_id = row.id
            house_point = row.point
            cluster_polygon = house_point.buffer(self.cluster_radius / 111000) 

            for poi in df_category:
                poi_id = poi['id']
                poi_point = Point(poi['latitude'], poi['longitude'])

                if cluster_polygon.contains(poi_point):
                    df_final.append({'house_id': house_id, 'point_id': poi_id})
        df = pd.DataFrame(df_final)
        df.to_csv(self.output_file, index=False)


if __name__ == "__main__":
    finder = PointFinder(cluster_radius=500,
                            housing_file='../data/madrid/cleaned/fotocasa/fotocasa_2023_located.csv',
                            points_file='../data/points/pharmacies_located.csv',
                            output_file='../data/points/points_count/housing_pharmacies.csv',
                            category='pharmacy')
    finder.find_points()