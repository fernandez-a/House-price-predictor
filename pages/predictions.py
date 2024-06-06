import streamlit as st
import folium
from streamlit_folium import folium_static
import pickle
import re
from shapely.geometry import Point
from utils.map_utils import Map
import numpy as np
import json
import pandas as pd
class Predictions():
    def main(self):
        st.title('Predictions Page')
        st.write('Fill in the information about the property to get the price prediction')

        st.write('*Note: fill the coordinates following the format: latitude, longitude*')
        col1, col2, col3 = st.columns(3)
        error = False
        with col1:
            zipcode = st.text_input('Zipcode')
            if zipcode and not re.match("^[0-9]+$", zipcode):
                st.error('Zipcode should only contain numbers')
                error = True
            elif len(zipcode) != 5 and zipcode:
                error = True
                st.error('Zipcode should have 5 digits')
            coordinates = st.text_input('Coordinates')
            if coordinates and not re.match("^[-+]?[0-9]*\.?[0-9]+\s*,\s*[-+]?[0-9]*\.?[0-9]+$", coordinates):
                error = True
                st.error('Coordinates should be in the format: latitude, longitude')

            elif len(coordinates.split(',')) != 2 and coordinates:
                error = True
                st.error('Coordinates should be in the format: latitude, longitude')
            terrace = st.selectbox('Terrace', ['Yes', 'No'])
            surface = st.text_input('Surface')
            if surface and not re.match("^[0-9]+$", surface):
                error = True
                st.error('Surface should only contain numbers')
            floors = st.text_input('Floor')
            if floors and not re.match("^[0-9]+$", floors):
                error = True
                st.error('Floor should only contain numbers')
        with col2:
            rooms = st.text_input('Rooms')
            if rooms and not re.match("^[0-9]+$", rooms):
                error = True
                st.error('Rooms should only contain numbers')
            bathrooms = st.text_input('Bathrooms')
            if bathrooms and not re.match("^[0-9]+$", bathrooms):
                error = True
                st.error('Bathrooms should only contain numbers')
            swimming_pool = st.selectbox('Swimming Pool', ['Yes', 'No'])
            balcony = st.selectbox('Balcony', ['Yes', 'No'])
            neighbourhood = st.text_input('Neighbourhood')
            if neighbourhood and not re.match("^[a-zA-Z]+$", neighbourhood):
                error = True
                st.error('Neighbourhood should only contain letters')
        with col3:
            elevator = st.selectbox('Elevator', ['Yes', 'No'])
            air_conditioner = st.selectbox('Air Conditioner', ['Yes', 'No'])
            heater = st.selectbox('Heater', ['Yes', 'No'])
            parking = st.selectbox('Parking', ['Yes', 'No'])
            district = st.text_input('District')
            if district and not re.match("^[a-zA-Z]+$", district):
                error = True
                st.error('District should only contain letters')
        button = st.button('Predict Price')

        map = folium.Map(location=['40.429820573538464', '-3.6753164315647533'], zoom_start=12)
        with open('./notebooks/district_mapping.json', 'r') as f:
            district_mapping = json.load(f)

        with open('./notebooks/neighbourhood_mapping.json', 'r') as f:
            neighbourhood_mapping = json.load(f)


        district_encoded = district.title()
        if district_encoded in district_mapping:
            district_encoded = district_mapping[district]
            district_encoded = str(district_encoded)
        elif district and district_encoded not in district_mapping:
            st.error('Invalid district')
        neighbourhood_encoded = neighbourhood.title()
        if neighbourhood_encoded in neighbourhood_mapping:
            neighbourhood_encoded = neighbourhood_mapping[neighbourhood_encoded]
            neighbourhood_encoded = str(neighbourhood_encoded)
        elif neighbourhood and neighbourhood_encoded not in neighbourhood_mapping:
            st.error('Invalid neighbourhood')
        
        features_list = [zipcode, coordinates, rooms, bathrooms, floors, swimming_pool, elevator, air_conditioner, heater, parking, balcony, terrace, district_encoded, neighbourhood_encoded, surface]
        
        if button and all(features_list) and error == False:
            print('Button clicked')
            latitude, longitude = coordinates.split(',')
            features_list.append(latitude)
            features_list.append(longitude)
            features_list.remove(coordinates)
            csv = self.construct_data(features_list)

            csv = self.find_points(csv)
            csv = self.find_supermarkets_and_jewlery(csv)
            csv = self.find_airbnb(csv)
            csv = csv.drop(columns=['id', 'point'])

            csv = csv[['zipcode', 'longitude', 'latitude', 'rooms', 'bathrooms', 'floor', 'elevator', 'air_conditioner', 'heater', 'parking', 'balcony', 'terrace', 'swimming_pool', 'count_airbnb_500', 'count_college_500', 'count_dentist_500', 'count_fast_food_500', 'count_jewelry_500', 'count_university_500', 'count_restaurant_500', 'count_hospital_500', 'count_pharmacy_500', 'count_supermarket_500', 'rooms/m2', 'bathrooms/m2', 'surface_log', 'district_encoded', 'neighbourhood_encoded']]
            model = pickle.load(open('./models/rf_model.pkl', 'rb'))
            log_prediction = model.predict(csv)
            prediction = np.exp(log_prediction)
            price = prediction[0].round(2).astype(str).replace('.', ',')
            st.write(f'The predicted price for the property is: {price} €')
            folium.Marker(
                location=[latitude, longitude],
                popup=f'Price: {price} €',
                icon=folium.Icon(color='blue')
            ).add_to(map)
        elif (button and not all(features_list)) or error == True:
            st.error('Please fill in all the fields in the correct format')
        folium_static(map, width=700, height=300)

    def construct_data(self, data):
        data = [int(x) if x.isdigit() else x for x in data]
        data = [0 if x == 'No' else 1 if x == 'Yes' else x for x in data]
        data = [float(x) if isinstance(x, str) else x for x in data]
        
        zipcode ,rooms, bathrooms, floors, swimming_pool, elevator, air_conditioner, heater, parking, balcony, terrace, district, neighbourhood,surface, latitude, longitude = data
        rooms_m2 = rooms / surface
        bathrooms_m2 = bathrooms / surface
        headers = 'zipcode,rooms,bathrooms,floor,swimming_pool,elevator,air_conditioner,heater,parking,balcony,terrace,district_encoded,neighbourhood_encoded,surface_log,rooms/m2,bathrooms/m2,latitude,longitude'
        csv = f'{zipcode},{rooms},{bathrooms},{floors},{swimming_pool},{elevator},{air_conditioner},{heater},{parking},{balcony},{terrace},{district},{neighbourhood},{surface},{rooms_m2},{bathrooms_m2},{longitude},{latitude}'

        df = pd.DataFrame([csv.split(',')], columns=headers.split(','))
        return df
    

    def find_supermarkets_and_jewlery(self, csv):
        categories = ['supermarket', 'jewelry']
        jewlery = pd.read_csv('./data/points/jewlery.csv')
        supermarkets = pd.read_csv('./data/points/supermarket.csv')
        df_housing = csv
        df_housing.columns = df_housing.columns.str.lower()
        df_housing['id'] = df_housing.index
        df_housing['point'] = df_housing.apply(lambda x: Point(x['longitude'], x['latitude']), axis=1)
        supermarkets_count = 0
        jewlery_count = 0
        for category in categories:
            if category == 'supermarket':
                df_category = supermarkets
            else:
                df_category = jewlery
            df_category = df_category.to_dict('records')
            for row in df_housing.itertuples():
                house_point = row.point
                cluster_polygon = house_point.buffer(500 / 111000) 
                for poi in df_category:
                    poi_point = Point(poi['latitude'], poi['longitude'])
                    if cluster_polygon.contains(poi_point):
                        if category == 'supermarket':
                            supermarkets_count += 1
                        else:
                            jewlery_count += 1
        df_housing['count_supermarket_500'] = supermarkets_count
        df_housing['count_jewelry_500'] = jewlery_count
        return df_housing

    def find_points(self, csv):
        categories = ['college', 'dentist', 'fast_food', 'university', 'restaurant', 'hospital', 'pharmacy']
        df_housing = csv
        df_housing.columns = df_housing.columns.str.lower()
        df_housing['id'] = df_housing.index
        df_housing['point'] = df_housing.apply(lambda x: Point(x['longitude'], x['latitude']), axis=1)

        points_raw = pd.read_csv('./data/points/amenity.csv')
        college = 0
        dentist = 0
        fast_food = 0
        university = 0
        restaurant = 0
        hospital = 0
        pharmacy = 0
        for category in categories:
            df_category = points_raw[points_raw['category'] == category]
            df_category = df_category.to_dict('records')
            for row in df_housing.itertuples():
                house_point = row.point
                cluster_polygon = house_point.buffer(500 / 111000) 
                for poi in df_category:
                    poi_point = Point(poi['latitude'], poi['longitude'])
                    if cluster_polygon.contains(poi_point):
                        if category == 'college':
                            college += 1
                        elif category == 'dentist':
                            dentist += 1
                        elif category == 'fast_food':
                            fast_food += 1
                        elif category == 'university':
                            university += 1
                        elif category == 'restaurant':
                            restaurant += 1
                        elif category == 'hospital':
                            hospital += 1
                        elif category == 'pharmacy':
                            pharmacy += 1
        df_housing['count_dentist_500'] = college
        df_housing['count_college_500'] = dentist
        df_housing['count_fast_food_500'] = fast_food
        df_housing['count_university_500'] = university
        df_housing['count_restaurant_500'] = restaurant
        df_housing['count_hospital_500'] = hospital
        df_housing['count_pharmacy_500'] = pharmacy
        return df_housing
    
    def find_airbnb(self,csv):
        df_housing = csv
        df_housing.columns = df_housing.columns.str.lower()
        df_housing['id'] = df_housing.index
        df_housing['point'] = df_housing.apply(lambda x: Point(x['longitude'], x['latitude']), axis=1)
        points_raw = pd.read_csv('./data/airbnb/detail_listings.csv')
        airbnb_count = 0
        for row in df_housing.itertuples():
            house_point = row.point
            cluster_polygon = house_point.buffer(500 / 111000) 

            for _, airbnb in points_raw.iterrows():
                airbnb_point = Point(airbnb['latitude'], airbnb['longitude'])

                if cluster_polygon.contains(airbnb_point):
                    airbnb_count +=1
        df_housing['count_airbnb_500'] = airbnb_count
        return df_housing
