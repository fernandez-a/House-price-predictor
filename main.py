import streamlit as st
import pandas as pd
import folium as folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster
import json

class AirbnbData:
    def __init__(self, filepath):
        self.data = self.load_data(filepath)

    @staticmethod
    def load_data(filepath):
        airbnb = pd.read_csv(filepath)
        airbnb['price'] = airbnb['price'].str.replace('$', '').str.split('.').str[0].str.replace(',', '')
        airbnb['price_month']  = ((airbnb['price'].astype(float) *30) * 0.8)
        return airbnb

class Map:
    def __init__(self, location):
        self.map = folium.Map(location=location)

    def add_markers(self, data):
        locations = data[['latitude', 'longitude']].values.tolist()
        FastMarkerCluster(data=locations,).add_to(self.map)


    def load_gjson(self, filepath, field):
        with open(filepath, 'r') as file:
            geojson = json.load(file)

        x = folium.GeoJson(geojson)

        x.add_child(
            folium.features.GeoJsonTooltip(fields=[field], sticky=True, labels=False),
        )
        x.add_to(self.map)
        folium.LayerControl().add_to(self.map)

    def create_map(self, data, geojson, key_on, field, legend_name,columns):
        print(data)
        folium.Choropleth(
            geo_data=geojson,
            data=data,
            columns=columns,
            key_on=key_on,
            fill_color="RdYlBu_r",
            fill_opacity=0.7,
            line_opacity=0.1,
            legend_name=legend_name).add_to(self.map)

        x = folium.GeoJson(geojson,
                        style_function=lambda feature: {
                            'fillColor': None,
                            'color': 'lightgrey',
                            'weight': 2,
                            'fillOpacity': 0,
                            }
        )

        x.add_child(
            folium.features.GeoJsonTooltip(fields=[field], sticky=True, labels=False),
        )
        x.add_to(self.map)
        folium.LayerControl().add_to(self.map)

    def display(self):
        folium_static(self.map, width=1000, height=800)

class Main:
    def __init__(self):
        self.airbnb_data = AirbnbData('./data/airbnb/detail_listings.csv').data
        self.map = Map([40.416775, -3.703790])

    def main(self):
        st.sidebar.header('Map options')
        option = st.sidebar.selectbox(
            'Choose an option',
            ('District', 'Neighbourhood')
        )
        layer = st.sidebar.selectbox(
            'Choose a layer',
            ('Population', 'Unemployment', 'Airbnb')
        )
            
        if option == 'District':
            geojson_data = './data/gjson/distritos.geojson'
            self.map.load_gjson(geojson_data, 'NOMBRE')
            if layer == 'Population':
                pop_columns = ['district','total']
                population = pd.read_csv('./data/madrid/cleaned/popu_by_district.csv')
                population['district'] = population['district'].str.upper()
                self.map = Map([40.416775, -3.703790])
                self.map.create_map(population, geojson_data, 'feature.properties.DISTRI_MT','NOMBRE',"Population by District", columns=pop_columns)
            elif layer == 'Unemployment':
                paro_columns = ['district','total']
                unemployment = pd.read_csv('./data/madrid/cleaned/paro_by_district.csv')
                unemployment['district'] = unemployment['district'].str.upper()
                self.map = Map([40.416775, -3.703790])
                self.map.create_map(unemployment, geojson_data, 'feature.properties.DISTRI_MT','NOMBRE',"Unemployment by District", columns=paro_columns)
            if layer == 'Airbnb':
                filter = st.sidebar.selectbox(
                    'Choose a filter',
                    ('Price', 'Number of Beds','Number of Reviews')
                )
                airbnb_columns = ['district', 'total', 'num_rentals']
                if filter == 'Price':
                    self.airbnb_data.to_csv('./data/madrid/cleaned/airbnb_prices_all.csv', index=False)                
                    price_filter = st.slider('Price', int(self.airbnb_data['price_month'].min()), int(self.airbnb_data['price_month'].max()))
                    priced_data = self.airbnb_data[(self.airbnb_data['price_month'] >= price_filter[0]) & (self.airbnb_data['price_month'] <= price_filter[1])]
                    priced_data_group = self.grouped_airbnb_prices(priced_data)
                    priced_data_group.to_csv('./data/madrid/cleaned/airbnb_prices.csv', index=False)
                    self.map = Map([40.416775, -3.703790])
                    self.map.add_markers(priced_data)
                    self.map.create_map(priced_data_group, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT', 'NOMBRE' ,"Airbnb prices by District", airbnb_columns)

                elif filter == 'Number of Beds':

                    bed_filter = st.slider('Number of Beds', self.airbnb_data['beds'].min(), self.airbnb_data['beds'].max(), (self.airbnb_data['beds'].min(), self.airbnb_data['beds'].max()))
                    bed_data = self.airbnb_data[(self.airbnb_data['beds'] >= bed_filter[0]) & (self.airbnb_data['beds'] <= bed_filter[1])]
                    bed_group = self.group_rentals(bed_data)
                    self.map = Map([40.416775, -3.703790])
                    self.map.add_markers(bed_data)
                    self.map.create_map(bed_group, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT', 'NOMBRE' ,"Number of beds by District", airbnb_columns)

                elif filter == 'Number of Reviews':

                    review_filter = st.slider('Number of Reviews', self.airbnb_data['number_of_reviews'].min(), self.airbnb_data['number_of_reviews'].max(), (self.airbnb_data['number_of_reviews'].min(), self.airbnb_data['number_of_reviews'].max()))
                    review_data = self.airbnb_data[(self.airbnb_data['number_of_reviews'] >= review_filter[0]) & (self.airbnb_data['number_of_reviews'] <= review_filter[1])]
                    review_group = self.group_rentals(review_data)
                    self.map = Map([40.416775, -3.703790])
                    self.map.add_markers(review_data)
                    self.map.create_map(review_group, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT', 'NOMBRE' ,"Number of reviews by District", airbnb_columns)

        else:           
            geojson_data = './data/gjson/neighbourhoods.geojson'
            self.map.load_gjson(geojson_data, 'NOMBRE')
            if layer == 'Population':
                

                pop_columns = ['district','total']
                population_nh = pd.read_csv('./data/madrid/cleaned/popu_by_neighbourhood.csv')
                self.map = Map([40.416775, -3.703790])
                self.map.create_map(population_nh, geojson_data, 'feature.properties.NOMBRE', 'NOMBRE' ,"Population by Neighbourhoods", columns=pop_columns)
        
            elif layer == 'Unemployment':
                
                genre = st.selectbox("Select genre", ['Hombres', 'Mujeres', 'Ambos sexos'])
                paro_columns = ['district','total']
                unemployment_nh = pd.read_csv('./data/madrid/cleaned/paro_by_neighbourhood.csv')
                unemployment_nh = unemployment_nh[unemployment_nh['genre'] == genre]
                print(unemployment_nh.total.max())
                self.map = Map([40.416775, -3.703790])
                self.map.create_map(unemployment_nh, geojson_data, 'feature.properties.NOMBRE', 'NOMBRE' ,"Unemployment by Neighbourhoods", columns=paro_columns)
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


    def create_map(data, geojson, key_on, field, legend_name, m):
        folium.Choropleth(
            geo_data=geojson,
            data=data,
            columns=['district', 'total'],
            key_on=key_on,
            fill_color="RdYlBu_r",
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name=legend_name).add_to(m)

        x = folium.GeoJson(geojson,
                        style_function=lambda feature: {
                            'fillColor': None,
                            'color': 'lightgrey',
                            'weight': 2,
                            'fillOpacity': 0,
                        })

        x.add_child(
            folium.features.GeoJsonTooltip(fields=[field], sticky=True, labels=False),
        )
        x.add_to(m)
        folium.LayerControl().add_to(m)
if __name__ == "__main__":
    Main().main()