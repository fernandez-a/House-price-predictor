import requests
import json
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

class Fotocasa:
    headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.fotocasa.es/',
                'Origin': 'https://www.fotocasa.es',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
            }
    properties = []
    data = []


    def scrape_data(self):
        url = 'https://web.gw.fotocasa.es/v2/propertysearch/search?combinedLocationIds=724,14,28,173,0,28079,0,0,0&culture=es-ES&includePurchaseTypeFacets=true&isMap=false&isNewConstructionPromotions=false&latitude=40.4096&longitude=-3.68624&pageNumber=1&platformId=1&propertyTypeId=2&sortOrderDesc=true&sortType=scoring&transactionTypeId=1'
        properties = []
        response = requests.get(url, headers=self.headers)
        b = json.loads(response.text)
        pages = int((b['count'] / 30)+1)
        for i in range(0, pages+1):
            print('Scrapping page:{}'.format(i))
            base_url = f'https://web.gw.fotocasa.es/v2/propertysearch/search?combinedLocationIds=724,14,28,173,0,28079,0,0,0&culture=es-ES&includePurchaseTypeFacets=true&isMap=false&isNewConstructionPromotions=false&latitude=40.4096&longitude=-3.68624&pageNumber={i}&platformId=1&propertyTypeId=2&sortOrderDesc=true&sortType=scoring&transactionTypeId=1'
            try:
                json_rental = json.loads(requests.get(base_url, headers=self.headers).text)
                properties.append(json_rental['realEstates'])
                print('Sleeping')
                sleep(5)
            except Exception as e:
                print(e)
                continue
        self.properties = properties

    
    def get_features(self, features):
        feature_dict = {feature['key']: feature['value'][0] for feature in features}
        bathrooms = feature_dict.get('bathrooms', 0)
        floor = feature_dict.get('floor', 0)
        air_conditioner = feature_dict.get('air_conditioner', 0)
        heater = feature_dict.get('heater', 0)
        elevator = feature_dict.get('elevator', 0)
        swimming_pool = feature_dict.get('swimming_pool', 0)
        rooms = feature_dict.get('rooms', 0)
        surface = feature_dict.get('surface', 0)
        conservationState = feature_dict.get('conservationState', 0)
        garden = feature_dict.get('garden', 0)
        terrace = feature_dict.get('terrace', 0)
        balcony = feature_dict.get('balcony', 0)
        parking = feature_dict.get('parking', 0)

        return bathrooms, floor, air_conditioner, heater, elevator, swimming_pool, rooms, surface, conservationState, garden, terrace, balcony, parking

    def save_data(self):
        columns = ['address','neighbourhood', 'district', 'latitud', 'longitud', 'zipcode', 'date', 'price', 'bathrooms','floor','air_conditioner','heater','elevator','swimming_pool','rooms','surface','conservationState','garden','terrace','balcony','parking']
        for i in self.properties:
            for j in i: 
                feature_dict = []
                features = j['features']
                feature_dict = [{feature['key']: feature['value'][0]} for feature in features]
                address = j['address']
                street = address['ubication']
                neighbourhood = address['location']['level8']
                district = address['location']['level7']
                latitud = address['coordinates']['latitude']
                longitud = address['coordinates']['longitude']
                zipcode = address['zipCode']
                date = j['date']
                price = j['transactions'][0]['value'][0]
                bathrooms, floor, air_conditioner, heater, elevator, swimming_pool, rooms, surface, conservationState, garden, terrace, balcony, parking = self.get_features(features)
                self.data.append([street,neighbourhood, district, latitud, longitud, zipcode, date, price, bathrooms, floor, air_conditioner, heater, elevator, swimming_pool, rooms, surface, conservationState, garden, terrace, balcony, parking])
        df = pd.DataFrame(self.data, columns=columns)
        df.to_csv('../data/madrid/cleaned/fotocasa/fotocasa.csv', index=False)
    def run(self):
        self.scrape_data()
        self.save_data()

if __name__ == "__main__":
    fotocasa = Fotocasa()
    fotocasa.run()