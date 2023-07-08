from yahooquery import Ticker
from datetime import date,timedelta,datetime
import pandas as pd
import numpy as np


allstocks = [
'AEFES.IS',
'AGHOL.IS',
'AHGAZ.IS',
'AKBNK.IS',
'AKCNS.IS',
'AKFGY.IS',
'AKSA.IS',
'AKSEN.IS',
'ALARK.IS',
'ALBRK.IS',
'ALFAS.IS',
'ARCLK.IS',
'ASELS.IS',
'ASTOR.IS',
'ASUZU.IS',
'AYDEM.IS',
'BAGFS.IS',
'BERA.IS',
'BIMAS.IS',
'BIOEN.IS',
'BRSAN.IS',
'BRYAT.IS',
'BUCIM.IS',
'CANTE.IS',
'CCOLA.IS',
'CEMTS.IS',
'CIMSA.IS',
'DOAS.IS',
'DOHOL.IS',
'ECILC.IS',
'ECZYT.IS',
'EGEEN.IS',
'EKGYO.IS',
'ENJSA.IS',
'ENKAI.IS',
'EREGL.IS',
'EUREN.IS',
'FROTO.IS',
'GARAN.IS',
'GENIL.IS',
'GESAN.IS',
'GLYHO.IS',
'GSDHO.IS',
'GUBRF.IS',
'GWIND.IS',
'HALKB.IS',
'HEKTS.IS',
'IPEKE.IS',
'ISCTR.IS',
'ISDMR.IS',
'ISGYO.IS',
'ISMEN.IS',
'IZMDC.IS',
'KARSN.IS',
'KCAER.IS',
'KCHOL.IS',
'KMPUR.IS',
'KONTR.IS',
'KONYA.IS',
'KORDS.IS',
'KOZAA.IS',
'KOZAL.IS',
'KRDMD.IS',
'KZBGY.IS',
'MAVI.IS',
'MGROS.IS',
'ODAS.IS',
'OTKAR.IS',
'OYAKC.IS',
'PENTA.IS',
'PETKM.IS',
'PGSUS.IS',
'PSGYO.IS',
'QUAGR.IS',
'SAHOL.IS',
'SASA.IS',
'SELEC.IS',
'SISE.IS',
'SKBNK.IS',
'SMRTG.IS',
'SNGYO.IS',
'SOKM.IS',
'TAVHL.IS',
'TCELL.IS',
'THYAO.IS',
'TKFEN.IS',
'TKNSA.IS',
'TOASO.IS',
'TSKB.IS',
'TTKOM.IS',
'TTRAK.IS',
'TUKAS.IS',
'TUPRS.IS',
'ULKER.IS',
'VAKBN.IS',
'VESBE.IS',
'VESTL.IS',
'YKBNK.IS',
'YYLGD.IS',
'ZOREN.IS'
]

file_name = 'lastday.txt'
with open(file_name, 'r') as file:
    lastday = file.read()

lastdaydate = datetime.strptime(lastday, '%Y-%m-%d').date()
sday = lastdaydate + timedelta(days=1)
eday = sday + timedelta(days=1)
tickers = Ticker(allstocks)
df_hist = tickers.history(start=sday, end=eday, interval='1d')

def fill_first_non_null(df):
    new_row = df.iloc[0].copy()
    for col in new_row.index:
        first_non_null = df[col].first_valid_index()
        if pd.notnull(new_row[col]):
            continue
        new_row[col] = df.loc[first_non_null, col]
    new_df = pd.DataFrame([new_row], index=[df.index[0]])
    return new_df


df_close = df_hist.reset_index().pivot(index='date',
                                  columns='symbol', values='close')
df_adjclose = df_hist.reset_index().pivot(index='date',
                                  columns='symbol', values='adjclose')
df_volume = df_hist.reset_index().pivot(index='date',
                                  columns='symbol', values='volume')
df_close = fill_first_non_null(df_close)
df_close = df_close.reset_index(names="date")
df_close['date'] = df_close['date'].dt.date.astype('object')
df_adjclose = fill_first_non_null(df_adjclose)
df_adjclose = df_adjclose.reset_index(names="date")
df_adjclose['date'] = df_adjclose['date'].dt.date.astype('object')
df_volume = fill_first_non_null(df_volume)
df_volume = df_volume.reset_index(names="date")
df_volume['date'] = df_volume['date'].dt.date.astype('object')

close_name = 'all_stocks_closed_2003.csv'
adjclose_name = 'all_stocks_adjclosed_2003.csv'
volume_name = 'all_stocks_volume_2003.csv'

df_close_all = pd.read_csv(close_name)
df_adjclose_all = pd.read_csv(adjclose_name)
df_volume_all = pd.read_csv(volume_name)

common_columns_close = list(set(df_close_all.columns) & set(df_close.columns))
common_columns_adjclose = list(set(df_adjclose_all.columns) & set(df_adjclose.columns))
common_columns_volume = list(set(df_volume_all.columns) & set(df_volume.columns))

df_close_all = pd.concat([df_close_all, df_close[common_columns_close]], ignore_index=True)
df_close_all.to_csv(close_name)

df_adjclose_all = pd.concat([df_adjclose_all, df_adjclose[common_columns_adjclose]], ignore_index=True)
df_adjclose_all.to_csv(adjclose_name)

df_volume_all = pd.concat([df_volume_all, df_volume[common_columns_volume]], ignore_index=True)
df_volume_all.to_csv(volume_name)

with open(file_name, 'w') as file:
    file.write(str(sday))