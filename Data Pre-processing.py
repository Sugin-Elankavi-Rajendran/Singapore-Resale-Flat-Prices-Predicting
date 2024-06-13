import glob
import pandas as pd
import json
import requests

df = pd.concat([pd.read_csv(f) for f in glob.glob("./data/*.csv")], ignore_index=True)
#print(df.head())

#print(df.shape)

#print(df.isnull().sum())

df = df.dropna()
print(df.isnull().sum())
