import streamlit as st
import pickle
import numpy as np
import pandas as pd
import json

# Load the trained Random Forest model
with open("random_forest_best.pkl", "rb") as file:
    model = pickle.load(file)

# Check the expected number of features
n_features = model.n_features_in_
st.write(f"Model expects {n_features} features.")

# Load preprocessed data (latitude, longitude, town_avg_price, price_per_sqft)
with open("preprocessed_data_updated.json", "r") as file:
    preprocessed_data = json.load(file)

df_preprocessed = pd.DataFrame(preprocessed_data)

# Get unique towns from preprocessed data (for display purposes)
towns = df_preprocessed["town"].unique().tolist()

# Flat type, storey range, etc.
flat_types = ["2-Room", "3-Room", "4-Room", "5-Room", "Executive"]
storey_ranges = ["01-03", "04-06", "07-09", "10-12", "13-15", "16-18", "19-21", "22-24", "25-27", "28-30", 
                 "31-33", "34-36", "37-39", "40-42", "43-45", "46-48", "49-51"]

# Streamlit UI
st.title("HDB Resale Price Prediction")
st.write("Enter the details below to predict the resale price of an HDB flat.")

# User inputs
selected_town = st.selectbox("Select Town", towns)
flat_type = st.selectbox("Select Flat Type", flat_types)
storey_range = st.selectbox("Select Storey Range", storey_ranges)
floor_area_sqm = st.number_input("Floor Area (sqm)", value=10.0, min_value=10.0, max_value=200.0, step=0.5)
remaining_lease_years = st.number_input("Remaining Lease (years)", value=70, min_value=1, max_value=99, step=1)
mrt_distance = st.number_input("Distance to Nearest MRT (km)", min_value=0.0, max_value=10.0, step=0.1)
cbd_distance = st.number_input("Distance to CBD (km)", min_value=0.0, max_value=30.0, step=0.1)
pri_distance = st.number_input("Distance to Nearest Primary School (km)", min_value=0.0, max_value=10.0, step=0.1)

# Mapping user input flat type to match dataset values
flat_type_mapping = {
    "2-Room": "2 ROOM", "3-Room": "3 ROOM",
    "4-Room": "4 ROOM", "5-Room": "5 ROOM", "Executive": "EXECUTIVE"
}
flat_type_encoded = flat_type_mapping[flat_type]

# Fetch town and flat type specific data
town_data = df_preprocessed[df_preprocessed["town"] == selected_town]

# Ensure flat type exists in town_data
flat_type_data = town_data[town_data["flat_type"].str.strip().str.upper() == flat_type_encoded]

# Handle missing flat type data
if not flat_type_data.empty:
    price_per_sqft = flat_type_data["price_per_sqft"].iloc[0]  
else:
    st.warning(f"No data found for {flat_type} in {selected_town}. Using town average price per sqft.")
    price_per_sqft = town_data["price_per_sqft"].mean() 

latitude = town_data["latitude"].mean()
longitude = town_data["longitude"].mean()
town_avg_price = town_data["town_avg_price"].mean()

# Display retrieved data
# st.write(f"Retrieved Data for {selected_town} ({flat_type}):")
# st.write(f"- Latitude: {latitude}")
# st.write(f"- Longitude: {longitude}")
# st.write(f"- Town Average Price: {town_avg_price}")
# st.write(f"- Price per Sqft: {price_per_sqft}")

# Feature engineering
floor_area_squared = floor_area_sqm ** 2
log_price_per_sqft = np.log(price_per_sqft + 1)

# Compute area_per_year
flat_age = 99 - remaining_lease_years
area_per_year = floor_area_sqm / (flat_age + 1)  # Avoid division by zero

# Storey range mapping
storey_map = {
    '01-03': 2, '04-06': 5, '07-09': 8, '10-12': 11,
    '13-15': 14, '16-18': 17, '19-21': 20, '22-24': 23,
    '25-27': 26, '28-30': 29, '31-33': 32, '34-36': 35,
    '37-39': 38, '40-42': 41, '43-45': 44, '46-48': 47,
    '49-51': 50
}
storey_mid = storey_map[storey_range]

# Create feature vector (no town encoding needed, use latitude and longitude)
input_features = np.array([[ 
    remaining_lease_years, floor_area_sqm, price_per_sqft, 
    mrt_distance * 1000, cbd_distance * 1000, pri_distance * 1000,
    latitude, longitude, storey_mid, area_per_year, town_avg_price, 
    floor_area_squared,log_price_per_sqft
]])

# Ensure the model receives the correct number of features
if input_features.shape[1] != n_features:
    st.error(f"Mismatch in column count. Expected {n_features} columns, but got {input_features.shape[1]} columns.")
else:
    if st.button("Predict"):
        prediction = model.predict(input_features)[0]
        
        # Adjust prediction if below town average price
        # if prediction < town_avg_price:
        #     prediction = (prediction + town_avg_price) / 2  # Move closer to town average
        
        st.success(f"Predicted Resale Price: SGD {prediction:,.2f}")

    # Show features passed to the model
    st.write("Features being passed to the model:")
    feature_names = [
        "remaining_lease_years", "floor_area_sqm", "price_per_sqft", 
        "distance_to_mrt_meters", "distance_to_cbd", "distance_to_pri_school_meters", 
        "latitude", "longitude", "storey_mid", "area_per_year", "town_avg_price", 
        "floor_area_squared","log_price_per_sqft"
    ]
    
    st.write(pd.DataFrame(input_features, columns=feature_names))

