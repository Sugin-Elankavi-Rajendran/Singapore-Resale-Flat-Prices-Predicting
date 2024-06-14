Singapore Resale Flat Prices Prediction
=======================================

This project provides tools to predict the resale prices of Singapore flats using a machine learning model. It involves data preprocessing, feature engineering, model training, and deployment through a Streamlit web application.

Table of Contents
-----------------

1.  [Project Description](#project-description)
    
2.  [Data Processing](#data-processing)
    
3.  [Machine Learning Model](#machine-learning-model)
    
4.  [Web Application](#web-application)
    
5.  [Usage](#usage)
    
6.  [Requirements](#requirements)
    
7.  [Model and Data Files](#model-and-data-files)
    
8.  [Acknowledgements](#acknowledgements)
    

Project Description
-------------------

This project aims to predict the resale prices of flats in Singapore based on various features such as floor area, lease remaining, and proximity to MRT stations. The solution is implemented in Python and leverages machine learning techniques for predictive modeling.

Data Processing
---------------

The data processing involves loading multiple CSV files containing information about Singapore flats, cleaning the data by handling missing values, and calculating geographical distances to MRT stations and the Central Business District (CBD).

1.  **Concatenation of CSV Files**: All CSV files in the ./data/ directory are loaded and concatenated into a single DataFrame.
    
2.  **Data Cleaning**: Missing values are dropped, and unique addresses are processed to obtain latitude and longitude using the OneMap API.
    
3.  **MRT Station Proximity Calculation**: Coordinates for all MRT stations are fetched, and distances from each flat to the nearest MRT station are calculated using the geodesic distance.
    
4.  **Saving Processed Data**: The processed data is saved into df\_coordinates.csv for use in modeling.
    

Machine Learning Model
----------------------

A Decision Tree Regressor is used to predict the resale prices based on features like distance to the CBD, distance to MRT stations, floor area, lease remaining, and storey range.

1.  **Data Preparation**: Relevant features are selected and log-transformed to improve model performance.
    
2.  **Model Training**: The dataset is split into training and testing sets. A grid search is performed to find the best hyperparameters for the Decision Tree model.
    
3.  **Model Evaluation**: The model's performance is evaluated using metrics such as Mean Squared Error, Mean Absolute Error, Root Mean Squared Error, and R-squared.
    

Web Application
---------------

A Streamlit web application is created for users to interact with the model:

*   Users can input details of a flat (like block number, street name, floor area, lease commence date, and storey range).
    
*   The application predicts the resale price based on the input values using the trained model.
    
*   The web application is styled with custom CSS for a better user experience.
    

Usage
-----

1.  **Running the Streamlit App**: 
```
streamlit run app.py
```
Ensure you have all dependencies installed.
    
2.  **Input Data**: Input the required flat details in the form provided in the application to get the resale price prediction.
    

Requirements
------------

*   Python 3.x
    
*   pandas
    
*   numpy
    
*   scikit-learn
    
*   streamlit
    
*   seaborn
    
*   matplotlib
    
*   geopy
    
*   requests
    
*   pickle
    

Model and Data Files
--------------------

*   model.pkl: The trained machine learning model.
    
*   scaler.pkl: The scaler used for feature standardization.
    
*   df\_coordinates.csv: The CSV file containing coordinates of the flats and their calculated features.
    

Acknowledgements
----------------

This project was created by Sugin Elankavi Rajendran. Special thanks to the Singapore government for providing the OneMap API, which was instrumental in fetching geographical data.