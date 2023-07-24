from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
char_mapping = {
    "İ": "I",
    "ı": "i",
    "Â": "A",
    "â": "a",
    "Î": "I",
    "î": "i",
    "Ş": "S",
    "ş": "s",
    "Ö": "O",
    "ö": "o",
    "Ü": "U",
    "ü": "u",
    "Ğ": "G",
    "ğ": "g",
    "Ç": "C",
    "ç": "c",
    "%": "yuzde",
    "(": "_",
    ")": "_",
    "+": "_",
    " ": "_",
    "-": "_",
    "/": "_",
    ".": "_",
    "$": "usd"
}
s = Service('D:/chromedriver/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('https://halkyatirim.com.tr/skorkart')
element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "DropDownEnstrumanKodu")))
select_element = driver.find_element(By.ID, 'DropDownEnstrumanKodu')
select = Select(select_element)
bugunun_tarihi = pd.Timestamp('today').strftime('%Y-%m-%d')
opts = select.options
opt_list = []
for i in range(len(opts)):
    opt_list.append(opts[i].text)

all_temel_bilgi = []
all_pazar_endeks = []
all_fiyat_perf = []
all_piyasa_deger = []
all_indikator = []
all_temel_analiz = []
all_fiyat_ozet = []
all_finansal_tablo = []
all_karlilik_tablo = []
all_carpanlar_tablo = []

opt_list = opt_list[:1]
for idx, opt_name in enumerate(opt_list):
    select.options[idx+1].click()
    element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, "divSirketVerileri")))
    # Wait ekle div class id='divSirketVerileri
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    tablolar = soup.findChildren('table')

    # Temel Bilgiler
    enstruman_kodu = driver.find_element(By.ID,'LabelEnstrumanKodu').text
    hesap_donemi = driver.find_element(By.ID,'LabelHesapDonem').text
    fiyat = driver.find_element(By.ID,'mPrice').text
    halka_aciklik_orani = driver.find_element(By.ID,'mHAO').text
    halka_aciklik_orani = halka_aciklik_orani.replace("% ","")
    yillik_degisim = driver.find_element(By.ID,'mYD').text
    mom = driver.find_element(By.ID,'mMOM').text
    rsi = driver.find_element(By.ID,'mRSI').text
    temettu_verimi = driver.find_element(By.ID,'mTV').text
    ozsermaye_karliligi = driver.find_element(By.ID,'mOK').text
    net_kar_buyume_orani = driver.find_element(By.ID,'mNKBO').text
    net_kar_marji_yillik = driver.find_element(By.ID,'mNKMY').text
    fk = driver.find_element(By.ID,'mFK').text
    fd_favok = driver.find_element(By.ID,'mFD').text

    temel_bilgiler_isim = ['enstruman_kodu','hesap_donemi','fiyat','halka_aciklik_orani','yillik_degisim','mom','rsi',
                           'temettu_verimi','ozsermaye_karliligi','net_kar_buyume_orani','net_kar_marji_yillik','fk',
                           'fd_favok']
    temel_bilgiler = [enstruman_kodu,hesap_donemi,fiyat,halka_aciklik_orani,yillik_degisim,mom,rsi,temettu_verimi,
                      ozsermaye_karliligi, net_kar_buyume_orani,net_kar_marji_yillik,fk,fd_favok]
    temel_bilgiler = [string if string != "" else "-" for string in temel_bilgiler]

    df_temel_bilgi = pd.DataFrame([temel_bilgiler], columns=temel_bilgiler_isim)
    df_temel_bilgi = df_temel_bilgi.replace(',', '', regex=True)

    pazarendeksler = tablolar[0]
    header = []
    rows = []
    for i, row in enumerate(pazarendeksler.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    #pazar_endeks_adi = [item[0] for item in rows]
    pazar_endeks_adi = ['dahil_oldugu_sektor','dahil_oldugu_endeksler','odenmis_sermaye_tl','halka_aciklik_orani']
    pazar_endeks_degeri = [item[1] for item in rows]

    df_pazar_endeks = pd.DataFrame([pazar_endeks_degeri],columns=pazar_endeks_adi)
    df_pazar_endeks['odenmis_sermaye_tl'] = df_pazar_endeks['odenmis_sermaye_tl'].str.replace(',', '').str.replace(' TL', '')
    df_pazar_endeks['halka_aciklik_orani'] = df_pazar_endeks['halka_aciklik_orani'].str.replace('% ', '')

    df_pazar_endeks.insert(0, "veri_toplanma_tarihi", str(bugunun_tarihi))
    df_pazar_endeks.insert(1, "enstruman_kodu", str(enstruman_kodu))

    fiyatperformans = tablolar[1]
    header = []
    rows = []
    for i, row in enumerate(fiyatperformans.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    performans_indeksi = [item[0] for item in rows]
    performans_degerleri = [item[1:] for item in rows]
    performans_donemleri = ['son_1_hafta','son_1_ay','son_3_ay','son_6_ay','son_1_yıl']
    df_fiyat_performans_enstruman = pd.DataFrame(performans_degerleri, columns=performans_donemleri, index=performans_indeksi)

    index = df_fiyat_performans_enstruman.index.to_list()

    # Create a new DataFrame
    new_data = {}
    for col in df_fiyat_performans_enstruman.columns:
        new_data[col] = [df_fiyat_performans_enstruman.at[index[0], col]]

    for col in df_fiyat_performans_enstruman.columns:
        new_data[f"{col}_{index[2]}"] = [df_fiyat_performans_enstruman.at[index[2], col]]

    df_fiyat_perf_enstru = pd.DataFrame(new_data)

    df_fiyat_perf_enstru.insert(0, "veri_toplanma_tarihi", str(bugunun_tarihi))
    df_fiyat_perf_enstru.insert(1, "enstruman_kodu", str(enstruman_kodu))
    df_fiyat_perf_enstru = df_fiyat_perf_enstru.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_fiyat_perf_enstru = df_fiyat_perf_enstru.rename(columns=lambda x: x.replace('__', '_'))
    df_fiyat_perf_enstru = df_fiyat_perf_enstru.replace(',', '', regex=True)

    piyasadegertablosu = tablolar[2]
    header = []
    rows = []
    for i, row in enumerate(piyasadegertablosu.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    piyasa_deger_adi = [item[0] for item in rows]
    piyasa_deger_miktari = [item[1] for item in rows]
    df_piyasa_deger = pd.DataFrame([piyasa_deger_miktari], columns=piyasa_deger_adi)
    df_piyasa_deger.insert(0, "veri_toplanma_tarihi", str(bugunun_tarihi))
    df_piyasa_deger.insert(1, "enstruman_kodu", str(enstruman_kodu))
    df_piyasa_deger = df_piyasa_deger.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_piyasa_deger = df_piyasa_deger.rename(columns=lambda x: x.replace('__', '_'))
    df_piyasa_deger = df_piyasa_deger.replace(',', '', regex=True)


    teknikveritablosu = tablolar[3]
    header = []
    rows = []
    for i, row in enumerate(teknikveritablosu.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])


    indikator_adi = [item[0] for item in rows]
    indikator_degeri = [item[1] for item in rows]
    indikator_yorum = [item[2] for item in rows]

    df_indikator_deger = pd.DataFrame([indikator_degeri], columns=indikator_adi)
    df_indikator_yorum = pd.DataFrame([indikator_yorum], columns=indikator_adi)
    df_indikator_yorum.columns = [col + "_yorum" for col in df_indikator_yorum.columns]
    df_indikator = pd.concat([df_indikator_deger, df_indikator_yorum], axis=1)
    df_indikator.insert(0, "veri_toplanma_tarihi", str(bugunun_tarihi))
    df_indikator.insert(1, "enstruman_kodu", str(enstruman_kodu))
    df_indikator = df_indikator.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_indikator = df_indikator.rename(columns=lambda x: x.replace('__', '_'))
    df_indikator = df_indikator.replace(',', '', regex=True)

    temel_analiz_tablosu = tablolar[4]
    header = []
    rows = []
    for i, row in enumerate(temel_analiz_tablosu.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    temel_deger_adi = [item[0] for item in rows]
    temel_deger_degeri = [item[1] for item in rows]

    df_temel_analiz = pd.DataFrame([temel_deger_degeri], columns=temel_deger_adi)
    df_temel_analiz.insert(0, "veri_toplanma_tarihi", str(bugunun_tarihi))
    df_temel_analiz.insert(1, "enstruman_kodu", str(enstruman_kodu))
    df_temel_analiz = df_temel_analiz.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_temel_analiz = df_temel_analiz.rename(columns=lambda x: x.replace('__', '_'))
    df_temel_analiz = df_temel_analiz.replace(',', '', regex=True)

    fiyat_ozet_tablosu = tablolar[5]
    header = []
    rows = []
    for i, row in enumerate(fiyat_ozet_tablosu.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    fiyat_ozet_adi = [item[0] for item in rows]
    fiyat_ozet_degeri = [item[1] for item in rows]

    df_fiyat_ozet = pd.DataFrame([fiyat_ozet_degeri], columns=fiyat_ozet_adi)
    df_fiyat_ozet.insert(0, "veri_toplanma_tarihi", str(bugunun_tarihi))
    df_fiyat_ozet.insert(1, "enstruman_kodu", str(enstruman_kodu))
    df_fiyat_ozet = df_fiyat_ozet.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_fiyat_ozet = df_fiyat_ozet.rename(columns=lambda x: x.replace('__', '_'))
    df_fiyat_ozet = df_fiyat_ozet.replace(',', '', regex=True)
    df_fiyat_ozet[['bir_yillik_bant_min', 'bir_yillik_bant_max']] = df_fiyat_ozet['bir_yillik_bant_min_max'].str.split(
        '-', expand=True)
    df_fiyat_ozet = df_fiyat_ozet.drop(columns=['bir_yillik_bant_min_max'])
    df_fiyat_ozet = df_fiyat_ozet.rename(columns=lambda x: x.replace('__', '_'))
    df_fiyat_ozet = df_fiyat_ozet.replace(',', '', regex=True)

    finansallar_tablosu = tablolar[6]
    header = []
    rows = []
    for i, row in enumerate(finansallar_tablosu.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    finansal_tablo_sutun_isimleri = header[1:]
    finansal_tablo_index = [item[0] for item in rows]
    finansal_tablo_deger = [item[1:] for item in rows]

    df_finansal_tablo = pd.DataFrame(finansal_tablo_deger, columns=finansal_tablo_sutun_isimleri)
    df_finansal_tablo.insert(0, "enstruman_kodu", str(enstruman_kodu))
    df_finansal_tablo.insert(1, "finans_donemi", finansal_tablo_index)
    df_finansal_tablo = df_finansal_tablo.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_finansal_tablo = df_finansal_tablo.rename(columns=lambda x: x.replace('__', '_').replace('__', '_'))
    df_finansal_tablo = df_finansal_tablo.replace(',', '', regex=True)

    karlilik_tablosu = tablolar[7]
    header = []
    rows = []
    for i, row in enumerate(karlilik_tablosu.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    karlilik_tablo_sutun_isimleri = header[1:]
    karlilik_tablo_index = [item[0] for item in rows]
    karlilik_tablo_deger = [item[1:] for item in rows]

    df_karlilik_tablo = pd.DataFrame(karlilik_tablo_deger, columns=karlilik_tablo_sutun_isimleri)
    df_karlilik_tablo.insert(0, "enstruman_kodu", str(enstruman_kodu))
    df_karlilik_tablo.insert(1, "finans_donemi", karlilik_tablo_index)
    df_karlilik_tablo = df_karlilik_tablo.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_karlilik_tablo = df_karlilik_tablo.rename(columns=lambda x: x.replace('__', '_').replace('__', '_').replace('_x',''))
    df_karlilik_tablo = df_karlilik_tablo.replace(',', '', regex=True)

    carpanlar_tablosu = tablolar[8]
    header = []
    rows = []
    for i, row in enumerate(carpanlar_tablosu.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    carpanlar_tablo_sutun_isimleri = header[1:]
    carpanlar_tablo_index = [item[0] for item in rows]
    carpanlar_tablo_deger = [item[1:] for item in rows]

    df_carpanlar_tablo = pd.DataFrame(carpanlar_tablo_deger, columns=carpanlar_tablo_sutun_isimleri)
    df_carpanlar_tablo.insert(0, "enstruman_kodu", str(enstruman_kodu))
    df_carpanlar_tablo.insert(1, "finans_donemi", carpanlar_tablo_index)
    df_carpanlar_tablo = df_carpanlar_tablo.rename(
        columns=lambda col: ''.join(char_mapping.get(c, c) for c in col).lower().rstrip('_'))
    df_carpanlar_tablo = df_carpanlar_tablo.rename(columns=lambda x: x.replace('__', '_').replace('__', '_').replace('_x',''))
    df_carpanlar_tablo = df_carpanlar_tablo.replace(',', '', regex=True)

    all_temel_bilgi.append(df_temel_bilgi)
    all_pazar_endeks.append(df_pazar_endeks)
    all_fiyat_perf.append(df_fiyat_perf_enstru)
    all_piyasa_deger.append(df_piyasa_deger)
    all_indikator.append(df_indikator)
    all_temel_analiz.append(df_temel_analiz)
    all_fiyat_ozet.append(df_fiyat_ozet)
    all_finansal_tablo.append(df_finansal_tablo)
    all_karlilik_tablo.append(df_karlilik_tablo)
    all_carpanlar_tablo.append(df_carpanlar_tablo)

    print(f"Scraped element:{enstruman_kodu} with id:{idx}")
    time.sleep(3)

all_temel_bilgi_df = pd.concat(all_temel_bilgi, ignore_index=True)
all_pazar_endeks_df = pd.concat(all_pazar_endeks, ignore_index=True)
all_fiyat_perf_df = pd.concat(all_fiyat_perf, ignore_index=True)
all_piyasa_deger_df = pd.concat(all_piyasa_deger, ignore_index=True)
all_indikator_df = pd.concat(all_indikator, ignore_index=True)
all_temel_analiz_df = pd.concat(all_temel_analiz, ignore_index=True)
all_fiyat_ozet_df = pd.concat(all_fiyat_ozet, ignore_index=True)
all_finansal_tablo_df = pd.concat(all_finansal_tablo, ignore_index=True)
all_karlilik_tablo_df = pd.concat(all_karlilik_tablo, ignore_index=True)
all_carpanlar_tablo_df = pd.concat(all_carpanlar_tablo, ignore_index=True)

all_temel_bilgi_df.to_csv('all_temel_bilgi.csv', index=False)
all_pazar_endeks_df.to_csv('all_pazar_endeks.csv', index=False)
all_fiyat_perf_df.to_csv('all_fiyat_perf.csv', index=False)
all_piyasa_deger_df.to_csv('all_piyasa_deger.csv', index=False)
all_indikator_df.to_csv('all_indikator.csv', index=False)
all_temel_analiz_df.to_csv('all_temel_analiz.csv', index=False)
all_fiyat_ozet_df.to_csv('all_fiyat_ozet.csv', index=False)
all_finansal_tablo_df.to_csv('all_finansal_tablo.csv', index=False)
all_karlilik_tablo_df.to_csv('all_karlilik_tablo.csv', index=False)
all_carpanlar_tablo_df.to_csv('all_carpanlar_tablo.csv', index=False)
