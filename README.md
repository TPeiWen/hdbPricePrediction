# hdbPricePrediction

# HDB Resale Price Prediction

This project provides a prediction model for estimating the resale price of HDB flats in Singapore based on various features such as flat type, storey range, and distances to amenities like MRT stations, CBD, and primary schools. The model is built using a trained Random Forest model and leverages preprocessed data for accurate predictions.

## Files in the Repository

- `app.py`: A Streamlit frontend application for users to input features and get resale price predictions.
- `HDB_JSON_code.py`: Python code to generate the preprocessed JSON file containing necessary features for the model.
- `preprocessed_data_updated.json`: The preprocessed dataset that is used to extract features for model predictions.
- `random_forest_best.pkl`: The trained Random Forest model saved in pickle format for making predictions.
- `hdb_resale_flat_transactions_2020-2025.csv`: Raw dataset used for training the model, containing HDB resale transaction data.

## Project Description

This project involves building a web-based application using **Streamlit** that allows users to input specific characteristics of an HDB flat to predict its resale price using a trained **Random Forest** model. The model predicts the resale price based on factors such as:

- Flat type (e.g., 1-Room, 2-Room, 3-Room, etc.)
- Storey range (e.g., 01-03, 04-06, etc.)
- Floor area in square meters
- Remaining lease in years
- Distance to nearest MRT station
- Distance to CBD (Central Business District)
- Distance to nearest primary school

The backend model is trained using a dataset of HDB resale flat transactions from 2020-2025, and the predictions are generated via a Random Forest algorithm.

## Setup Instructions

### Prerequisites

Make sure you have the following dependencies installed:

- Python 3.7 or later
- Streamlit
- scikit-learn
- pandas
- numpy
- pickle
- json

### Installing Dependencies

You can install the required dependencies by running:

```bash
pip install -r requirements.txt
