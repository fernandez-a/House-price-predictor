from utils.maps import MapPage
from utils.graphs import Visualizations
from utils.predictions import Predictions
import streamlit as st

class Main:

    def main(self):
        st.sidebar.header('Page Selector')
        page = st.sidebar.selectbox(
            'Choose a page',
            ('Maps Visualizations', 'Graphs Visualizations', 'Predictions')
        )
        if page == 'Maps Visualizations': 
            MapPage().main()
        elif page == 'Graphs Visualizations':
            Visualizations().main()
        else:
            Predictions().main()
if __name__ == '__main__':
    Main().main()