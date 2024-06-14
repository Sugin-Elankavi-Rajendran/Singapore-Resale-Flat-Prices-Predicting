import streamlit as st
from streamlit_option_menu import option_menu
import json
import requests
import pandas as pd
from geopy.distance import geodesic
import statistics
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV


data = pd.read_csv('mrt.csv')
mrt_location = pd.DataFrame(data)

st.set_page_config(
    page_title="Singapore Resale Flat Prices Prediction",
    page_icon="🏨",
    layout="wide"
)

with st.sidebar:
    selected = option_menu("Main Menu", ["Predictions"],
                           icons=["house", "gear"],
                           styles={"nav-link": {"font": "sans serif", "font-size": "20px", "text-align": "centre"},
                                   "nav-link-selected": {"font": "sans serif", "background-color": "#0072b1"},
                                   "icon": {"font-size": "20px"}
                                   }
                           )

if selected == "Predictions":
    st.markdown("# :blue[Predicting Results based on Trained Models]")
    st.markdown("### :orange[Predicting Resale Price (Regression Task) (Accuracy: 84%)]")

    try:
        with st.form("form1"):

            # -----New Data inputs from the user for predicting the resale price-----
            street_name = st.text_input("Street Name")
            block = st.text_input("Block Number")
            floor_area_sqm = st.number_input('Floor Area (Per Square Meter)', min_value=1.0, max_value=500.0)
            lease_commence_date = st.number_input('Lease Commence Date')
            storey_range = st.text_input("Storey Range (Format: 'Value1' TO 'Value2')")
            
            submit_button = st.form_submit_button(label="PREDICT RESALE PRICE")

            if submit_button is not None:
                with open(r"model.pkl", 'rb') as file:
                    loaded_model = pickle.load(file)
                with open(r'scaler.pkl', 'rb') as f:
                    scaler_loaded = pickle.load(f)
                
                lease_remain_years = 99 - (2024 - lease_commence_date)

                split_list = storey_range.split(' TO ')
                float_list = [float(i) for i in split_list]
                storey_median = statistics.median(float_list)

                address = block + " " + street_name
                query_address = address
                query_string = 'https://www.onemap.gov.sg/api/common/elastic/search?searchVal='+str(query_address)+'&returnGeom=Y&getAddrDetails=Y'
                resp = requests.get(query_string)

                origin = []
                data_geo_location = json.loads(resp.content)
                if data_geo_location['found'] != 0:
                    latitude = data_geo_location['results'][0]['LATITUDE']
                    longitude = data_geo_location['results'][0]['LONGITUDE']
                    origin.append((latitude, longitude))
                
                mrt_lat = mrt_location['latitude']
                mrt_long = mrt_location['longitude']
                list_of_mrt_coordinates = []
                for lat, long in zip(mrt_lat, mrt_long):
                    list_of_mrt_coordinates.append((lat, long))
                
                list_of_dist_mrt = []
                for destination in range(0, len(list_of_mrt_coordinates)):
                    list_of_dist_mrt.append(geodesic(origin, list_of_mrt_coordinates[destination]).meters)
                shortest = (min(list_of_dist_mrt))
                min_dist_mrt = shortest
                list_of_dist_mrt.clear()

                cbd_dist = geodesic(origin, (1.2830, 103.8513)).meters