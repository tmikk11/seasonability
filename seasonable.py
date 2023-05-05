#!/usr/bin/env python
# coding: utf-8

# In[70]:


# packages
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from datetime import datetime
import math


# In[71]:


# given day x, returns dataframe of all tmin and tmix of 15 day window centered around x in past 30 years
def get_window(x, historical):
    window = historical[(historical['dayyear'] >= x-7) & (historical['dayyear'] <= x+7)                & (historical['year'] > 1991)][['date','tmax','tmin','prcp']]
    # wrapping about for beginning/end of year (leap years get extra day for window)
    if x <= 7:
        window = window.append(historical[(historical['dayyear'] >= 360-x) & (historical['year'] > 1991)][['date','tmax','tmin','prcp']])
    elif x >= 360:
        window = window.append(historical[(historical['dayyear'] <= x-358) & (historical['year'] > 1991)][['date','tmax','tmin','prcp']])

    return window


# In[76]:


def plot(day, high, hist):
    # Getting info we need
    window = get_window(day, hist)

    # Setting up the plot
    fig, ax = plt.subplots(figsize=(4.8, 3.6), dpi=300)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Plotting histogram 
    b = list(range(window.tmax.min(), max(window.tmax.max(), high)+2))
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
    ax.text(alignment, max_ylim*0.85, 'Today\'s High: {:.0f}'.format(high), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.80, 'Percentile: {:.1f}'.format(stats.stats.percentileofscore(window.tmax, high, 'mean')), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.70, 'Average High: {:.1f}'.format(window.tmax.mean()), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.65, 'All Time High: {:.0f}'.format(window.tmax.max()), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.60, 'Lowest High: {:.0f}'.format(window.tmax.min()), ha='right', fontsize=8)

    # Finishing touches
    ax.set_ylabel("Occurrences in Last 30 Years")
    ax.set_xlabel("Daily High (F)")
    window['date'] = pd.to_datetime(window['date'])
    start = window['date'].min()
    end = window['date'].max()
    ax.set_title("Daily Highs for %d/%d to %d/%d" %(start.month,start.day,end.month,end.day))
    plt.savefig('seasonable.png', bbox_inches='tight')


# In[77]:


# using open-meteo.com api for seatac coordinates
forecast = pd.read_json('https://api.open-meteo.com/v1/forecast?latitude=47.4431&longitude=-122.302&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&forecast_days=1&timezone=America%2FLos_Angeles')
day = datetime.strptime(forecast['daily']['time'][0], '%Y-%m-%d').timetuple().tm_yday
# rounded accourding to https://www.nws.noaa.gov/directives/sym/pd01013002curr.pdf
high = math.floor(forecast['daily']['temperature_2m_max'][0] + 0.5)
plot(day, high, pd.read_csv('seatac_cleaned.csv'))


# In[ ]:




