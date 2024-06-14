import pandas as pd
import numpy as np
import warnings
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle

# Suppress warnings
warnings.filterwarnings('ignore')

# Load the dataset
df = pd.read_csv('combined.csv')
print(df.head())  # Print the first few rows for a quick overview

# Display data types
print(df.dtypes)

# Check for missing values
print(df.isnull().sum())

# Function to get the median of storey range
def get_median(x):
    split_list = x.split(' TO ')
    float_list = [float(i) for i in split_list]
    return statistics.median(float_list)

# Apply the get_median function to storey_range column
df['storey_median'] = df['storey_range'].apply(get_median)
print(df.head())

# Select relevant columns
scope_df = df[['cbd_dist', 'min_dist_mrt', 'floor_area_sqm', 'lease_remain_years', 'storey_median', 'resale_price']]
scope_df = scope_df.drop_duplicates()
print(scope_df.head())

# Plot boxplots for each selected column
columns = ['cbd_dist', 'min_dist_mrt', 'floor_area_sqm', 'lease_remain_years', 'storey_median', 'resale_price']
for column in columns:
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=scope_df, x=column)
    plt.title(f'Boxplot of {column}')
    plt.xlabel(column)
    plt.show()

# Log transform selected columns
df1 = scope_df.copy()
df1['floor_area_sqm'] = np.log(df1['floor_area_sqm'])
df1['storey_median'] = np.log(df1['storey_median'])
df1['resale_price'] = np.log(df1['resale_price'])

# Plot boxplots for log-transformed columns
for column in ['floor_area_sqm', 'storey_median', 'resale_price']:
    sns.boxplot(x=column, data=df1)
    plt.title(f'Boxplot of log-transformed {column}')
    plt.show()

# Display data types after transformation
print(df1.dtypes)

# Compute and plot the correlation matrix
corr_matrix = df1.corr()
plt.figure(figsize=(15, 10))
plt.title("Correlation Heatmap")
sns.heatmap(corr_matrix, xticklabels=corr_matrix.columns, yticklabels=corr_matrix.columns, cmap='RdBu', annot=True)
plt.show()

# Define feature matrix and target vector
X = df1[['cbd_dist', 'min_dist_mrt', 'floor_area_sqm', 'lease_remain_years', 'storey_median']]
y = df1['resale_price']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Print the scaled feature matrix
test_dataframe = pd.DataFrame(X_scaled, columns=X.columns)
print(test_dataframe.head())

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=42)

# Initialize and tune the Decision Tree Regressor
dtr = DecisionTreeRegressor()
param_grid = {
    'max_depth': [2, 5, 10, 15, 20, 22],
    'min_samples_split': [2, 3, 4, 5],
    'min_samples_leaf': [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
    'max_features': ['auto', 'sqrt', 'log2']
}
grid_search = GridSearchCV(estimator=dtr, param_grid=param_grid, cv=5)
grid_search.fit(X_train, y_train)
print("Best hyperparameters:", grid_search.best_params_)

# Evaluate the best model
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse}")
print(f"Mean Absolute Error: {mae}")
print(f"Root Mean Squared Error: {rmse}")
print(f"R-squared: {r2}")

# Predict a new sample
new_sample = np.array([[8740, 999, np.log(44), 55, np.log(11)]])
new_sample_scaled = scaler.transform(new_sample)
new_pred = best_model.predict(new_sample_scaled)[0]
print(f"Predicted resale price (log-transformed): {np.exp(new_pred)}")

# Save the model and scaler
with open('model.pkl', 'wb') as file:
    pickle.dump(best_model, file)

with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)
