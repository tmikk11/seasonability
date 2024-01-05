#!/usr/bin/env python
# coding: utf-8

# In[41]:


# this notebook cleans data, adds helpful columns, saves as .csv for past 30 years of data


# In[42]:


# packages
import pandas as pd


# In[43]:


# data is last 30 years of daily highs, mins, and precipitation 
# for Boston (Logan) and Seattle (Sand Point) 
# from https://www.ncdc.noaa.gov/cdo-web

# Loading data (12/31/2023 wan't readt for seattle yet)
seattle = pd.read_csv('seattle_sand_point.csv')
seattle.loc[len(seattle.index)] = ['USW00094290', '2023-12-31', 0.06, 40.0, 51.0]
boston = pd.read_csv('boston_logan.csv')

# Cleaning headers
seattle = seattle[['DATE', 'PRCP', 'TMIN', 'TMAX']]
seattle.rename(columns={"DATE": "date", "PRCP": "prcp", "TMAX": "tmax", "TMIN": "tmin"}, inplace=True)
boston = boston[['DATE', 'PRCP', 'TMIN', 'TMAX']]
boston.rename(columns={"DATE": "date", "PRCP": "prcp", "TMAX": "tmax", "TMIN": "tmin"}, inplace=True)

# Adding date columns
seattle['date'] = pd.to_datetime(seattle['date'])
seattle['year'] = seattle['date'].dt.year
seattle['month'] = seattle['date'].dt.month
seattle['day'] = seattle['date'].dt.day
seattle['dayyear'] = seattle['date'].dt.dayofyear
seattle['season'] = [1 if m in [12,1,2] else 2 if m in [3,4,5] else 3 if m in [6,7,8] else 4 for m in seattle['month']]
boston['date'] = pd.to_datetime(boston['date'])
boston['year'] = boston['date'].dt.year
boston['month'] = boston['date'].dt.month
boston['day'] = boston['date'].dt.day
boston['dayyear'] = boston['date'].dt.dayofyear
boston['season'] = [1 if m in [12,1,2] else 2 if m in [3,4,5] else 3 if m in [6,7,8] else 4 for m in boston['month']]

# missing prcp data is all for days with no rainfall
boston['prcp'].fillna(value=0, inplace=True)
seattle['prcp'].fillna(value=0, inplace=True)

# missing temp values for seattle from https://www.wunderground.com/dashboard/pws/KWASEATT232/
seattle.at[10014,'tmin'] = 61.0
seattle.at[10015,'tmin'] = 57.0
seattle.at[10486,'tmin'] = 36.0
seattle.at[10487,'tmin'] = 37.0
seattle.at[10487,'tmax'] = 53.0
seattle.at[10488,'tmin'] = 43.0
seattle.at[10488,'tmax'] = 50.0
seattle.at[10489,'tmin'] = 38.0
seattle.at[10489,'tmax'] = 50.0
seattle.at[10490,'tmin'] = 40.0
seattle.at[10490,'tmax'] = 57.0

# Saving last 30 years to dataframe
boston.to_csv('boston_logan_cleaned.csv', index=False)
seattle.to_csv('seattle_sand_point_cleaned.csv', index=False)


# In[ ]:




