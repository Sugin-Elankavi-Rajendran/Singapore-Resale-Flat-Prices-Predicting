import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV


df = pd.read_csv('combined.csv')
print(df)

print(df.dtypes)

print(df.isnull().sum())

