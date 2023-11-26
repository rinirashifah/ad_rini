# -*- coding: utf-8 -*-
"""Analisis Data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_Q_95E17TxRoW_AfjoIvRz-IHyihBSZp

# Proyek Analisis Data: Nama dataset
- Nama: Rini Rashifah
- Email: rinirashifahv@gmail.com
- Id Dicoding:

## Menentukan Pertanyaan Bisnis

- pertanyaan 1
Apakah terdapat pola atau tren tertentu dalam tingkat PM2.5 selama berbagai kondisi cuaca seperti suhu, kecepatan angin, atau arah angin?

- pertanyaan 2
Apakah terdapat perbedaan yang signifikan dalam tingkat polusi udara antara jam-jam tertentu dalam sehari?

## Menyiapkan semua library yang dibutuhkan
"""

!pip install streamlit

import pandas as pd
import streamlit as st
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns

"""## Data Wrangling

### Gathering Data
"""

# Membaca data dari file CSV
file_path = '/content/drive/My Drive/dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv'
df = pd.read_csv(file_path)

# Menampilkan beberapa baris pertama data
print(df.head())

"""### Assessing Data"""

# Menampilkan jumlah duplikasi
duplicate_count = df.duplicated().sum()
print(f"Jumlah duplikasi: {duplicate_count}")

# Menampilkan informasi mengenai nilai yang hilang
missing_info = df.isnull().sum()
print("Informasi mengenai nilai yang hilang:")
print(missing_info)

"""### Cleaning Data"""

# Imputasi untuk kolom-kolom tertentu
columns_to_impute = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM']

# Imputasi dengan median
df[columns_to_impute] = df[columns_to_impute].fillna(df[columns_to_impute].median())

# Imputasi untuk kolom 'wd' dengan nilai tertentu (misalnya, mode)
custom_value_wd = df['wd'].mode()[0]
df['wd'] = df['wd'].fillna(custom_value_wd)

# Imputasi untuk kolom 'WSPM' dengan nilai mean
df['WSPM'] = df['WSPM'].fillna(df['WSPM'].mean())

# Menyimpan DataFrame setelah imputasi ke file CSV
df.to_csv('/content/drive/My Drive/dataset/PRSA_Data_Nongzhanguan_Imputed.csv', index=False)

"""## Exploratory Data Analysis (EDA)

### Explore ...
"""

# Menampilkan data awal
print("Data Awal:")
print(df.head())

# Melakukan EDA dengan mengurutkan berdasarkan kolom tertentu
# Misalnya, mengurutkan berdasarkan kolom 'PM2.5' secara descending
sorted_df = df.sort_values(by='PM2.5', ascending=False)

# Menampilkan data setelah diurutkan
print("\nData Setelah Diurutkan:")
print(sorted_df.head())

"""## Visualization & Explanatory Analysis

### Pertanyaan 1:
"""

# Menggunakan DataFrame setelah imputasi
df_imputed = pd.read_csv('/content/drive/My Drive/dataset/PRSA_Data_Nongzhanguan_Imputed.csv')

# Visualisasi hubungan antara PM2.5 dan suhu
plt.figure(figsize=(12, 8))
sns.regplot(x='TEMP', y='PM2.5', data=df_imputed, scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'})
plt.title('Hubungan antara PM2.5 dan Suhu (Data yang Telah Diimputasi)')
plt.xlabel('Suhu (Celsius)')
plt.ylabel('PM2.5')
plt.show()

# Menggunakan DataFrame asli sebelum imputasi
df_original = pd.read_csv('/content/drive/My Drive/dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv')

# Visualisasi hubungan antara PM2.5 dan suhu
plt.figure(figsize=(12, 8))
sns.regplot(x='TEMP', y='PM2.5', data=df_original, scatter_kws={'alpha': 0.3}, line_kws={'color': 'blue'})
plt.title('Hubungan antara PM2.5 dan Suhu (Data Asli)')
plt.xlabel('Suhu (Celsius)')
plt.ylabel('PM2.5')
plt.show()

"""### Pertanyaan 2:

"""

# Membaca data dari file CSV
file_path = '/content/drive/My Drive/dataset/PRSA_Data_Nongzhanguan_20130301-20170228.csv'
df = pd.read_csv(file_path)

# Menghapus nilai yang hilang untuk mempermudah analisis (jangan lakukan ini jika nilai hilang perlu ditangani secara khusus)
df_cleaned = df.dropna(subset=['PM2.5', 'hour'])

# Menampilkan distribusi tingkat polusi udara berdasarkan jam
plt.figure(figsize=(12, 8))
sns.boxplot(x='hour', y='PM2.5', data=df_cleaned)
plt.title('Distribusi Tingkat Polusi Udara Berdasarkan Jam')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('PM2.5')
plt.show()

# Melakukan uji statistik ANOVA
hours = df_cleaned['hour'].unique()
groups = [df_cleaned[df_cleaned['hour'] == hour]['PM2.5'] for hour in hours]
statistic, p_value = f_oneway(*groups)

# Menampilkan hasil uji statistik
print(f'Hasil Uji Statistik ANOVA: F = {statistic}, p-value = {p_value}')

# Menentukan apakah perbedaan signifikan (umumnya menggunakan alpha = 0.05)
alpha = 0.05
if p_value < alpha:
    print('Terdapat perbedaan yang signifikan dalam tingkat polusi udara antara jam-jam tertentu.')
else:
    print('Tidak terdapat perbedaan yang signifikan dalam tingkat polusi udara antara jam-jam tertentu.')

"""## Conclusion

- Conclution pertanyaan 1
Berdasarkan analisis data, terdapat hubungan antara tingkat PM2.5 dengan kondisi cuaca tertentu. Visualisasi menunjukkan tren positif antara suhu dan PM2.5, menunjukkan korelasi potensial dengan peningkatan polusi pada suhu yang lebih tinggi. Analisis kecepatan angin memberikan konteks tambahan.
- conclution pertanyaan 2
Analisis menunjukkan perbedaan signifikan dalam tingkat polusi udara antar jam dalam sehari. Uji statistik ANOVA mengungkapkan variasi yang signifikan pada distribusi PM2.5 pada berbagai jam. Melalui visualisasi Boxplot, ditemukan [deskripsi visual yang relevan, misalnya, perbedaan antara jam sibuk dan jam sepi].
"""