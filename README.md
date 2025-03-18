# HDB Resale Price Prediction

This project predicts the resale price of HDB flats based on various features such as town, flat type, storey range, floor area, remaining lease, and proximity to amenities like MRT stations and schools.

## Files in this Repository

- **app.py**: The frontend code using Streamlit for building the user interface for HDB resale price prediction.
- **HDB_JSON_code.py**: The code to generate the preprocessed JSON file from the raw dataset.
- **preprocessed_data_updated.json**: The preprocessed data used for model prediction.
- **random_forest_best.pkl**: The trained Random Forest model for predicting HDB resale prices.

## Dataset and Trained Models

The dataset `hdb_resale_flat_transactions_2020-2025.csv` and the 3 trained models are too large to upload directly to GitHub. You can download them from the following link:

[Download Dataset and Trained Models](https://tinyurl.com/2p9stcy9)

After downloading, please place the files in the appropriate directories:

- `hdb_resale_flat_transactions_2020-2025.csv` should be used for training the models (if needed).
- `random_forest_best.pkl` should be placed in the working directory for prediction.

## How to Run the Application

1. Install the required libraries:
   ```bash
   pip install -r requirements.txt

2. Run the Streamlit app using the following command:
   ```bash
   python -m streamlit run app.py
