#############################
import yfinance as yf
from datetime import date,timedelta,datetime
import pandas as pd
import numpy as np

with open('stocks.txt') as f:
    stocks = f.read().splitlines()

stocksa = " ".join(stocks)

history_df = yf.download(stocksa,period='7d', interval='1m', group_by='ticker')
transposed_history = history_df.stack(level=1).rename_axis(['Datetime', 'Ticker']).reset_index(level=1)
adj_close_df = transposed_history[transposed_history['Ticker'] == 'Adj Close'].drop('Ticker', axis=1)
volume_df = transposed_history[transposed_history['Ticker'] == 'Volume'].drop('Ticker', axis=1)

sel_stocks = ["ALBRK.IS","GARAN.IS","HALKB.IS","ISCTR.IS"]
bankalar = " ".join(sel_stocks)
history_df = yf.download(bankalar,period='7d', interval='1m', group_by='ticker')
transposed_history = history_df.stack(level=1).rename_axis(['Datetime', 'Ticker']).reset_index(level=1)
adj_close_df = transposed_history[transposed_history['Ticker'] == 'Adj Close'].drop('Ticker', axis=1)
volume_df = transposed_history[transposed_history['Ticker'] == 'Volume'].drop('Ticker', axis=1)
sel_df = adj_close_df[sel_stocks]


def calculate_cross_correlation(df):
    columns = df.columns
    num_columns = len(columns)

    # Initialize a DataFrame to store the results
    result_df = pd.DataFrame(columns=['Column 1', 'Column 2', 'Max Correlation', 'Lag'])

    # Calculate cross-correlation between all column pairs
    for i in range(num_columns):
        for j in range(i+1, num_columns):
            column1 = columns[i]
            column2 = columns[j]

            max_corr = 0.0
            lag = None

            # Iterate over different lag values
            for l in range(15):
                # Drop the first l rows from both columns
                dropped_df = df[l:].reset_index(drop=True)
                dropped_column2 = dropped_df[column2]

                # Calculate cross-correlation using pandas corr function
                cross_corr = dropped_df[column1].corr(dropped_column2)

                # Update the maximum correlation and lag if necessary
                if abs(cross_corr) > abs(max_corr):
                    max_corr = cross_corr
                    lag = l

            # Append the result to the DataFrame
            result_df = result_df.append({'Column 1': column1, 'Column 2': column2,
                                          'Max Correlation': max_corr, 'Lag': lag}, ignore_index=True)

    return result_df

# Assuming your DataFrame is called "df" with numeric columns

# Call the function to calculate cross-correlation
cross_corr_df = calculate_cross_correlation(sel_df)

