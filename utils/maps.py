import streamlit as st
import pandas as pd
from utils.airbnbdata import AirbnbData
from utils.map_utils import Map

class MapPage:
    def __init__(self):
        self.airbnb_data = AirbnbData('./data/airbnb/detail_listings.csv').data
        self.housing_data = pd.read_csv('./data/madrid/cleaned/fotocasa_2023.csv')
        self.map = Map([40.416775, -3.703790])

    def main(self):
        st.title('Maps Visualizations')
        st.sidebar.header('Map options')
        option = st.sidebar.selectbox(
            'Choose an option',
            ('District', 'Neighbourhood')
        )
        
            
        if option == 'District':
            geojson_data = './data/gjson/distritos.geojson'
            layer = st.sidebar.selectbox(
            'Choose a layer',
            ('Population', 'Unemployment', 'Airbnb','House Properties')
            )   
            if layer == 'Population':
                pop_columns = ['district','total']
                population = pd.read_csv('./data/madrid/cleaned/total_by_district.csv')
                population['district'] = population['district'].str.upper()
                self.map.create_map(population, geojson_data, 'feature.properties.DISTRI_MT','NOMBRE',"Population by District", columns=pop_columns)
            
            elif layer == 'Unemployment':
                genre = st.selectbox("Select genre", ['Hombres', 'Mujeres', 'Ambos sexos'])
                paro_columns = ['district','total']
                unemployment = pd.read_csv('./data/madrid/cleaned/paro_by_district.csv')
                unemployment = unemployment[unemployment['genre'] == genre]
                unemployment['district'] = unemployment['district'].str.upper()
                self.map.create_map(unemployment, geojson_data, 'feature.properties.DISTRI_MT','NOMBRE',"Unemployment by District", columns=paro_columns)
            
            elif layer == 'Airbnb':
                #click the price button to filter by price
                filter = st.selectbox("Filter by", ['Price'])
                airbnb_columns = ['district', 'total', 'num_rentals']

                if filter == 'Price':
                    self.airbnb_data.to_csv('./data/madrid/cleaned/airbnb_prices_all.csv', index=False)                
                    priced_data_group = self.grouped_airbnb_prices(self.airbnb_data)
                    price_filter = st.slider('Price', priced_data_group['total'].min(), priced_data_group['total'].max())
                    priced_data = priced_data_group[priced_data_group['total'] <= price_filter]
                    self.map.create_map(priced_data, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT', 'NOMBRE' ,"Airbnb prices by District", airbnb_columns)

            elif layer == 'House Properties':
                house_columns = ['district', 'price']
                fotocasa_group = self.group_fotocasa('district')
                self.map.create_map(fotocasa_group, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT', 'NOMBRE' ,"House prices by District", house_columns)
        
        else:           
            geojson_data = './data/gjson/neighbourhoods.geojson'
            layer = st.sidebar.selectbox(
            'Choose a layer',
            ('Population', 'Unemployment','House Properties')
            )   
            if layer == 'Population':
                pop_columns = ['neigbourhood','total']
                population_nh = pd.read_csv('./data/madrid/cleaned/total_by_neighbourhood.csv')
                self.map.create_map(population_nh, geojson_data, 'feature.properties.NOMBRE', 'NOMBRE' ,"Population by Neighbourhoods", columns=pop_columns)
        
            elif layer == 'Unemployment':
                genre = st.selectbox("Select genre", ['Hombres', 'Mujeres', 'Ambos sexos'])
                paro_columns = ['neighbourhood','total']
                unemployment_nh = pd.read_csv('./data/madrid/cleaned/paro_by_neighbourhood.csv')
                unemployment_nh = unemployment_nh[unemployment_nh['genre'] == genre]
                self.map.create_map(unemployment_nh, geojson_data, 'feature.properties.NOMBRE', 'NOMBRE' ,"Unemployment by Neighbourhoods - " + genre, columns=paro_columns)
        
            elif layer == 'House Properties':
                house_columns = ['neighbourhood', 'price']
                fotocasa_group = self.group_fotocasa('neighbourhood')
                self.map.create_map(fotocasa_group, geojson_data, 'feature.properties.BARRIO_MT', 'BARRIO_MT' ,"House prices by Neighbourhoods", house_columns)
        
        self.map.display()

    def grouped_airbnb_prices(self, data):
        
        neighbourhood_prices = data.groupby('neighbourhood_group_cleansed').agg({'price_month': 'mean', 'id': 'count'}).reset_index()
        neighbourhood_prices.columns = ['district', 'total', 'num_rentals']
        neighbourhood_prices['district'] = neighbourhood_prices['district'].str.upper()
        return neighbourhood_prices

    def group_rentals(self, airbnb):
        neighbourhoods = airbnb.groupby('neighbourhood_group_cleansed').agg({'id': 'count'}).reset_index()
        neighbourhoods.columns = ['district','num_rentals']
        neighbourhoods['district'] = neighbourhoods['district'].str.upper()
        return neighbourhoods

    def group_fotocasa(self, key):
        self.housing_data[key] = self.housing_data[key].str.upper()
        self.housing_data.columns = self.housing_data.columns.str.lower()
        return self.housing_data.groupby(key).agg({'price': 'mean'}).reset_index()

if __name__ == "__main__":
    MapPage().main()
