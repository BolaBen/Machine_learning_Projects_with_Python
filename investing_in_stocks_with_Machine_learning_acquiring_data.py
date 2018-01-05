import pandas as pd
import os
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt

from matplotlib import style
#style.use('dark_background')

import re

import urllib

# path to the folder where we have our data

path = "C:/Investing_in_stocks_with_ML/intraQuarter/intraQuarter"

# defining spec for our stat, path to stat's directory and a one liner loop
# to list the contents in our directory

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+('/_KeyStats')  
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)

    # added a new dataframe, also added % change of stock_Price and sp500
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'DE Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 'Status']) 

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv") # S & P Data

    ticker_list = []

# we first iterate on our directories and list each directory, that is the
# contents in each directory(ticker) and save, now if lenght of each file in
# the directory is greater than zero we would like to proceed for each file in
# each directory that meets this condition, note that some directories has no
# data.

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[1] # added stock ticker name
        ticker_list.append(ticker)  # add every ticker as a list

# defined two variables to calculate % change for stock_price and sp500
# we always want to do this each time the stock price changes

        starting_stock_value = False
        starting_sp500_value = False
        
        if len(each_file) > 0:

# now that we've accessed each directory in our stock list, we would like to
# also pull some info from each file in our directory.

    # Here we would like to pull time and date from the files

            for file in each_file:
                #print(file)

                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time, ticker)

# we pulled the full path to our files, retrieved the source code together with our stats value 
# with this we've been able to Debt/Equity ratios for all of the companies

                full_file_path = each_dir+'/'+file
                #print(full_file_path)
                source = open(full_file_path,'r').read()
                #print(source)
                #value = (source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                #print(ticker+":",value)

# we added functions here to execute our code and do error handling as well
                try:

                    try:
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except:
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    #df = df.append({'Date':date_stamp,'Unix':unix_time,'Ticker':ticker,'DE Ratio':value,}, ignore_index = True)
                    
#added new try-except to make sp500 date and values from S&P 500 data                    
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                    except:
                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                        
# pulled price from source script by splitting and indexing
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                        #print("stock_price:",stock_price,"ticker:", ticker)
                    except:

                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            #print(stock_price)

                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
            
                            stock_price = float(stock_price.group(1))
                            #print(stock_price)

                        except:

                            try:
                                stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                                #print(stock_price)

                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                
                                stock_price = float(stock_price.group(1))
                                #print(stock_price)

                            except:

                                print('wtf stock price lol',ticker,file, value)
                                time.sleep(5)
                                
# setting the start value for stock_price and sp500 to calculate % change (new-old)/old * 100:

                        if not starting_stock_value:
                            starting_stock_value = stock_price
                        if not starting_sp500_value:
                            starting_sp500_value = sp500_value

                        stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                        sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                        location = len(df['Date'])

#Here we account for the difference between the S&P 500 and the stock:
                        
                        difference = stock_p_change - sp500_p_change
                        if difference > 0:
                            status = "outperform"
                        else:
                            status = "underperform"
                            
#updating our dataframe
                        df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change':stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change':sp500_p_change,
                                    'Difference':difference,
                                    'Status':status}, ignore_index = True)
                        
                except Exception as e:
                    pass
                    #print(ticker,e,file, value)


        #print(ticker_list)   
        #print(df)


        for each_ticker in ticker_list:
            try:
                plot_df = df[(df['ticker'] == each_ticker)]
                
                plot_df = plot_df.set_index(['Date'])

                if plot_df['Status'][-1] == 'underperform':
                    color = 'r'
                else:
                    color = 'g'

                plot_df['Difference'].plot(label == each_ticker, color = color)
                plt.legend()

            except Exception as e:
                pass
                #print(str(e)):

        plt.show
        
# we edit our gather variable by replacing space, single quotes and forward slash with nothing so as to customise our file name .csv

        save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
        #print(save)
        #df.to_csv(save)
            
        #time.sleep(10)

Key_Stats()
