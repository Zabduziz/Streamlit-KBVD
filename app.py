import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv('tourism_data_transformed.csv')

report_types = df['Report Type'].unique()

with st.sidebar:
    st.header(":blue[Report Type]")
    type = st.radio("Please Select Report Type", report_types, index=None)
    if type:
        # Filter data berdasarkan Report Type yang dipilih
        filtered_df = df[df["Report Type"] == type]

        # Ambil nilai unik dari Subcategory & Metric
        unique_subcategories = filtered_df["Subcategory"].unique()
        unique_metrics = filtered_df["Metric"].unique()

        # Multiselect untuk memilih Subcategory
        selected_subcategories = st.selectbox("Pilih Subcategory:", unique_subcategories)

        # Multiselect untuk memilih Metric
        selected_metrics = st.multiselect("Pilih Metric:", unique_metrics)
        show = st.button("Show Data")

st.title("UNWTO Tourism Data")


if type:
    st.write(f"## {type}")
    if show:
        show_df = filtered_df[
            (filtered_df["Subcategory"] == selected_subcategories) 
            & (filtered_df["Metric"].isin(selected_metrics)) 
            & (filtered_df["Country"] == "INDONESIA")
        ]

        show_df = show_df.drop(['Country', 'Report Type', 'Subcategory', 'Category'], axis=1)

        # Gunakan pivot untuk mengubah 'Metric' menjadi kolom baru
        df_pivot = show_df.pivot(index="Year", columns="Metric", values="Total")

        # Reset index agar "Year" kembali menjadi kolom
        df_pivot.reset_index(inplace=True)

        # Ubah DataFrame ke format long (melt) untuk plot dengan warna berdasarkan Metric
        df_melted = df_pivot.melt(id_vars=["Year"], var_name="Metric", value_name="Total_Count")

        # Buat Line Plot dengan Plotly Express
        fig = px.line(
            df_melted, x="Year", y="Total_Count", color="Metric",
            title=selected_subcategories+" in Indonesia",
            labels={"Total_Count": "Total Count", "Year": "Year", "Metric": "Subcategory"},
            markers=True)

        # Tampilkan plot di Streamlit
        st.plotly_chart(fig)
        
else:
    st.write("Belum ada Report Type yang dipilih.")