# Strategy maded by Jordanmatutel
# https://github.com/Jordanmatutel
# https://medium.com/@donjordanje
# This algorithm its not 100% effective, the creator is not responsible for any case
# in which money is lost. Use it at your own risk.
# This code contains the backtest of the strategy. 
# If you want to see the backtest results, run the code! And good luck.

import pandas as pd
import numpy as np
import talib
import yfinance as yf
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Backtest info
today = date.today()
start_day = today - timedelta(days=6)
market = "BTC-USD"
dataframe = "1m"
# Download the backtest data
data = yf.download(market, start=start_day, end=today, interval=dataframe)
dates = data.index.strftime("%Y-%m-%d").tolist()

# Inputs
close = data["Close"]
lenght = 9
wma_list = talib.WMA(close, timeperiod=lenght) # Calculate the WMA

# Resize
close = close[lenght:]
wma_list = wma_list[lenght:]
dates = dates[lenght:]

# Backtest execution
investment = 1000
position = False
last_position = 0
gains = []

# Replicates the historical data. 
for i in range(len(close)):
    # Buy
    if close[i] > wma_list[i] and not position:
        last_position =  investment / close[i]
        position = True
        gains.append(0)

    # Exit buy
    elif close[i] < wma_list[i] and position:
        c = (close[i] * last_position) - investment
        position = False
        gains.append(c)
    # Add 0 to gain list variable even if there's not movement.
    else:
        gains.append(0)


# Saves the data
gains = np.cumsum(gains)
gains = np.round(gains, 2)
drawdown = min(gains)

# Saves the obtained info.
r = f"This strategy is based on the WMA indicator. It opens a position everytime "\
    f"that the close > WMA and sell it everytime close < WMA. the lenght of periods" \
    f"Used in this strategy was {lenght} using the data of {market} in {dataframe} dataframe. " \
    f"The backtest info was from yfinances and was applied in the interval of {start_day} from {today}. " \
    f"The total profit was: {gains[-1]} with a maximun drawdown of {drawdown}."

with open("readme.txt", "w") as f:
        f.write(str(r))

# Saves the csv
c = pd.DataFrame({"Close":close, "wma":wma_list, "Profit":gains})
c.to_csv("results_backtest.csv", index=False)

# Graph
dates = mdates.datestr2num(dates)
fig, ax = plt.subplots()
ax.plot(dates, gains)
date_format = mdates.DateFormatter('%m')
ax.xaxis.set_major_formatter(date_format)
ax.set_xlabel('Month')
ax.set_ylabel('Earnings')
ax.set_title(f"Initial investment: {investment}, gains: {round(gains[-1],2)}")
plt.show()