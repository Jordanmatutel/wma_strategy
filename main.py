# Strategy maded by Jordanmatutel
# https://github.com/Jordanmatutel
# https://medium.com/@donjordanje
# This algorithm its not 100% effective, the creator is not responsible for any case
# in which money is lost. Use it at your own risk.
# This code contains the application model, you just have to add your broker API.

import ccxt
import talib
import time

# Connect the broker
public_api = "XXXX"
secret_api = "XXXX"
exchange = ccxt.binance({
    "apiKey": public_api,
    "secret": secret_api,
})

# Inputs
symbol = "BTC/USDT"
timeframe = "1m"
invest = 1000

# Strategy variables
position = False
wma_lenght = 9


# Loop. This keep the strategy running
while True:
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=11) 
    close = [x[4] for x in ohlcv] # Takes the list of close
    close = np.array(close)
    wma_list = talib.WMA(close, wma_lenght) # Calculate the wma
    # How much will be bought.
    ticker = exchange.fetch_ticker(symbol) 
    amount = invest / ticker["ask"]

    # Buy
    if close[-1] > wma_list[-1] and not position: 
        order = exchange.create_order(symbol, "limit", "buy", amount, ticker["ask"])
        position = True
    # Sell
    if close[-1] < wma_list[-1] and position:
        order = exchange.create_order(symbol, "limit", "sell", amount, ticker["bid"])
        position = False

    # Iteration every 60 seconds
    time.sleep(60)
