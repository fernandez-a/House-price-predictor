import pandas as pd
from shapely.geometry import Point
from tqdm import tqdm

class AirbnbProcessor:
    """
    A class to process Airbnb data and generate output based on housing clusters.

    Parameters:
    - cluster_radius (float): The radius in meters used to define the cluster around each housing location.
    - housing_file (str): The file path to the CSV file containing housing data.
    - airbnb_file (str): The file path to the CSV file containing Airbnb data.
    - output_file (str): The file path to save the output CSV file.

    Methods:
    - process_data(): Process the data and generate the output CSV file.
    """

    def __init__(self, cluster_radius, housing_file, airbnb_file, output_file):
        self.cluster_radius = cluster_radius
        self.housing_file = housing_file
        self.airbnb_file = airbnb_file
        self.output_file = output_file

    def process_data(self):
        """
        Process the data and generate the output CSV file.

        Reads the housing and Airbnb data from CSV files, performs clustering based on the cluster radius,
        and saves the output to a CSV file.
        """
        df_housing = pd.read_csv(self.housing_file)
        df_housing.columns = df_housing.columns.str.lower()
        df_housing['id'] = df_housing.index
        df_housing['point'] = df_housing.apply(lambda x: Point(x['longitude'], x['latitude']), axis=1)
        points_raw = pd.read_csv(self.airbnb_file)
        df_2 = []

        for row in tqdm(df_housing.itertuples(), total=len(df_housing)):
            house_id = row.id
            house_point = row.point
            cluster_polygon = house_point.buffer(self.cluster_radius / 111000) 

            for _, airbnb in points_raw.iterrows():
                airbnb_id = airbnb['id']
                airbnb_point = Point(airbnb['latitude'], airbnb['longitude'])

                if cluster_polygon.contains(airbnb_point):
                    df_2.append({'house_id': house_id, 'airbnb': airbnb_id})

        df = pd.DataFrame(df_2)
        df.to_csv(self.output_file, index=False)

if __name__ == "__main__":
    processor = AirbnbProcessor(cluster_radius=500,
                                housing_file='../data/madrid/cleaned/fotocasa/fotocasa_2023_located.csv',
                                airbnb_file='../data/airbnb/detail_listings.csv',
                                output_file='../data/output/airbnb_clusters.csv')
    processor.process_data()