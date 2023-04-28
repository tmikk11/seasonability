#!/usr/bin/env python
# coding: utf-8

# In[151]:


# packages
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# reutrns dataframe containing daily highs from last 30 years
def get_history():
    # Loading data
    data = pd.read_csv('seattle_full.csv')

    # Cleadning headers
    cleaned = data[['DATE', 'PRCP', 'TMIN', 'TMAX']].copy()
    cleaned.rename(columns={"DATE": "date", "PRCP": "prcp", "TMAX": "tmax", "TMIN": "tmin"}, inplace=True)

    cleaned['date'] = pd.to_datetime(cleaned['date'])
    cleaned['year'] = cleaned['date'].dt.year
    cleaned['month'] = cleaned['date'].dt.month
    cleaned['day'] = cleaned['date'].dt.day
    cleaned['dayyear'] = cleaned['date'].dt.dayofyear
    cleaned['season'] = [1 if m in [12,1,2] else 2 if m in [3,4,5] else 3 if m in [6,7,8] else 4 for m in cleaned['month']]

    #Filling missing prcp values
    cleaned.at[10944,'prcp'] = 0.13
    cleaned.at[10956,'prcp'] = 0.11
    cleaned['prcp'].fillna(value=0, inplace=True)

    # Saving to dataframe
    history = cleaned[cleaned['year'] > 1992]
    return history


# given day x, returns dataframe of all tmin and tmix of 15 day window centered around x in past 30 years
def get_window(x, historical):
    window = historical[(historical['dayyear'] >= x-7) & (historical['dayyear'] <= x+7)                & (historical['year'] > 1991)][['date','tmax','tmin','prcp']]
    # wrapping about for beginning/end of year (leap years get extra day for window)
    if x <= 7:
        window = window.append(historical[(historical['dayyear'] >= 360-x) & (historical['year'] > 1991)][['Date','tmax','tmin','prcp']])
    elif x >= 360:
        window = window.append(historical[(historical['dayyear'] <= x-358) & (historical['year'] > 1991)][['Date','tmax','tmin','prcp']])

    return window


# make our histogram
def plot(day, high, hist):
    # Getting info we need
    window = get_window(day, hist)

    # Setting up the plot
    fig, ax = plt.subplots(figsize=(4.8, 3.6), dpi=300)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Plotting histogram 
    b = np.arange(window.tmax.min(), max(window.tmax.max(), high)+2, 1)
    # Colormap for the matches
    if high > window.tmax.max():
        w = window.tmax.append(pd.Series(high))
    else:
        w = window.tmax
    n, bins, patches = ax.hist(w, bins=b, alpha=1, align='left', facecolor='blue', edgecolor='white', linewidth=0.5)
    for i, patch in enumerate(patches):
        if bins[i] == high:
            patch.set_facecolor('red')
        else:
            patch.set_facecolor(plt.cm.viridis(stats.stats.percentileofscore(window.tmax, bins[i], 'mean')/100))

    # Fixing plot limites
    min_ylim, max_ylim = plt.ylim()

    # Text stats
    alignment = max(high, window.tmax.max())+1
    ax.text(alignment, max_ylim*0.85, 'Today\'s High: {:.0f}'.format(high), ha='right', fontsize=10)
    ax.text(alignment, max_ylim*0.75, 'Percentile: {:.1f}'.format(stats.stats.percentileofscore(window.tmax, high, 'mean')), ha='right', fontsize=10)
    ax.text(alignment, max_ylim*0.55, 'All Time High: {:.0f}'.format(window.tmax.max()), ha='right', fontsize=10)
    ax.text(alignment, max_ylim*0.45, 'Lowest High: {:.0f}'.format(window.tmax.min()), ha='right', fontsize=10)

    # Finishing touches
    ax.set_ylabel("Occurrences in Last 30 Years")
    ax.set_xlabel("Daily High (F)")
    start = window['date'].min()
    end = window['date'].max()
    ax.set_title("Daily Highs for %d/%d to %d/%d (This was automated)" %(start.month,start.day,end.month,end.day))
    plt.savefig('test.png')


# using open-meteo.com api for seatac coordinates
day = datetime.today().timetuple().tm_yday
forecast = pd.read_json('https://api.open-meteo.com/v1/forecast?latitude=47.4431&longitude=-122.302&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&forecast_days=1&timezone=America%2FLos_Angeles')
high = int(forecast['daily']['temperature_2m_max'][0])
plot(day, high, get_history())

