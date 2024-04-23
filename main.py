import streamlit as st
import pandas as pd
import folium as folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster


def create_map(data, geojson, key_on, field, legend_name, m):
    folium.Choropleth(
        geo_data=geojson,
        data=data,
        columns=['district', 'num_rentals'],
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
                        }
    )

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
    FastMarkerCluster(data=locations,).add_to(m)


def load_gjson(geojson, field, m):
    x = folium.GeoJson(geojson)

    x.add_child(
        folium.features.GeoJsonTooltip(fields=[field], sticky=True, labels=False),
    )
    x.add_to(m)
    folium.LayerControl().add_to(m)

def grouped_airbnb_prices(airbnb):
    airbnb['price'] = airbnb['price'].str.replace('$', '').str.split('.').str[0].str.replace(',', '')
    airbnb['price'] = ((airbnb['price'].astype(float) *30) * 0.8)
    neighbourhood_prices = airbnb.groupby('neighbourhood_group_cleansed').agg({'price': 'mean', 'id': 'count'}).reset_index()
    neighbourhood_prices.columns = ['district', 'total', 'num_rentals']
    neighbourhood_prices['district'] = neighbourhood_prices['district'].str.upper()
    print(neighbourhood_prices)
    return neighbourhood_prices

def group_rentals(airbnb):
    neighbourhoods = airbnb.groupby('neighbourhood_group_cleansed').agg({'id': 'count'}).reset_index()
    neighbourhoods.columns = ['district','num_rentals']
    neighbourhoods['district'] = neighbourhoods['district'].str.upper()
    print(neighbourhoods)
    return neighbourhoods

def main():
    m = folium.Map(location=[40.416775, -3.703790])
    airbnb_data = load_airbnb_data()
    priced_data = grouped_airbnb_prices(airbnb_data)
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
        load_gjson(geojson_data, 'NOMBRE', m)
        if layer == 'Airbnb':
            filter = st.sidebar.selectbox(
                'Choose a filter',
                ('Price', 'Number of Beds','Number of Reviews')
            )
            # if filter == 'Price':
                
            #     price_filter = st.slider('Price', priced_data['total'].min(), priced_data['total'].max())
            #     priced_data = priced_data[priced_data['total'] <= price_filter]
            #     print(priced_data.columns)
            # el    
            if filter == 'Number of Beds':
                #remove the outlier
                bed_filter = st.slider('Number of Beds', airbnb_data['beds'].min(), airbnb_data['beds'].max(), (airbnb_data['beds'].min(), airbnb_data['beds'].max()))
                bed_data = airbnb_data[(airbnb_data['beds'] >= bed_filter[0]) & (airbnb_data['beds'] <= bed_filter[1])]
                bed_group = group_rentals(bed_data)
                m = folium.Map(location=[40.416775, -3.703790])
                add_airbnb_markers(m, bed_data)
                create_map(bed_group, './data/gjson/distritos.geojson', 'feature.properties.DISTRI_MT', 'NOMBRE' ,"Airbnb prices by District", m)
    else:
        geojson_data = './data/gjson/neighbourhoods.geojson'
        load_gjson(geojson_data, 'NOMBRE', m)
    folium_static(m, width=1000, height=800)

if __name__ == "__main__":
    main()