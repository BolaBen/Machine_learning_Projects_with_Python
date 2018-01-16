##Automating getting the S&P 500 list - Python Programming for Finance

import bs4 as bs    # HTML parsing library
import pickle       # module to save list of companies
import requests     #  to grab the source code from Wikipedia's page.
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

# we added some few new imports
##we used datetime to specify dates for the Pandas datareader, os is to
##check for, and create, directories

import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web


##we divine a function to save our sp500 tickers(info), fetched source code from wiki and called beautiful soup function on the .text part
##of the source code turn it to a python object, called find function on soup to extract table from it

def save_sp500_tickers():
##    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}
##    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies', headers=headers)

    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    
##For each row, after the header row (this is why we're going through with [1:]),
##we're saying the ticker is the "table data" (td), we grab the .text of it, and we append this ticker to our list.

    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    #print(tickers)

##using the pickle module for this, which serializes Python objects for us.

    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    print(tickers)
    return tickers

##save_sp500_tickers()

##we decide here in the code below whether to reload(update) our sp_500 list
##or not each time we run our code or not

def get_data_from_google(reload_sp500=False):
    
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle","rb") as f:
            tickers = pickle.load(f)

#in case path does not exists we want to create one
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

# pulling data from our directory
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2016, 12, 31)
    
    for ticker in tickers:
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'google', start, end)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_data_from_google()
