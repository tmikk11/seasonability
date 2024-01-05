#!/usr/bin/env python
# coding: utf-8

# In[1]:


# packages
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from datetime import datetime
import math


# In[2]:


# given day x, returns dataframe of all tmin and tmix of 15 day window centered around x in past 30 years
def get_window(year, mon, mday, hist):
    # updated to work with leap years
    m_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4) == 0:
        m_days[1] = 29
        
    # getting window of dates
    window = hist[(hist['month'] == mon) & (hist['day'] >= mday-7) & (hist['day'] <= mday+7)]
    start = window['date'].min()
    end = window['date'].max()
    # wrapping for beginning of month
    if mday <= 7:
        if mon == 1:
            pmon = 12
        else:
            pmon = mon-1
        window = pd.concat([window, hist[(hist['month'] == pmon) & (hist['day'] >= m_days[pmon-1]-(7-mday))]])
        start = window[window['month'] == pmon]['date'].min()
    # wrapping for end of month
    elif mday > (m_days[mon-1]-7):
        if mon == 12:
            nmon = 1
        else:
            nmon = mon+1
        window = pd.concat([window, hist[(hist['month'] == nmon) & (hist['day'] <= 7-(m_days[mon-1]-mday))]])
        end = window[window['month'] == mon+1]['date'].max()
    
    return window, datetime.strptime(start, "%Y-%m-%d"), datetime.strptime(end, "%Y-%m-%d")


# In[19]:


def plot(year, mon, mday, high, hist, loc):
    # Getting info we need
    window, start, end = get_window(year, mon, mday, hist)

    # Setting up the plot
    fig, ax = plt.subplots(figsize=(4.8, 3.6), dpi=300)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Plotting histogram    
    b = list(range(int(window.tmax.min()), int(max(window.tmax.max(), high)+2)))
    # Colormap for the matches
    if high > window.tmax.max():
        w = pd.concat([window.tmax, pd.Series(high)])
    else:
        w = window.tmax
    n, bins, patches = ax.hist(w, bins=b, alpha=1, align='left', facecolor='blue', edgecolor='white', linewidth=0.5)
    for i, patch in enumerate(patches):
        if bins[i] == high:
            patch.set_facecolor('red')
        else:
            patch.set_facecolor(plt.cm.viridis(stats.stats.percentileofscore(w, bins[i], 'mean')/100))

    # Fixing plot limites
    min_ylim, max_ylim = plt.ylim()

    # Text stats
    alignment = max(high, window.tmax.max())+1
    ax.text(alignment, max_ylim*0.95, 'Today\'s High: {:.0f}'.format(high), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.90, 'Average High: {:.1f}'.format(window.tmax.mean()), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.85, 'Percentile: {:.1f}'.format(stats.stats.percentileofscore(window.tmax, high, 'mean')), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.75, 'All Time High: {:.0f}'.format(window.tmax.max()), ha='right', fontsize=8)
    ax.text(alignment, max_ylim*0.70, 'Lowest High: {:.0f}'.format(window.tmax.min()), ha='right', fontsize=8)
    
    # Finishing touches
    ax.set_ylabel("Occurrences in Last 30 Years")
    ax.set_xlabel("Daily High (F)")
    window['date'] = pd.to_datetime(window['date'])
    ax.set_title("Daily Highs for %d/%d to %d/%d in %s" %(start.month,start.day,end.month,end.day,loc))
    plt.savefig(loc+'.png', bbox_inches='tight')


# In[28]:


def main():
    paths = ['seattle_sand_point_cleaned.csv', 'boston_logan_cleaned.csv']
    locs = ['Seattle', 'Boston']
    urls = ['https://api.open-meteo.com/v1/forecast?latitude=47.6871&longitude=-122.2566&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&forecast_days=1&timezone=America%2FLos_Angeles', 'https://api.open-meteo.com/v1/forecast?latitude=42.3651&longitude=-71.0178&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&forecast_days=1&timezone=America%2FLos_Angeles']
    for path, loc, url in zip(paths, locs, urls):
        # using open-meteo.com api for seatac coordinates
        forecast = pd.read_json('https://api.open-meteo.com/v1/forecast?latitude=47.4446&longitude=-122.3144&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&forecast_days=1&timezone=America%2FLos_Angeles')
        date = datetime.strptime(forecast['daily']['time'][0], '%Y-%m-%d').timetuple()
        # rounded accourding to https://www.nws.noaa.gov/directives/sym/pd01013002curr.pdf
        high = math.floor(forecast['daily']['temperature_2m_max'][0] + 0.5)
        # making plot
        plot(date.tm_year, date.tm_mon, date.tm_mday, high, pd.read_csv(path), loc)


# In[29]:


if __name__ == '__main__':
    main()


# In[ ]:




