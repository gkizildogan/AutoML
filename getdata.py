from yahooquery import Ticker


def datagetter(stocks, asynchro, start, end):
    tickers = Ticker(stocks,asynchronous=asynchro)
    df = tickers.history(start=start, end=end)
    df_close = df.reset_index().pivot(index='date',
                                      columns='symbol', values='close')
    df_adj_close = df.reset_index().pivot(index='date',
                                          columns='symbol', values='adjclose')
    return df_close, df_adj_close