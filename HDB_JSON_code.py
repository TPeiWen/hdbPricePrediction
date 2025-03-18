# import pandas as pd
# import json

# # Load dataset
# df = pd.read_csv("hdb_resale_flat_transactions_2020-2025.csv")

# # Compute the average resale price per town
# if 'town' in df.columns and 'resale_price' in df.columns:
#     df['town_avg_price'] = df.groupby('town')['resale_price'].transform('mean')
# else:
#     raise ValueError("Missing 'town' or 'resale_price' column in dataset.")

# # Compute price per square foot
# if 'resale_price' in df.columns and 'floor_area_sqm' in df.columns:
#     df['price_per_sqft'] = df['resale_price'] / (df['floor_area_sqm'] * 10.764)  # Convert sqm to sqft
# else:
#     raise ValueError("Missing 'resale_price' or 'floor_area_sqm' column.")

# # Select required columns
# selected_columns = ['town', 'town_avg_price', 'price_per_sqft', 'latitude', 'longitude']

# # Check if all required columns exist
# missing_cols = [col for col in selected_columns if col not in df.columns]
# if missing_cols:
#     raise ValueError(f"Missing required columns: {missing_cols}")

# # Group by town and store unique values
# town_data = df[selected_columns].groupby('town').agg({
#     'town_avg_price': 'mean',  # Average resale price for town
#     'price_per_sqft': 'mean',  # Average price per sqft for town
#     'latitude': 'first',  # Use the first occurrence (assumes town-level consistency)
#     'longitude': 'first'
# }).to_dict(orient='index')

# # Save to JSON
# json_filename = "preprocessed_data.json"
# with open(json_filename, "w") as json_file:
#     json.dump(town_data, json_file, indent=4)

# print(f"✅ Preprocessed data saved to {json_filename}")

import pandas as pd
import json

# Load dataset
df = pd.read_csv("hdb_resale_flat_transactions_2020-2025.csv")

# Check if required columns exist
required_columns = ['town', 'resale_price', 'floor_area_sqm', 'price_per_sqft', 'latitude', 'longitude', 'flat_type']
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Compute the average resale price per town and flat_type
df['town_avg_price'] = df.groupby(['town', 'flat_type'])['resale_price'].transform('mean')

# Select required columns
selected_columns = ['town', 'flat_type', 'town_avg_price', 'price_per_sqft', 'latitude', 'longitude']

# Check if all required columns exist
missing_cols = [col for col in selected_columns if col not in df.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Group by town and flat_type and calculate the mean values
df_town = df[selected_columns].groupby(['town', 'flat_type']).agg({
    'town_avg_price': 'mean',  # Average resale price for each town and flat type
    'price_per_sqft': 'mean',  # Average price per sqft for each town and flat type
    'latitude': 'first',  # Use the first occurrence (assumes town-level consistency)
    'longitude': 'first'
}).reset_index()  # Reset index to keep 'town' and 'flat_type' as columns

# Save to JSON
json_filename = "preprocessed_data_updated.json"
df_town.to_json(json_filename, orient="records", indent=4)  # Save as list of dictionaries

print(f"✅ Preprocessed data saved to {json_filename}")
