import glob
import pandas as pd
import json
import requests
from geopy.distance import geodesic

# Load and concatenate all CSV files in the ./data/ directory
df = pd.concat([pd.read_csv(f) for f in glob.glob("./data/*.csv")], ignore_index=True)
print(df.head())
print(df.shape)

# Check for and drop any missing values
print(df.isnull().sum())
df = df.dropna()
print(df.isnull().sum())

# Display unique town names
print(df['town'].unique())

# List of MRT stations
list_of_mrt = [
    'Jurong East MRT Station', 'Bukit Batok MRT Station', 'Bukit Gombak MRT Station', 
    'Choa Chu Kang MRT Station', 'Yew Tee MRT Station', 'Kranji MRT Station', 
    'Marsiling MRT Station', 'Woodlands MRT Station', 'Admiralty MRT Station', 
    'Sembawang MRT Station', 'Canberra MRT Station', 'Yishun MRT Station', 
    'Khatib MRT Station', 'Yio Chu Kang MRT Station', 'Ang Mo Kio MRT Station', 
    'Bishan MRT Station', 'Braddell MRT Station', 'Toa Payoh MRT Station', 
    'Novena MRT Station', 'Newton MRT Station', 'Orchard MRT Station', 
    'Somerset MRT Station', 'Dhoby Ghaut MRT Station', 'City Hall MRT Station', 
    'Raffles Place MRT Station', 'Marina Bay MRT Station', 'Marina South Pier MRT Station', 
    'Pasir Ris MRT Station', 'Tampines MRT Station', 'Simei MRT Station', 
    'Tanah Merah MRT Station', 'Bedok MRT Station', 'Kembangan MRT Station', 
    'Eunos MRT Station', 'Paya Lebar MRT Station', 'Aljunied MRT Station', 
    'Kallang MRT Station', 'Lavender MRT Station', 'Bugis MRT Station', 
    'Tanjong Pagar MRT Station', 'Outram Park MRT Station', 'Tiong Bahru MRT Station', 
    'Redhill MRT Station', 'Queenstown MRT Station', 'Commonwealth MRT Station', 
    'Buona Vista MRT Station', 'Dover MRT Station', 'Clementi MRT Station', 
    'Chinese Garden MRT Station', 'Lakeside MRT Station', 'Boon Lay MRT Station', 
    'Pioneer MRT Station', 'Joo Koon MRT Station', 'Gul Circle MRT Station', 
    'Tuas Crescent MRT Station', 'Tuas West Road MRT Station', 'Tuas Link MRT Station', 
    'Expo MRT Station', 'Changi Airport MRT Station', 'HarbourFront MRT Station', 
    'Chinatown MRT Station', 'Clarke Quay MRT Station', 'Little India MRT Station', 
    'Farrer Park MRT Station', 'Boon Keng MRT Station', 'Potong Pasir MRT Station', 
    'Woodleigh MRT Station', 'Serangoon MRT Station', 'Kovan MRT Station', 
    'Hougang MRT Station', 'Buangkok MRT Station', 'Sengkang MRT Station', 
    'Punggol MRT Station', 'Bras Basah MRT Station', 'Esplanade MRT Station', 
    'Promenade MRT Station', 'Nicoll Highway MRT Station', 'Stadium MRT Station', 
    'Mountbatten MRT Station', 'Dakota MRT Station', 'MacPherson MRT Station', 
    'Tai Seng MRT Station', 'Bartley MRT Station', 'Lorong Chuan MRT Station', 
    'Marymount MRT Station', 'Caldecott MRT Station', 'Botanic Gardens MRT Station', 
    'Farrer Road MRT Station', 'Holland Village MRT Station', 'one-north MRT Station', 
    'Kent Ridge MRT Station', 'Haw Par Villa MRT Station', 'Pasir Panjang MRT Station', 
    'Labrador Park MRT Station', 'Telok Blangah MRT Station', 'Bayfront MRT Station', 
    'Bukit Panjang MRT Station', 'Cashew MRT Station', 'Hillview MRT Station', 
    'Beauty World MRT Station', 'King Albert Park MRT Station', 'Sixth Avenue MRT Station', 
    'Tan Kah Kee MRT Station', 'Stevens MRT Station', 'Rochor MRT Station', 
    'Downtown MRT Station', 'Telok Ayer MRT Station', 'Fort Canning MRT Station', 
    'Bencoolen MRT Station', 'Jalan Besar MRT Station', 'Bendemeer MRT Station', 
    'Geylang Bahru MRT Station', 'Mattar MRT Station', 'Ubi MRT Station', 
    'Kaki Bukit MRT Station', 'Bedok North MRT Station', 'Bedok Reservoir MRT Station', 
    'Tampines West MRT Station', 'Tampines East MRT Station', 'Upper Changi MRT Station', 
    'Woodlands North MRT Station', 'Woodlands South MRT Station'
]

# Fetch coordinates for each MRT station
mrt_lat = []
mrt_long = []

for mrt in list_of_mrt:
    query_string = f'https://www.onemap.gov.sg/api/common/elastic/search?searchVal={mrt}&returnGeom=Y&getAddrDetails=Y'
    response = requests.get(query_string)
    data_mrt = response.json()

    if data_mrt['found'] != 0:
        mrt_lat.append(data_mrt["results"][0]["LATITUDE"])
        mrt_long.append(data_mrt["results"][0]["LONGITUDE"])
        print(f"{mrt}, Lat: {data_mrt['results'][0]['LATITUDE']} Long: {data_mrt['results'][0]['LONGITUDE']}")
    else:
        mrt_lat.append('NotFound')
        mrt_long.append('NotFound')
        print(f"No Results for {mrt}")

# Create DataFrame for MRT locations
mrt_location = pd.DataFrame({
    'MRT': list_of_mrt,
    'latitude': mrt_lat,
    'longitude': mrt_long
})

# Combine block and street name to form the address
df['address'] = df['block'] + " " + df['street_name']
print(df)

# Fetch unique addresses from the DataFrame
address_list = df['address'].unique()

latitude = []
longitude = []
blk_no = []
road_name = []
postal_code = []
address = []

# Fetch coordinates for each address
for addr in address_list:
    query_string = f'https://www.onemap.gov.sg/api/common/elastic/search?searchVal={addr}&returnGeom=Y&getAddrDetails=Y'
    response = requests.get(query_string)
    data_geo_location = response.json()
    
    if data_geo_location['found'] != 0:
        latitude.append(data_geo_location['results'][0]['LATITUDE'])
        longitude.append(data_geo_location['results'][0]['LONGITUDE'])
        blk_no.append(data_geo_location['results'][0]['BLK_NO'])
        road_name.append(data_geo_location['results'][0]['ROAD_NAME'])
        postal_code.append(data_geo_location['results'][0]['POSTAL'])
        address.append(addr)
        print(f"{addr}, Lat: {data_geo_location['results'][0]['LATITUDE']} Long: {data_geo_location['results'][0]['LONGITUDE']}")
    else:
        print(f"No Results for {addr}")

# Create DataFrame for fetched coordinates
df_coordinates = pd.DataFrame({
    'latitude': latitude,
    'longitude': longitude,
    'blk_no': blk_no,
    'road_name': road_name,
    'postal_code': postal_code,
    'address': address
})
print(len(df_coordinates))

# Compute distances to the nearest MRT station and CBD
list_of_coordinates = list(zip(df_coordinates['latitude'], df_coordinates['longitude']))
list_of_mrt_coordinates = list(zip(mrt_location['latitude'], mrt_location['longitude']))

min_dist_mrt = []
for origin in list_of_coordinates:
    dist_mrt = [geodesic(origin, destination).meters for destination in list_of_mrt_coordinates]
    min_dist_mrt.append(min(dist_mrt))

cbd_dist = [geodesic(origin, (1.2830, 103.8513)).meters for origin in list_of_coordinates]

# Add computed distances to the DataFrame
df_coordinates['cbd_dist'] = cbd_dist
df_coordinates['min_dist_mrt'] = min_dist_mrt
print(df_coordinates)

# Save the coordinates DataFrame to CSV
df_coordinates.to_csv('df_coordinates.csv', index=False)

# Load the saved coordinates DataFrame
df_coordinates = pd.read_csv('df_coordinates.csv')

# Merge the coordinates DataFrame with the original DataFrame
df_new = df_coordinates.merge(df, on="address", how='outer')
print(df_new)

# Data type conversions and adding lease remaining years
df_new['resale_price'] = df_new['resale_price'].astype('float')
df_new['floor_area_sqm'] = df_new['floor_area_sqm'].astype('float')
df_new['lease_commence_date'] = df_new['lease_commence_date'].astype('int64')
df_new['lease_remain_years'] = 99 - (2023 - df_new['lease_commence_date'])

# Drop any remaining missing values
df_new.dropna(inplace=True)
print(df_new)

# Save the final combined DataFrame to CSV
df_new.to_csv('combined.csv', index=False)
