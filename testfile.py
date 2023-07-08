from datetime import date,timedelta,datetime
import pandas as pd
import getdailydata
import datafiller
import numpy as np

df = pd.read_csv('all_stocks_test.csv')
df.to_csv('yarak.csv',index=False)

closed, adjclosed = getdata.datagetter(allstocks,startday=yday,endday=tday, interval='1d')

filled_closed = datafiller.filler(closed, 'linear')
filled_adjclosed = datafiller.filler(adjclosed, 'linear')

lastday = df.date.max()
date_object = datetime.strptime(lastday, '%Y-%m-%d').date()
tday = date_object + timedelta(days=2)
yday = tday - timedelta(days=1)
closed, adjclosed = getdata.datagetter(allstocks,startday=yday,endday=tday)
df = tickers.history(period='1d', interval='1d')
df = tickers.history(start=yday, end=tday, interval='1d')
def fill_first_non_null(df):
    new_row = df.iloc[0].copy()  # Create a new row by copying the first row of the original dataframe
    for col in new_row.index:
        first_non_null = df[col].first_valid_index()  # Find the index of the first non-null value in the column
        if pd.notnull(new_row[col]):  # Skip columns that already have a non-null value in the first row
            continue
        new_row[col] = df.loc[first_non_null, col]  # Fill the new row with the first non-null value
    new_df = pd.DataFrame([new_row], index=[df.index[0]])  # Create a new dataframe with the new row
    return new_df

df_close = df.reset_index().pivot(index='date',
                                  columns='symbol', values='close')
df_adjclose = df.reset_index().pivot(index='date',
                                  columns='symbol', values='adjclose')
df_volume = df.reset_index().pivot(index='date',
                                  columns='symbol', values='volume')
df_close = fill_first_non_null(df_close)
df_adjclose = fill_first_non_null(df_adjclose)
df_volume = fill_first_non_null(df_volume)
lastday = df_close.index.values[0]
lastdaystr = np.datetime_as_string(lastday, unit='D')
file_name = 'lastday.txt'
with open(file_name, 'w') as file:
    file.write(lastdaystr)