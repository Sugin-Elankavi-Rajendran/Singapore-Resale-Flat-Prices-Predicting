import streamlit as st
from streamlit_option_menu import option_menu
import json
import requests
import pandas as pd
from geopy.distance import geodesic
import statistics
import numpy as np
import pickle

# Load data
data = pd.read_csv('mrt.csv')
mrt_location = pd.DataFrame(data)

# Streamlit page configuration
st.set_page_config(
    page_title="Singapore Resale Flat Prices Prediction",
    page_icon="🏨",
    layout="wide"
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Predictions"],
        icons=["house", "gear"],
        styles={
            "nav-link": {
                "font": "sans serif",
                "font-size": "20px",
                "text-align": "centre"
            },
            "nav-link-selected": {
                "font": "sans serif",
                "background-color": "#0072b1"
            },
            "icon": {
                "font-size": "20px"
            }
        }
    )

# Prediction page
if selected == "Predictions":
    st.markdown("# :blue[Predicting Results based on Trained Models]")
    st.markdown("### :orange[Predicting Resale Price (Regression Task) (Accuracy: 84%)]")

    try:
        with st.form("form1"):
            street_name = st.text_input("Street Name")
            block = st.text_input("Block Number")
            floor_area_sqm = st.number_input('Floor Area (Per Square Meter)', min_value=1.0, max_value=500.0)
            lease_commence_date = st.number_input('Lease Commence Date')
            storey_range = st.text_input("Storey Range (Format: 'Value1' TO 'Value2')")
            
            submit_button = st.form_submit_button(label="PREDICT RESALE PRICE")

            if submit_button:
                with open("model.pkl", 'rb') as file:
                    loaded_model = pickle.load(file)
                with open('scaler.pkl', 'rb') as f:
                    scaler_loaded = pickle.load(f)
                
                lease_remain_years = 99 - (2024 - lease_commence_date)

                storey_values = [float(value) for value in storey_range.split(' TO ')]
                storey_median = statistics.median(storey_values)

                address = f"{block} {street_name}"
                query_string = f'https://www.onemap.gov.sg/api/common/elastic/search?searchVal={address}&returnGeom=Y&getAddrDetails=Y'
                response = requests.get(query_string)

                origin = []
                data_geo_location = json.loads(response.content)
                if data_geo_location['found']:
                    latitude = data_geo_location['results'][0]['LATITUDE']
                    longitude = data_geo_location['results'][0]['LONGITUDE']
                    origin.append((latitude, longitude))
                
                mrt_coordinates = list(zip(mrt_location['latitude'], mrt_location['longitude']))
                
                distances_to_mrt = [geodesic(origin, dest).meters for dest in mrt_coordinates]
                min_dist_mrt = min(distances_to_mrt)

                cbd_dist = geodesic(origin, (1.2830, 103.8513)).meters

                new_sample = np.array([
                    [cbd_dist, min_dist_mrt, np.log(floor_area_sqm), lease_remain_years, np.log(storey_median)]
                ])
                new_sample_scaled = scaler_loaded.transform(new_sample)
                predicted_price = loaded_model.predict(new_sample_scaled)[0]

                st.write('## :green[Predicted resale price:] ', np.exp(predicted_price))
    
    except Exception as e:
        st.write("Enter the above values to get the predicted resale price of the flat.")
