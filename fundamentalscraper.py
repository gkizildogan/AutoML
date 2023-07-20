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

s = Service('D:/chromedriver/chromedriver-win64/chromedriver.exe')


driver = webdriver.Chrome(service=s)
driver.get('https://halkyatirim.com.tr/skorkart')

time.sleep(10)
select_element = driver.find_element(By.ID, 'DropDownEnstrumanKodu')
select = Select(select_element)


# Dropdown options
opts = select.options

# Dropdown options as texts
opt_list = []
for i in range(len(opts)):
    opt_list.append(opts[i].text)

opt_list = opt_list[1:]
#for i in range(1, len(opt_list)):
for i, opt_name in enumerate(opt_list):
    select.options[i+1].click()
    time.sleep(60)
    # Wait ekle div class id='divSirketVerileri
    page_source = driver.page_source
    soup = BeautifulSoup(page_source)
    tablolar = soup.findChildren('table')
    #element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "LabelEnstrumanKodu")))

    # Temel Bilgiler
    enstruman_kodu = driver.find_element(By.ID,'LabelEnstrumanKodu').text
    hesap_donemi = driver.find_element(By.ID,'LabelHesapDonem').text
    fiyat = driver.find_element(By.ID,'mPrice').text
    halka_aciklik_orani = driver.find_element(By.ID,'mHAO').text
    yillik_degisim = driver.find_element(By.ID,'mYD').text
    mom = driver.find_element(By.ID,'mMOM').text
    rsi = driver.find_element(By.ID,'mRSI').text
    temettu_verimi = driver.find_element(By.ID,'mTV').text
    ozsermaye_karliligi = driver.find_element(By.ID,'mOK').text
    net_kar_buyume_orani = driver.find_element(By.ID,'mNKBO').text
    net_kar_marji_yillik = driver.find_element(By.ID,'mNKMY').text
    fk = driver.find_element(By.ID,'mFK').text
    fd_favok = driver.find_element(By.ID,'mFD').text

    temel_bilgiler_isim = ['Enstruman Kodu','Hesap Dönemi','Yıllık Değişim','MOM','RSI','Temettü Verimi',
                           'Özsermaye Karlılığı', 'Net Kar Büyüme Oranı', 'Net Kar Marjı (Yıllık)', 'FK', 'FD/FAVÖK']
    temel_bilgiler = [enstruman_kodu,hesap_donemi,yillik_degisim,mom,rsi,temettu_verimi,ozsermaye_karliligi,
                      net_kar_buyume_orani,net_kar_marji_yillik,fk,fd_favok]

    df_temel_bilgi = pd.DataFrame([temel_bilgiler], columns=temel_bilgiler_isim)

    pazarendeksler = tablolar[0]
    header = []
    rows = []
    for i, row in enumerate(pazarendeksler.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])

    pazar_endeks_adi = [item[0] for item in rows]
    pazar_endeks_degeri = [item[1] for item in rows]

    df_pazar_endeks = pd.DataFrame([pazar_endeks_degeri],columns=pazar_endeks_adi)
    # isim : değer

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
    performans_donemleri = header[1:]

    df_fiyat_performans = pd.DataFrame(performans_degerleri, columns=performans_donemleri, index=performans_indeksi)

    # İndeksler yatayda 3 taneler. Dönemler ve degerler alt alta fakat degerler list of lists

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
    # isim : miktar
    df_piyasa_deger = pd.DataFrame([piyasa_deger_miktari], columns=piyasa_deger_adi)

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

    df_finansal_tablo = pd.DataFrame(finansal_tablo_deger, columns=finansal_tablo_sutun_isimleri,
                                     index=finansal_tablo_index)


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

    df_karlilik_tablo = pd.DataFrame(karlilik_tablo_deger, columns=karlilik_tablo_sutun_isimleri,
                                     index=karlilik_tablo_index)

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

    df_carpanlar_tablo = pd.DataFrame(carpanlar_tablo_deger, columns=carpanlar_tablo_sutun_isimleri,
                                     index=carpanlar_tablo_index)

    folder_path = os.path.join(current_directory, opt_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_filename = os.path.join(folder_path, opt_name + '.csv')
    df_carpanlar_tablo.to_csv(csv_filename, index=True)

    time.sleep(5)