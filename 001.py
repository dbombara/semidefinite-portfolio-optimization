import yfinance as yf
import pandas as pd
tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
data = yf.download(tickers.Symbol.to_list(),'2023-1-1','2023-12-31', auto_adjust=True)['Close']
data.to_csv('resources/out2023.csv',index='False')