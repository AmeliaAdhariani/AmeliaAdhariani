# -*- coding: utf-8 -*-
"""Proyek Analisis Data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ug4Ox4qIFDSo1koFA0XiNJE-ce12rECy

# Proyek Analisis Data: [Input Nama Dataset]
- **Nama:** [Amelia Adhariani]
- **Email:** [m198d4kx1406@bangkit.academy]
- **ID Dicoding:** [amelia_adhariani]

## Menentukan Pertanyaan Bisnis

- Jam berapakah penyewaan sepeda paling banyak dan paling sedikit?
- Musim apakah yang menjadi penyewaan sepeda paling banyak?
"""



"""## Import Semua Packages/Library yang Digunakan"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""## Data Wrangling

### Gathering Data
"""

# menampilkan tabel day
day_df = pd.read_csv("/content/day.csv")
day_df.head()

#menampilkan tabel hour
hour_df = pd.read_csv("/content/hour.csv")
hour_df.head()

"""### Assessing Data"""

#memeriksa tipe data
hour_df.info()
day_df.info()

#mengecek missing value di dataset hour
hour_df.isna().sum()

# mengecek missing value di dataset day_df
day_df.isna().sum()

# memeriksa duplikasi
print("Jumlah duplikasi: ", hour_df.duplicated().sum())
print("Jumlah duplikasi: ", day_df.duplicated().sum())

# mengecek parameter statistik dari kolom numerik yang terdapat didalam day_df
day_df.describe()

#memeriksa parameter statistik dari kolom numerik di dalam dataset day
hour_df.describe()

"""### Cleaning Data
* pada dataset ini saya akan menghapus instan dan workingday, dikarenakan workingday sama seperti weekday, dan untuk instant tidak memilki hubungan
* menggunakan tipe data int menjadia category pada kolom 'season', 'mnth','holiday','weekday','weathersit' karena hal2 tersebut memiliki data denga beberapa varian
* mengganti nama kolom agar mudah dipahami
* menghandling tipe data dteday dari 'object' menjadi 'datetime'
* mengonversi isi kolom agar mudah di fahami
* membuat kolom baru category_days yang menunjukan isi kolom tersebut weekend atau weekdays

DROPPING
"""

#menghapus kolom instant dan workingday
hour_df.drop(['workingday'], axis = 1, inplace= True)
day_df.drop(['workingday'], axis = 1, inplace= True)

"""MENGUBAH TIPE DATA

#int to category
"""

#int to category
columns = ['season', 'mnth', 'holiday', 'weekday', 'weathersit']

for column in columns:
    day_df[column] =  day_df[column].astype("category")
    hour_df[column] =  hour_df[column].astype("category")

#object to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

"""RENAME"""

#mengganti nama kolom day_df)
day_df.rename(columns={'yr':'year','mnth':'month','weekday':'one_of_week', 'weathersit':'weather_situation', 'windspeed':'wind_speed','cnt':'count_cr','hum':'humidity'},inplace=True)

#mengganti nama kolom hour_df)
hour_df.rename(columns={'yr':'year','hr':'hours','mnth':'month','weekday':'one_of_week', 'weathersit':'weather_situation','windspeed':'wind_speed','cnt':'count_cr','hum':'humidity'},inplace=True)

# Mengkonversi isi kolom agar mudah dipahami
# konversi season menjadi: 1:Spring, 2:Summer, 3:Fall, 4:Winter
day_df.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)
hour_df.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)

# konversi month menjadi: 1:Jan, 2:Feb, 3:Mar, 4:Apr, 5:May, 6:Jun, 7:Jul, 8:Aug, 9:Sep, 10:Oct, 11:Nov, 12:Dec
day_df.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
hour_df.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)

# konversi weather_situation menjadi: 1:Clear, 2:Misty, 3:Light_RainSnow 4:Heavy_RainSnow
day_df.weather_situation.replace((1,2,3,4), ('Clear','Misty','Light_rainsnow','Heavy_rainsnow'), inplace=True)
hour_df.weather_situation.replace((1,2,3,4), ('Clear','Misty','Light_rainsnow','Heavy_rainsnow'), inplace=True)

# konversi one_of_week menjadi: 0:Sun, 1:Mon, 2:Tue, 3:Wed, 4:Thu, 5:Fri, 6:Sat
day_df.one_of_week.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
hour_df.one_of_week.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)

# konversi year menjadi: 0:2011, 1:2012
day_df.year.replace((0,1), ('2011','2012'), inplace=True)
hour_df.year.replace((0,1), ('2011','2012'), inplace=True)

# Menghitung Humidity
day_df['humidity'] = day_df['humidity']*100
hour_df['humidity'] = hour_df['humidity']*100

"""MEMBUAT KOLOM BARU CATEGORY_DAYS YANG BERISI WEEKEND/ WEEKDAYS"""

one_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
def get_category_days(one_of_week):
    if one_of_week in ["Saturday", "Sunday"]:
        return "weekend"
    else:
        return "weekdays"

hour_df["category_days"] = hour_df["one_of_week"].apply(get_category_days)
day_df["category_days"] = day_df["one_of_week"].apply(get_category_days)

def classify_humidity(humidity):
    if humidity < 45:
        return "Terlalu kering"
    elif humidity >= 45 and humidity < 65:
        return "Ideal"
    else:
        return "Terlalu Lembab"

hour_df["humidity_category"] = hour_df["humidity"].apply(classify_humidity)
day_df["humidity_category"] = day_df["humidity"].apply(classify_humidity)

"""## Exploratory Data Analysis (EDA)

### Explore Data hour_df
"""

# melihat rangkuman parameter dari data hour_df
hour_df.describe(include="all")

"""dari rangkuman parameter diatas, kita akan memperoleh informasi jumlah pelanggan sebanyak 17379. Berdasarkan daat yang ditampilkan antara jam 00.00 sampai 23.59 memiliki rata- rata penyewa sepeda terjaid pada 11.54 dengan standar deasinya sebesar 6.91"""

# penyewaan berdasarkan jam
hour_df.groupby(by="hours").agg({
    "count_cr": ["sum"]
})

"""jika kita lihat pivot table di atas, dapat diketahui bahwa pelanggan yang memilliki banyak menyewa sepeda terjadi pada jam 17.00 sedangkan penyewaan sepeda yang paling sedikit dimiliki pada jam 04.00

EXPLORE DATA day_df
"""

# melihat rangkuman parameter statistik dari data day_df
day_df.describe(include="all")

"""
Pada parameter statistik di atas, kita memperoleh informasi jumlah pelanggan sebanyak 17379 orang di musim 1 - 4 memiliki"""

#jumlah penyewaan tiap season
day_df.groupby(by="season").count_cr.sum().sort_values(ascending=False).reset_index().head(10)

"""
Sebagaimana hasil tersebut, diketahui bahwa season fall dan summer merupakan dua musim yang memiliki jumlah terbanyak."""

# melihat jumlah penyewaan tiap tahun berdasarkan registered dan casul
day_df.groupby(by="year").agg({
    "registered": ["sum"],
    "casual": ["sum"]
})

"""jika dilihat gambar diatas, orang yang sudah menjadi member dengan belum menjadi member memiliki nilai yang cukup jauh, orang yang telah menjadi member pada tahun 2011 sebanyak 995851 sedangkan yang belum menjadi member sebanyak 247252

## Visualization & Explanatory Analysis

### Pertanyaan 1:Jam berapakah penyewaan sepeda paling banyak dan paling sedikit?
"""

# Grouping terhadap hours dan count_cr
sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()

# membuat bar chart untuk melihat perbedaan penyewaan sepeda berdasarkan jam
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# membuat barplot untuk penyewa sepeda terbanyak
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])

# mengatur label dan judul untuk subplot pertama
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# membuat barplot untuk penyewa sepeda terdikit
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])

# mengatur label dan judul untuk subplot pertama
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# menampilkan plot
plt.show()

"""Gambar diatas menunjukkan bahwa penyewaan sepeda paling banyak digunakan pada jam 17:00 sekitar 336860 penyewaan. Sedangkan, penyewaan pada jam 04:00 merupakan produk yang paling sedikit terjual sekitar 4428 penyewaan.

### Pertanyaan 2: Musim apakah yang menjadi penyewaan sepeda paling banyak?
"""

# mengatur warna
colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]

# membuat subplot dengan 1 baris dan 1 kolom, dengan ukuran (20, 10)
fig, ax = plt.subplots(figsize=(20, 10))

# Buat barplot untuk y="count_cr" dan x="season", menggunakan data=day_df
sns.barplot(
        y="count_cr",
        x="season",
        data=day_df.sort_values(by="season", ascending=False),
        palette=colors,
        ax=ax
    )
# mengatur judul, label y dan x, serta tick params untuk subplot tersebut
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)

# menampilkan plot
plt.show()

"""Dari pemaparan diatas dapat disimpulkan musim yang paling banyak disewa ialah pada musim Fall (musim gugur) dengan total penyewaan pada musim gugur sebanyak 1061129 penyewaan

## Conclusion

- Conclution pertanyaan 1: Penyewaan sepeda paling banyak digunakan pada jam 17:00 sekitar 336860 penyewaan. Sedangkan, penyewaan pada jam 04:00 merupakan produk yang paling sedikit terjual sekitar 4428 penyewaan.

- Conclution pertanyaan 2: Musim yang paling banyak penyewaan sepeda adalah  pada musim Fall (musim gugur)

Tidak hanya itu kita dapat menggunakan teknik analisis lanjutan berupa clustering analisis sebgaiaman berikut ini:

Jumlah Pengguna berdasarkan weather_situation
"""

hour_df.groupby(by="weather_situation").count_cr.nunique().sort_values(ascending=False)

"""Dapat disimpulkan bahwa kelompok pengguna yang lebih cenderung menyewa pada ahri- hari yang clear

TOTAL PENGGUNA BERDASARKAN HUMADITY
"""

hour_df.groupby(by="humidity_category").agg({
    "count_cr": ["count"]})

"""kesimpulannya kelompok pengguna yang menyewa sepeda yang itu golongan yang terlalu lembap"""