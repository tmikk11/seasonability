#!/usr/bin/env python
# coding: utf-8

# In[30]:


# packages
import pandas as pd


# In[31]:


# seatac_noaa.csv is data from https://www.ncdc.noaa.gov/cdo-web/
# this notebook cleans data, saves as seatac_cleaned.csv for past 30 years of data

# Loading data
data = pd.read_csv('seatac_noaa.csv')

# Cleaning headers
data = data[['DATE', 'PRCP', 'TMIN', 'TMAX']]
data.rename(columns={"DATE": "date", "PRCP": "prcp", "TMAX": "tmax", "TMIN": "tmin"}, inplace=True)

# Adding date columns
data['date'] = pd.to_datetime(data['date'])
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data['day'] = data['date'].dt.day
data['dayyear'] = data['date'].dt.dayofyear
data['season'] = [1 if m in [12,1,2] else 2 if m in [3,4,5] else 3 if m in [6,7,8] else 4 for m in data['month']]

# Filling missing prcp values
data.at[10944,'prcp'] = 0.13
data.at[10956,'prcp'] = 0.11
data['prcp'].fillna(value=0, inplace=True)

# Saving last 30 years to dataframe
data = data[data['year'] > 1992]
data.to_csv('seatac_cleaned.csv', index=False)


# In[ ]:




