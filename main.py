from maps import MapPage
from graphs import Visualizations
import streamlit as st

class Main:

    def main(self):
        st.sidebar.header('Page Selector')
        page = st.sidebar.selectbox(
            'Choose a page',
            ('Maps Visualizations', 'Graphs Visualizations')
        )
        if page == 'Maps Visualizations': 
            MapPage().main()
        elif page == 'Graphs Visualizations':
            Visualizations().main()

if __name__ == '__main__':
    Main().main()