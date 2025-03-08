import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Load cleaned dataset
all_df = pd.read_csv("dashboard/main_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Dashboard Title
st.title("📊 Dashboard Penyewaan Sepeda")

# Sidebar
st.sidebar.header("Filter Data")
selected_season = st.sidebar.multiselect("Pilih Musim", options=all_df['season_name'].unique(), default=all_df['season_name'].unique())
selected_weather = st.sidebar.multiselect("Pilih Cuaca", options=all_df['weather_name'].unique(), default=all_df['weather_name'].unique())

# Filter data
df_filtered = all_df[(all_df['season_name'].isin(selected_season)) & (all_df['weather_name'].isin(selected_weather))]

# Visualisasi Tren Penyewaan Sepeda
st.subheader("📈 Tren Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(x=df_filtered['dteday'], y=df_filtered['cnt'], ax=ax, color='red')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Tren Penyewaan Sepeda Harian")
st.pyplot(fig)

# Visualisasi Penyewaan Berdasarkan Cuaca
st.subheader("🌦️ Rata-rata Penyewaan Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(10, 5))
weather_counts = df_filtered.groupby("weather_name")["cnt"].mean().reset_index()
sns.barplot(x="weather_name", y="cnt", data=weather_counts, palette="coolwarm", ax=ax)
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
st.pyplot(fig)

# Visualisasi Korelasi Antar Variabel
st.subheader("🔥 Korelasi Antar Variabel")
fig, ax = plt.subplots(figsize=(10, 6))
numeric_cols = df_filtered.select_dtypes(include=['number'])
sns.heatmap(numeric_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
st.pyplot(fig)

# Kesimpulan
st.subheader("📌 Kesimpulan")
st.markdown("1. **Hujan atau salju secara signifikan mengurangi jumlah penyewaan sepeda**, terbukti dari rata-rata penyewaan yang jauh lebih rendah pada kondisi cuaca buruk.")
st.markdown("2. **Faktor utama yang berkontribusi terhadap jumlah penyewaan sepeda** adalah suhu (temp), diikuti oleh kelembapan (hum) dan kecepatan angin (windspeed), seperti yang ditunjukkan oleh korelasi yang lebih tinggi dalam heatmap.")
st.markdown("3. **Musim juga mempengaruhi penyewaan**, dengan peningkatan jumlah penyewaan selama musim gugur dan kondisi cuaca cerah.")
