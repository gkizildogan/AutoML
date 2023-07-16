import yfinance as yf


def datagetter(stocks,interval):
    """
    :param stocks: Stock names as a list of strings
    :param interval: Yfinance intervals
    :return: Adjclose, Close, High, Low, Open, Volume Dataframes
    """
    history_df = yf.download(tickers=stocks,interval=interval, group_by='ticker')
    # special case --> Stock = 1 kontrol
    transposed_history = history_df.stack(level=1).rename_axis(['Datetime', 'Ticker']).reset_index(level=1)
    adj_close_df = transposed_history[transposed_history['Ticker'] == 'Adj Close'].drop('Ticker', axis=1)
    close_df = transposed_history[transposed_history['Ticker'] == 'Close'].drop('Ticker', axis=1)
    high_df = transposed_history[transposed_history['Ticker'] == 'High'].drop('Ticker', axis=1)
    low_df = transposed_history[transposed_history['Ticker'] == 'Low'].drop('Ticker', axis=1)
    open_df = transposed_history[transposed_history['Ticker'] == 'Open'].drop('Ticker', axis=1)
    volume_df = transposed_history[transposed_history['Ticker'] == 'Volume'].drop('Ticker', axis=1)
    return adj_close_df, close_df, low_df, high_df, open_df, volume_df
