
# coding: utf-8

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json
from pprint import pprint

# Import API key
import BP_api_keys

from BP_api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "BP_cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []
CountryList = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    Country = citipy.nearest_city(lat_lng[0], lat_lng[1]).country_code    
    
    if city not in cities:
        cities.append(city)
        CountryList.append(Country)

# Print the city count to confirm sufficient count
print(f'Length of Cities: \n{len(cities)}')
# print(f'\nCities: \n{cities}')

# Create a dictionary of the cities
cities_dic = {"City": cities, "Country": CountryList}

# Create a data frame of the cities
cities_df = pd.DataFrame(cities_dic)
print(f'\nCities Data Frame:')
cities_df.head()


# ## Perform API Calls

# In[3]:


# OpenWeatherMap API Key
api_key = BP_api_keys.api_key

# Starting URL for Weather Map API Call
url = f'http://api.openweathermap.org/data/2.5/weather?units=IMPERIAL&appid={api_key}'


# In[4]:


RowCount = 0

print(f'\nRetrieve Weather Data:')

# for index, row in cities_df.head().iterrows(): ## print 5 cities only during development
for index, row in cities_df.iterrows(): ## print 5 cities only during development
    
    City = row["City"]
    target_url = f'{url}&q={City}' 
#     print({target_url})

    response = requests.get(target_url)
    response_json = response.json()
    
# pprint(response_json)

    print(f'{"*"*20}')
    print(f'\nRetrieve city #{RowCount + 1}: {cities_df.loc[index]["City"]}')
    print(f'URL: {target_url}')


    RowCount = RowCount + 1
    
    try:
        cities_df.set_value(index, "Date", response_json["dt"])
        cities_df.set_value(index, "Lat", response_json["coord"]["lat"])
        cities_df.set_value(index, "Lng", response_json["coord"]["lon"])
        cities_df.set_value(index, "Max Temperature (F)", response_json["main"]["temp_max"])
        cities_df.set_value(index, "Humidity", response_json["main"]["humidity"])
        cities_df.set_value(index, "Cloudiness", response_json["clouds"]["all"])
        cities_df.set_value(index, "Wind Speed", response_json["wind"]["speed"])
        
    except:
        print("Exception: Missing data point(s)")
  
    # Perform modulus to print out 100 cities before pausing
    if RowCount % 100 == 0:
        print(f'{"*"*20}')
        print(f'\nPause: 30 seconds\n')
        time.sleep(30)

print(f'{"*"*20}')        
print(f'\nRetrieval complete\n')
print(f'{"*"*20}')


# ## Data Cleaning

# In[5]:


cities_df.head(20)


# In[6]:


#Check number of values for each column to see if we lost cities in the search 
print(f'\nColumn Counts:')
cities_df.count()


# In[8]:


#Drop columns with missing variables
cities_df = cities_df.dropna()
cities_df.head()


# In[9]:


#Convert "Date" to DATETIME
cities_df['Date'] = pd.to_datetime(cities_df['Date'], unit='s')
cities_df.head()


# In[10]:


# Save Cities Data frame to an output csv file
cities_df.to_csv("Output/BP_Output_cities_df.csv", index = False)


# ## Chart: Temperature (F) vs. Latitude Scatter Plot

# In[11]:


cities_df.plot.scatter(["Lat"], ["Max Temperature (F)"], marker ='o', alpha = 1, grid = True)

# Chart details
plt.title("Termperature (F) v. City Latitude")
plt.xlabel("City Latitude")
plt.ylabel("Max Temp (F)")

# Save an image of the chart and print to screen
plt.savefig("Output/BP_Output_Temperature_vs_CityLatitude_ScatterPlot.png")
plt.show()


# ## Chart: Humidity (%) vs. Latitude

# In[12]:


cities_df.plot.scatter(["Lat"], ["Humidity"], marker ='o', alpha = 1, grid = True)

# Chart details
plt.title("Humidity v. City Latitude")
plt.xlabel("City Latitude")
plt.ylabel("Humidity")

# Save an image of the chart and print to screen
plt.savefig("Output/BP_Output_Humidity_vs_CityLatitude_ScatterPlot.png")
plt.show()


# ## Chart: Cloudiness (%) vs. Latitude

# In[13]:


cities_df.plot.scatter(["Lat"], ["Cloudiness"], marker ='o', alpha = 1, grid = True)

# Chart details
plt.title("Cloudiness v. City Latitude")
plt.xlabel("City Latitude")
plt.ylabel("Cloudiness")

# Save an image of the chart and print to screen
plt.savefig("Output/BP_Output_Cloudiness_vs_CityLatitude_ScatterPlot.png")
plt.show()


# ## Chart: Wind Speed (mph) vs. Latitude

# In[14]:


cities_df.plot.scatter(["Lat"], ["Wind Speed"], marker ='o', alpha = 1, grid = True)

# Chart details
plt.title("Wind Speed (MPH) v. City Latitude")
plt.xlabel("City Latitude")
plt.ylabel("Wind Speed (MPH)")

# Save an image of the chart and print to screen
plt.savefig("Output/BP_Output_WindSpeedMPH_vs_CityLatitude_ScatterPlot.png")
plt.show()

