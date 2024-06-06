import streamlit as st
import pandas as pd
import folium as folium
import streamlit as st
import pandas as pd
from plotly import express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

class Visualizations:
    def __init__(self):
        self.sq2m = pd.read_csv('./data/madrid/cleaned/sq2_madrid_monthly.csv')
        self.data = pd.read_csv('./data/madrid/cleaned/fotocasa_2023.csv')
    def animate_plot(self, x, y, animation_frame, color, title):
        fig = px.line(self.sq2m, x=x, y=y, animation_frame=animation_frame, color=color, title=title)
        
        st.write(fig)

    def main(self):
        st.title('Graphs Visualizations')
        st.write('This page is dedicated to visualizing data in graphs.')
    
        ## Plotting the distribution of prices
        fig = plt.figure(figsize=(10,5))
        plt.title('Price distribution of houses in Madrid more than 500000€')
        sns.histplot(data=self.data[self.data['Price'] > 500000], x='Price', bins=100, kde=True)
        st.pyplot(fig)
        fig = plt.figure(figsize=(10,5))
        plt.title('Price distribution of houses in Madrid less than 500000€')
        sns.histplot(data=self.data[self.data['Price'] < 500000], x='Price', bins=100, kde=True)
        st.pyplot(fig)


        fig = plt.figure(figsize=(10,5))
        plt.title('This graph shows the distribution of ads date of publication.')
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        sns.histplot(data=self.data, x='Date', bins=100, kde=True)
        st.pyplot(fig)
       

        ## sq2m prices by district
        st.write('This graph shows the evolution of the price per square meter in Madrid by district and month.')
        self.animate_plot(x='month_n', y='price', animation_frame='district', color='año', title = 'Sq2m Prices by district')
        
        
if __name__ == '__main__':
    Visualizations().main()
