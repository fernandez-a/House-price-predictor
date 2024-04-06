import streamlit as st
import pandas as pd
import folium as folium
from streamlit_folium import folium_static

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

def main():
    m = folium.Map(location=[40.416775, -3.703790])
    choice_map = st.selectbox("Select layer", ['Poblacion','Paro'])
    popu_dist, popu_ngh, paro_ngh, paro_dist = load_data()

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