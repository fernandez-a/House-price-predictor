from folium.plugins import FastMarkerCluster
import json
import folium
from streamlit_folium import folium_static
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

    def create_map(self, data, geojson, key_on, field, legend_name, columns):
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
        folium_static(self.map, width=800, height=700)
        