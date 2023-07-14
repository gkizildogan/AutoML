from yahooquery import Ticker
from datetime import date,timedelta,datetime
import pandas as pd
import numpy as np

input_format = '%Y-%m-%d'
output_format = '%d/%m/%Y'

close_name = 'all_stocks_closed_2003.csv'
adjclose_name = 'all_stocks_adjclosed_2003.csv'
volume_name = 'all_stocks_volume_2003.csv'
name_list = [close_name, adjclose_name, volume_name]

df_close_all = pd.read_csv(close_name)
df_adjclose_all = pd.read_csv(adjclose_name)
df_volume_all = pd.read_csv(volume_name)

df_copy = df_close_all.copy()
df_copy['date'] = pd.to_datetime(df_copy['date'], format='%d/%m/%Y', dayfirst=True)
lastday = df_copy['date'].max().strftime('%Y-%m-%d')
lastdaydate = datetime.strptime(lastday, '%Y-%m-%d').date()
sday = lastdaydate + timedelta(days=1)
eday = datetime.today() + timedelta(days=1)
eday = eday.date()

stocks = df_adjclose_all.columns[1:].tolist()
tickers = Ticker(stocks)
df_hist = tickers.history(start=sday, end=eday, interval='1d')


def history_to_df(df, values):
    df_new = df.reset_index().pivot(index='date',columns='symbol', values=values)

    new_row = df_new.iloc[0].copy()
    for col in new_row.index:
        first_non_null = df_new[col].first_valid_index()
        if pd.notnull(new_row[col]):
            continue
        new_row[col] = df_new.loc[first_non_null, col]
    new_df = pd.DataFrame([new_row], index=[df_new.index[0]])
    new_df = new_df.reset_index(names="date")
    new_df['date'] = new_df['date'].dt.date.astype('object')
    new_df['date'] = new_df['date'].apply(lambda x: x.strftime(output_format) if pd.notnull(x) else '')
    return new_df


df_close = history_to_df(df_hist, values = 'close')
df_adjclose = history_to_df(df_hist, values = 'adjclose')
df_volume = history_to_df(df_hist, values = 'volume')

common_columns_close = list(set(df_close_all.columns) & set(df_close.columns))
common_columns_adjclose = list(set(df_adjclose_all.columns) & set(df_adjclose.columns))
common_columns_volume = list(set(df_volume_all.columns) & set(df_volume.columns))

df_close_all = pd.concat([df_close_all, df_close[common_columns_close]], ignore_index=True)
df_close_all.to_csv(close_name, index=False)

df_adjclose_all = pd.concat([df_adjclose_all, df_adjclose[common_columns_adjclose]], ignore_index=True)
df_adjclose_all.to_csv(adjclose_name, index=False)

df_volume_all = pd.concat([df_volume_all, df_volume[common_columns_volume]], ignore_index=True)
df_volume_all.to_csv(volume_name, index=False)
