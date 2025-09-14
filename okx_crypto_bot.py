import pandas as pd
import yfinance as yf
import ta
import plotly.graph_objects as go

# Fetch data - Daily and 1-hour timeframes
symbol = 'AAPL'
period = '1mo'

# Daily data
df_daily = yf.download(symbol, period=period, interval='1d')
# 1-hour data
df_hourly = yf.download(symbol, period=period, interval='1h')

# Function to process data: compute indicators, patterns, support/resistance
def process_data(df):
    # Ensure datetime index
    df = df.copy()
    df.reset_index(inplace=True)
    df['timestamp'] = pd.to_datetime(df['Date'])
    
    # Technical Indicators
    df['SMA20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['EMA20'] = ta.trend.ema_indicator(df['Close'], window=20)
    
    # Bollinger Bands
    bb = ta.volatility.BollingerBands(df['Close'], window=20)
    df['bb_hband'] = bb.bollinger_hband()
    df['bb_lband'] = bb.bollinger_lband()
    df['bb_mavg'] = bb.bollinger_mavg()
    
    # RSI
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    
    # MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    
    # Volume Moving Average
    df['Vol_SMA20'] = df['Volume'].rolling(window=20).mean()
    
    # Support & Resistance
    df['support'] = df['Low'].rolling(window=20).min()
    df['resistance'] = df['High'].rolling(window=20).max()
    
    # Candlestick Pattern: Simple Bullish Engulfing
    def bullish_engulfing(data):
        patterns = [False]
        for i in range(1, len(data)):
            prev_open = data['Open'].iloc[i-1]
            prev_close = data['Close'].iloc[i-1]
            curr_open = data['Open'].iloc[i]
            curr_close = data['Close'].iloc[i]
            if prev_close < prev_open and curr_open < curr_close and curr_open < prev_close and curr_close > prev_open:
                patterns.append(True)
            else:
                patterns.append(False)
        return patterns
    df['Bullish_Engulfing'] = bullish_engulfing(df)
    
    # Detect Breakouts
    df['breakout_up'] = df['Close'] > df['resistance']
    df['breakout_down'] = df['Close'] < df['support']
    
    return df

# Process data
def process_data(df):
    # Ensure a copy
    df = df.copy()
    df.reset_index(inplace=True)
    df['timestamp'] = pd.to_datetime(df['Date'])
    
    # Assign Series variables
    close_series = df['Close']
    high_series = df['High']
    low_series = df['Low']
    volume_series = df['Volume']
    
    # Calculate indicators using these Series
    df['SMA20'] = ta.trend.sma_indicator(close_series, window=20)
    df['EMA20'] = ta.trend.ema_indicator(close_series, window=20)

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close_series, window=20)
    df['bb_hband'] = bb.bollinger_hband()
    df['bb_lband'] = bb.bollinger_lband()
    df['bb_mavg'] = bb.bollinger_mavg()

    # RSI
    df['RSI'] = ta.momentum.rsi(close_series, window=14)

    # MACD
    macd = ta.trend.MACD(close_series)
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # Volume moving average
    df['Vol_SMA20'] = volume_series.rolling(window=20).mean()

    # Support & Resistance
    df['support'] = low_series.rolling(window=20).min()
    df['resistance'] = high_series.rolling(window=20).max()

    # Candlestick pattern: Bullish Engulfing
    def bullish_engulfing(data):
        patterns = [False]
        for i in range(1, len(data)):
            prev_open = data['Open'].iloc[i-1]
            prev_close = data['Close'].iloc[i-1]
            curr_open = data['Open'].iloc[i]
            curr_close = data['Close'].iloc[i]
            if prev_close < prev_open and curr_open < curr_close and curr_open < prev_close and curr_close > prev_open:
                patterns.append(True)
            else:
                patterns.append(False)
        return patterns
    df['Bullish_Engulfing'] = bullish_engulfing(df)

    # Breakouts
    df['breakout_up'] = df['Close'] > df['resistance']
    df['breakout_down'] = df['Close'] < df['support']
    
    return df