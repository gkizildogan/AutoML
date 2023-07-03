from datetime import date,timedelta
import pandas as pd
import getdata
import datafiller

stocks = ["TRY=X","XU100.IS","AKBNK.IS","ALBRK.IS","GARAN.IS","ICBCT.IS","SKBNK.IS","TSKB.IS","HALKB.IS","ISCTR.IS","VAKBN.IS","YKBNK.IS"]
yday = date.today() - timedelta(days=1)
startday = yday - timedelta(days=729)
closed, adjclosed = getdata.datagetter(stocks,True,startday,yday)

filled_closed = datafiller.filler(closed, 'linear')
filled_adjclosed = datafiller.filler(adjclosed, 'linear')

