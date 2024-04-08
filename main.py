import streamlit as st
import pandas as pd
import folium as folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster


def load_data():
    popu_dist = pd.read_csv('./data/madrid/cleaned/popu_by_district.csv')
    popu_ngh = pd.read_csv('./data/madrid/cleaned/popu_by_neighbourhood.csv')
    
    paro_ngh = pd.read_csv('./data/madrid/cleaned/paro_by_neighbourhood.csv')
    paro_dist = pd.read_csv('./data/madrid/cleaned/paro_by_district.csv')
    return popu_dist, popu_ngh, paro_ngh, paro_dist

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


@st.cache_data
def load_airbnb_data():
    airbnb = pd.read_csv('./data/airbnb/detail_listings.csv')
    return airbnb

def add_airbnb_markers(m, airbnb):
    locations = airbnb[['latitude', 'longitude']].values.tolist()
    FastMarkerCluster(data=locations).add_to(m)

def grouped_airbnb_prices(airbnb):
    airbnb['price'] = airbnb['price'].str.replace('$', '').str.split('.').str[0].str.replace(',', '')
    airbnb['price'] = ((airbnb['price'].astype(float) *31) * 0.9)
    neighbourhood_prices = airbnb.groupby('neighbourhood_group_cleansed').agg({'price': 'mean', 'id': 'count'}).reset_index()
    neighbourhood_prices.columns = ['district', 'total', 'num_rentals']
    neighbourhood_prices['district'] = neighbourhood_prices['district'].str.upper()
    print(neighbourhood_prices)
    return neighbourhood_prices

def main():
    m = folium.Map(location=[40.416775, -3.703790])
    choice_map = st.selectbox("Select layer", ['Poblacion','Paro'])
    airbnb_data = load_airbnb_data()
    priced_data = grouped_airbnb_prices(airbnb_data)
    popu_dist, popu_ngh, paro_ngh, paro_dist = load_data()
    price_range = st.slider("Select price range", min_value=0, max_value=1000, value=(0, 7000))
    if st.selectbox("Select layer", ['Show Airbnb']):
        if price_range:
            airbnb_data = airbnb_data[(airbnb_data['price'] >= price_range[0]) & (airbnb_data['price'] <= price_range[1])]
        add_airbnb_markers(m, airbnb_data)
        create_map(priced_data, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT','NOMBRE', "Airbnb Prices by District", m)
    if choice_map == 'Poblacion':
        choice_layer = st.selectbox("Select layer", ['Districts', 'Neighbourhoods'])
        if choice_layer == 'Districts':
            create_map(popu_dist, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT','NOMBRE',"Population by District", m)

        if choice_layer == 'Neighbourhoods':
            create_map(popu_ngh, './data/gjson/neighbourhoods.geojson', 'feature.properties.NOMBRE', 'NOMBRE' ,"Population by Neighbourhoods", m)

    if choice_map == 'Paro':

        choice_layer = st.selectbox("Select layer", ['Districts', 'Neighbourhoods'])
        genre_paro = st.selectbox("Select paro", ['Hombres', 'Mujeres', 'Ambos sexos'])

        

        if choice_layer == 'Districts':
            paro_dist = paro_dist[paro_dist['genre'] == genre_paro]
            print(paro_dist)
            create_map(paro_dist, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT','NOMBRE', "Population by District", m)
        if choice_layer == 'Neighbourhoods':
            paro_ngh = paro_ngh[paro_ngh['genre'] == genre_paro]
            create_map(paro_ngh, './data/gjson/neighbourhoods.geojson', 'feature.properties.NOMBRE','NOMBRE', "Population by Neighbourhoods", m)
    folium_static(m, width=1000, height=800, )

if __name__ == "__main__":
    main()