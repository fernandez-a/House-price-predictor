from pages.maps import MapPage
from pages.graphs import Visualizations
from pages.predictions import Predictions
import streamlit as st

class Main:
    def main_page(self):
        st.write("""# House Price Prediction""")
        st.write("""This application allows you to explore different visualizations and predictions related to house prices.""")
        st.write("""The data used in this application is from Madrid, Spain and has been collected from Fotocasa, Airbnb, Comunidad de Madrid and OpenStreetMap.""")
        st.image('data/imgs/madrid_data.png', use_column_width=True)
        st.image('data/imgs/fotocasa.png', use_column_width=True)
        st.image('data/imgs/open_streetmap.png', use_column_width=True)
        st.image('data/imgs/airbnb.png', use_column_width=True)
    def main(self):
        st.sidebar.header('Page Selector')
        page = st.sidebar.selectbox(
            'Choose a page',
            ('Main','Maps Visualizations', 'Graphs Visualizations', 'Predictions')
        )
        if page == 'Main':
            self.main_page()
        elif page == 'Maps Visualizations': 
            MapPage().main()
        elif page == 'Graphs Visualizations':
            Visualizations().main()
        elif page == 'Predictions':
            Predictions().main()
if __name__ == '__main__':
    Main().main()
