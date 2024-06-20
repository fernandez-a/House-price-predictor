# House Price Prediction Application

This application allows users to explore different visualizations and predictions related to house prices in Madrid, Spain. The data used in this application has been collected from various sources including Fotocasa, Airbnb, Comunidad de Madrid, and OpenStreetMap.

## Structure

The application is structured into several Python scripts and Jupyter notebooks, organized in the following directories:

- `pages/`: Contains the Streamlit pages for the application, including maps, graphs, and predictions.
- `models/`: Contains the trained machine learning model for house price prediction.
- `notebooks/`: Contains Jupyter notebooks for data preparation and exploration.
- `scrapers/`: Contains scripts for scraping data from various sources.
- `utils/`: Contains utility scripts for tasks such as finding Airbnb listings and clustering.

## Main Features

- **Maps Visualizations**: This page displays various map-based visualizations.
- **Graphs Visualizations**: This page displays various graph-based visualizations of the data.
- **Predictions**: This page allows users to input information about a property and get a price prediction.

## Usage

To run the application, execute the `main.py` script:

```bash
python main.py
```
This will start the Streamlit server and open the application in your web browser.

## Dependencies

The application depends on several Python libraries, including Streamlit, pandas, folium, and scikit-learn. All dependencies can be installed using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```
## Data
The data used in this application is stored in the data/ directory. It includes housing data from Fotocasa, Airbnb listings, and geographic data from OpenStreetMap and Comunidad de Madrid.

Data available upon request

## Notebooks
The notebooks/ directory contains Jupyter notebooks that were used for data preparation and exploration. They can be viewed for a more in-depth look at the data and the steps taken to clean and process it for use in the application.

The tutor for this application was @carlosmanza the mark obtain was 9.52 out of 10