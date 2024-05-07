import yfinance as yf
import pandas as pd
tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
data = yf.download(tickers.Symbol.to_list(),'2010-1-1','2022-12-31', auto_adjust=True)['Close']
data.to_csv('resources/out.csv',index='False')