from datetime import date,timedelta,datetime
import pandas as pd
import getdailydata
import datafiller
import numpy as np
allstocks = ['AEFES.IS',
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

#tday = date.today()
#yday = tday - timedelta(days=1)
tday = date.today() - timedelta(days=2)
yday = tday - timedelta(days=365*20+193)

closed, adjclosed = getdata.datagetter(allstocks,startday=yday,endday=tday, interval='1d')

filled_closed = datafiller.filler(closed, 'linear')
filled_adjclosed = datafiller.filler(adjclosed, 'linear')

df = pd.read_csv('all_stocks_closed_2003.csv')
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