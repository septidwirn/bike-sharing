# Import library yang dibutuhkan
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


# Membuat helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule="D", on="dteday").agg({
        "instant": "nunique",
        "cnt": "sum",
        "registered": "sum",
        "casual": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "instant": "day_count",
        "cnt": "total_rental"
    }, inplace=True)
    return daily_rentals_df

def create_mean_rentals_byweekday_df(df):
    mean_rentals_byweekday_df = df.groupby("weekday").agg({
        "casual": ["mean"],
        "registered": ["mean"],
        "cnt": ["mean"]
    })
    return mean_rentals_byweekday_df

def create_mean_rentals_byhour_df(df):
    mean_rentals_byhour_df = df.groupby("hr").agg({
        "casual": ["mean"],
        "registered": ["mean"],
        "cnt": ["mean"]
    })
    return mean_rentals_byhour_df

def create_seasonal_rentals_df(df):
    seasonal_rentals_df = df.groupby("season").agg({
        "casual": ["sum"],
        "registered": ["sum"],
        "cnt": ["sum"]
    })
    return seasonal_rentals_df
    

# Memuat data
all_df = pd.read_csv("dashboard/hour.csv")
# Mengubah kolom dteday menjadi jenis data datetime
all_df["dteday"] = pd.to_datetime(all_df["dteday"])
# Mengurutkan data berdasarkan dteday    
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)


# Membuat komponen filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo
    st.image("https://media.istockphoto.com/id/854733622/vector/bicycle-icon.jpg?s=612x612&w=0&k=20&c=cu34k4KEV5VYWwwVbMAmPogLJmh-OBITXEd1d9rWfrw=")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Timeframe",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
# Mengambil data sesuai dengan rentang waktu
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]


# Menyiapkan dataframe
daily_rentals_df = create_daily_rentals_df(main_df)
mean_rentals_byweekday_df = create_mean_rentals_byweekday_df(main_df)
mean_rentals_byhour_df = create_mean_rentals_byhour_df(main_df)
seasonal_rentals_df = create_seasonal_rentals_df(main_df)


# Visualisasi data
st.header("Bike Sharing Dashboard :bike:")

st.subheader("Daily Rentals")

# Menampilkan jumlah penyewa
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = daily_rentals_df.total_rental.sum()
    st.metric("Total rentals", value=total_rentals)
with col2:
    total_registered_users = daily_rentals_df.registered.sum() 
    st.metric("Registered users", value=total_registered_users)
with col3:
    total_casual_users = daily_rentals_df.casual.sum() 
    st.metric("Casual users", value=total_casual_users)

# Menmapilkan grafik jumlah total penyewa harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["total_rental"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=18)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Daily Rentals Over Time", fontsize=24, pad=20)  # Judul grafik
ax.set_xlabel("Date", fontsize=18, labelpad=15)  # Keterangan sumbu x
ax.set_ylabel("Total Rentals", fontsize=18, labelpad=15)  # Keterangan sumbu y

st.pyplot(fig)

# Menampilkan grafik jumlah penyewa registered dan casual
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["registered"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=18)
    ax.tick_params(axis='x', labelsize=15)
    ax.set_title("Daily Registered User Rentals Over Time", fontsize=24, pad=20)  # Judul grafik
    ax.set_xlabel("Date", fontsize=18, labelpad=15)  # Keterangan sumbu x
    ax.set_ylabel("Total Registered User Rentals", fontsize=18, labelpad=15)  # Keterangan sumbu y
    #plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
    daily_rentals_df["dteday"],
    daily_rentals_df["casual"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=18)
    ax.tick_params(axis='x', labelsize=15)
    ax.set_title("Daily Casual User Rentals Over Time", fontsize=24, pad=20)  # Judul grafik
    ax.set_xlabel("Date", fontsize=18, labelpad=15)  # Keterangan sumbu x
    ax.set_ylabel("Total Casual User Rentals", fontsize=18, labelpad=15)  # Keterangan sumbu y
    #plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

# Menampilkan grafik rata-rata total penyewa berdasarkan waktu dan hari
st.subheader("Busy and Quite Time")

# Grafik berdasarkan hari

# Ubah index agar lebih mudah diproses untuk plotting
mean_rentals_byweekday_df.columns = ["casual_mean", "registered_mean", "total_mean"]
mean_rentals_byweekday_df.reset_index(inplace=True)

# Membuat label hari
days_labels = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Identifikasi nilai tertinggi dan terendah
max_value = mean_rentals_byweekday_df["total_mean"].max()
min_value = mean_rentals_byweekday_df["total_mean"].min()

# Menentukan warna untuk setiap bar
colors = [
    "#EF5350" if val == max_value else
    "#66BB6A" if val == min_value else
    "#90CAF9"
    for val in mean_rentals_byweekday_df["total_mean"]
]

# Membuat grafik dengan matplotlib
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    mean_rentals_byweekday_df["weekday"],
    mean_rentals_byweekday_df["total_mean"],
    color=colors
)
ax.set_title("Average Total Rental Amount by Day", fontsize=24, pad=20)
#ax.set_xlabel("Day", fontsize=18, labelpad=10)
ax.set_ylabel("Average Total Rental Amount", fontsize=18, labelpad=10)
plt.xticks(ticks=range(7), labels=days_labels, fontsize=15) 

# Tampilkan grafik di Streamlit
st.pyplot(fig)

# Grafik berdasarkan jam

# Ubah index agar lebih mudah diproses untuk plotting
mean_rentals_byhour_df.columns = ["casual_mean", "registered_mean", "total_mean"]
mean_rentals_byhour_df.reset_index(inplace=True)

# Membuat label jam
hour_labels = ["00.00", "01.00", "02.00", "03.00", "04.00", "05.00", "06.00", "07.00", "08.00", "09.00", 
               "10.00", "11.00", "12.00", "13.00", "14.00", "15.00", "16.00", "17.00", "18.00", "19.00",
               "20.00", "21.00", "22.00", "23.00"]

# Identifikasi nilai tertinggi dan terendah
max_value = mean_rentals_byhour_df["total_mean"].max()
min_value = mean_rentals_byhour_df["total_mean"].min()

# Menentukan warna untuk setiap bar
colors = [
    "#EF5350" if val == max_value else
    "#66BB6A" if val == min_value else
    "#90CAF9"
    for val in mean_rentals_byhour_df["total_mean"]
]

# Membuat grafik dengan matplotlib
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    mean_rentals_byhour_df["hr"],
    mean_rentals_byhour_df["total_mean"],
    color=colors
)
ax.set_title("Average Total Rental Amount by Hour", fontsize=24, pad=20)
#ax.set_xlabel("Hour", fontsize=18, labelpad=10)
ax.set_ylabel("Average Total Rental Amount", fontsize=18, labelpad=10)
ax.tick_params(axis='x', labelrotation=45)
plt.xticks(ticks=range(24), labels=hour_labels, fontsize=15) 

# Tampilkan grafik di Streamlit
st.pyplot(fig)

# Menampilkan grafik jumlah penyewa berdasarkan musim
st.subheader('Seasonal Rentals')

# Ubah index agar lebih mudah diproses untuk plotting
seasonal_rentals_df.columns = ["casual_sum", "registered_sum", "total_sum"]
seasonal_rentals_df.reset_index(inplace=True)

# Membuat label musim
season_labels = ["Spring", "Summer", "Fall", "Winter"]

# Membuat grafik dengan matplotlib
fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    seasonal_rentals_df["season"],
    seasonal_rentals_df["total_sum"],
    color="#90CAF9"
)

# Menambahkan judul dan label sumbu
ax.set_title("Total Rental Amount by Season", fontsize=24, pad=20)
ax.set_ylabel("Total Rental Amount", fontsize=18, labelpad=10)

# Mengatur label sumbu X sesuai dengan season_labels
ax.set_xticks(seasonal_rentals_df["season"])
ax.set_xticklabels(season_labels, fontsize=18)

# Tampilkan grafik di Streamlit
st.pyplot(fig)
