import streamlit as st
import datetime
import numpy as np
import pandas as pd
import requests
#from shapely.geometry import Point, Polygon
#import geopandas as gpd
#import geopy
#from geopy.geocoders import Nominatim
#from geopy.extra.rate_limiter import RateLimiter
#map


df = pd.DataFrame(
     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
     columns=['lat', 'lon'])

st.map(df)


#date and time
d = st.sidebar.date_input(
     "Select Pick Up Date",
     datetime.date(2019, 7, 6))


t = st.sidebar.time_input('Select travel time:', datetime.time(6, 8, 45))

# combine date & time
formatted_pickup_datetime = f"{d} {t}"

# get pickup & dropoff
def get_lonlat(address):
    '''This function uses the nominatim API to convert address into longitude & latitude
    input: address string
    '''
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q':address, \
            'format':'json'}
    response = requests.get(url,
                        params=params).json()[0]

    return  float(response['lat']), float(response['lon'])

pickup = st.sidebar.text_input('Pickup location (street name, number, and city):', 'Mariannenstr. 61, Leipzig')
lat1, lon1 = get_lonlat(pickup)

dropoff = st.sidebar.text_input('Dropoff location (street name, number, and city):', 'Weichselstr. 43, Berlin')
lat2, lon2 = get_lonlat(dropoff)

# get number of passengers
# num_passenger = st.number_input('Select number of passengers')


passengers = st.sidebar.slider('Select number of passengers', 1, 20, 3)

parameters = {
    # FAKE KEY FOR SUBMIT TO KAGGLE
    "key": "2013-07-06 17:18:00.000000119",
    "pickup_datetime": formatted_pickup_datetime,
    "pickup_longitude": lon1,
    "pickup_latitude": lat1,
    "dropoff_longitude": lon2,
    "dropoff_latitude": lat2,
    "passenger_count": passengers
    }

#pickup longitude
#street = st.sidebar.text_input("Street", "75 Bay Street")
#city = st.sidebar.text_input("City", "Toronto")
#province = st.sidebar.text_input("Province", "Ontario")
#country = st.sidebar.text_input("Country", "Canada")

#geolocator = Nominatim(user_agent="GTA Lookup")
#geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
#location = geolocator.geocode(street+", "+city+", "+province+", "+country)

#lat = location.latitude
#lon = location.longitude

map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

st.map(map_data)

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:

- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

response = requests.get(url,
                        params=parameters).json()

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
st.write('Your estimated fare: ', round(response['fare'], 2))
