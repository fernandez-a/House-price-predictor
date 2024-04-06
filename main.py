
import streamlit as st
import pandas as pd
import folium as folium
from streamlit_folium import folium_static

m = folium.Map(location=[40.416775, -3.703790])
choice_map = st.selectbox("Select layer", ['Poblacion','Paro'])




if choice_map == 'Poblacion':
    choice_layer = st.selectbox("Select layer", ['Districts', 'Neighbourhoods'])
    data_ngh = pd.read_csv('./data/madrid/cleaned/popu_by_neighbourhood.csv')
    data_dist = pd.read_csv('./data/madrid/cleaned/popu_by_district.csv')
    print(data_ngh.head())
    if choice_layer == 'Districts':
        folium.Choropleth(
                        geo_data='./data/gjson/distritos.geojson',
                        data=data_dist,
                        columns=['district', 'total'],
                        key_on='feature.properties.DISTRI_MT',
                        fill_color="YlGn",
                        fill_opacity=0.7,
                        line_opacity=.1,
                        legend_name="Population by District").add_to(m)

        x = folium.GeoJson('./data/gjson/distritos.geojson',
                        style_function=lambda feature: {
                            'fillColor': None,
                            'color': 'lightgrey',
                            'weight': 2,
                            'fillOpacity': 0,
                        })

        x.add_child(
            folium.features.GeoJsonTooltip(fields=['NOMBRE'], sticky=True, labels=False),
        )
        x.add_to(m)
        folium.LayerControl().add_to(m)

    if choice_layer == 'Neighbourhoods':
        folium.Choropleth(
                        geo_data='./data/gjson/neighbourhoods.geojson',
                        data=data_ngh,
                        columns=['district', 'total'],
                        key_on='feature.properties.NOMBRE',
                        fill_color="YlGn",
                        fill_opacity=0.7,
                        line_opacity=.1,
                        legend_name="Population by Neighbourhoods").add_to(m)

        x = folium.GeoJson('./data/gjson/neighbourhoods.geojson',
                    style_function=lambda feature: {
                        'fillColor': None,
                        'color': 'lightblue',
                        'weight': 2,
                        'fillOpacity': 0,
                    })
        x.add_child(
            folium.features.GeoJsonTooltip(fields=['NOMBRE'], sticky=True, labels=False),
        )
        x.add_to(m)
        folium.LayerControl().add_to(m)

# if choice_map == 'Paro':
#     data = pd.read_csv('./data/madrid/cleaned/paro_by_neighbourhood.csv')
#     select_paro = st.selectbox("Select paro", ['Hombres', 'Mujeres', 'Ambos sexos'])
#     select_layer = st.selectbox("Select layer", ['Neighbourhoods', 'Districts'])
#     data = data[data['genre'] == select_paro]

#     if select_layer == 'Neighbourhoods':
#         folium.Choropleth(
#                     geo_data='./data/gjson/neighbourhoods.geojson',
#                     data=data,
#                     columns=['district', 'total'],
#                     key_on='feature.properties.NOMDIS',
#                     fill_color="RdYlBu_r",
#                     fill_opacity=0.7,
#                     line_opacity=.1,
#                     legend_name="{} Unemployment by Neighbourhood".format(select_paro),
#                     ).add_to(m)
#         x = folium.GeoJson('./data/gjson/neighbourhoods.geojson',
#                         style_function=lambda feature: {
#                             'fillColor': None,
#                             'color': 'lightblue',
#                             'weight': 2,
#                             'fillOpacity': 0,
#                         })
#         x.add_child(
#             folium.features.GeoJsonTooltip(fields=['NOMDIS'], sticky=True, labels=False),
#         )
#         x.add_to(m)
#     if select_layer == 'Districts':

#         folium.Choropleth(
#                         geo_data='./data/gjson/distritos.geojson',
#                         data=data,
#                         columns=['district', 'total'],
#                         key_on='feature.properties.NOMBRE',
#                         fill_color="RdYlBu_r",
#                         fill_opacity=0.7,
#                         line_opacity=.1,
#                         legend_name="{} Unemployment by District".format(select_paro)
#                         ).add_to(m)

#         x = folium.GeoJson('./data/gjson/distritos.geojson',
#                     style_function=lambda feature: {
#                         'fillColor': None,
#                         'color': 'lightblue',
#                         'weight': 2,
#                         'fillOpacity': 0,
#                     })
#         x.add_child(
#             folium.features.GeoJsonTooltip(fields=['NOMBRE'], sticky=True, labels=False),
#         )
#         x.add_to(m)
folium_static(m, width=1000, height=800, )