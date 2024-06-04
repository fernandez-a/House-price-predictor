import pandas as pd

class AirbnbData:
    def __init__(self, filepath):
        self.data = self.load_data(filepath)

    @staticmethod
    def load_data(filepath):
        airbnb = pd.read_csv(filepath)
        airbnb['price'] = airbnb['price'].str.replace('$', '').str.split('.').str[0].str.replace(',', '')
        airbnb['price_month']  = ((airbnb['price'].astype(float) *30) * 0.8)
        return airbnb