import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def ubahKeNumeric(x):
    for col in x.columns[1:]:
        x[col] = pd.to_numeric(x[col], errors='coerce')
    return x

def isiNilaiNull(x):
    x[x.select_dtypes(include="number").columns] = x.select_dtypes(include="number").apply(lambda x: x.fillna(x.mean()))
    return x

def ubahKeString(x):
    x[x.select_dtypes(include="number").columns] = x.select_dtypes(include="number").astype(str)
    return x

def filterNullValues(df):
    df = ubahKeNumeric(df)
    df = isiNilaiNull(df)
    df = ubahKeString(df)
    return df

def getReportType(name):
    df = pd.read_csv('tourism_data_transformed.csv')
    df_filtered = df[df["Report Type"] == name]
    metric = df_filtered["Metric"].unique()
    df_filtered = df_filtered[df_filtered["Country"] == 'INDONESIA']
    df_filtered = df_filtered.drop(['Country', 'Report Type', 'Subcategory', 'Category'], axis=1)
    df_filtered_pivot = df_filtered.pivot(index="Year", columns="Metric", values="Total")
    df_filtered_pivot.reset_index(inplace=True)
    if df_filtered_pivot.isnull().values.any():
        df_filtered_pivot = filterNullValues(df_filtered_pivot)
    df_filtered_melted = df_filtered_pivot.melt(id_vars=["Year"], var_name="Metric", value_name="Total_Count")
    return metric, df_filtered_melted



col1, col2 = st.columns(2)

with col1:
    inbound_metric, inbound_tourism_transport = getReportType('Inbound Tourism-Transport')
    fig_inbound_tourism_transport = px.bar(
        inbound_tourism_transport, x="Year", y="Total_Count", color="Metric",
        title="Inbound Tourism-Transport in Indonesia",
        labels={"Total_Count": "Total Count", "Year": "Year", "Metric": "Metric"})
    fig_inbound_tourism_transport.update_layout(width=500, height=400, legend_orientation="h", legend_y=-0.3)
    st.plotly_chart(fig_inbound_tourism_transport, use_container_width=True)

    domestic_tourism_trips_metric, domestic_tourism_trips = getReportType('Domestic Tourism-Trips')
    fig_domestic_tourism_trips = px.line(
        domestic_tourism_trips, x="Year", y="Total_Count", color="Metric",
        title="Domestic Tourism-Trips in Indonesia",
        labels={"Total_Count": "Total Count", "Year": "Year", "Metric": "Metric"})
    fig_domestic_tourism_trips.update_layout(width=500, height=400, legend_orientation="h", legend_y=-0.3)
    st.plotly_chart(fig_domestic_tourism_trips, use_container_width=True)

with col2:
    inbound_tourism_expenditure_metric, inbound_tourism_expenditure = getReportType('Inbound Tourism-Expenditure')
    fig_inbound_tourism_expenditure = px.line(
        inbound_tourism_expenditure, x="Year", y="Total_Count", color="Metric",
        title="Inbound Tourism-Expenditure in Indonesia",
        labels={"Total_Count": "Total Count", "Year": "Year", "Metric": "Metric"})
    fig_inbound_tourism_expenditure.update_layout(width=500, height=400, legend_orientation="h", legend_y=-0.3)
    st.plotly_chart(fig_inbound_tourism_expenditure, use_container_width=True)

    outbound_tourism_expenditure_metric, outbound_tourism_expenditure = getReportType('Outbound Tourism-Expenditure')
    fig_outbound_tourism_expenditure = px.line(
        outbound_tourism_expenditure, x="Year", y="Total_Count", color="Metric",
        title="Outbound Tourism-Expenditure in Indonesia",
        labels={"Total_Count": "Total Count", "Year": "Year", "Metric": "Metric"})
    fig_outbound_tourism_expenditure.update_layout(width=500, height=400, legend_orientation="h", legend_y=-0.3)
    st.plotly_chart(fig_outbound_tourism_expenditure, use_container_width=True)

employment_metric, employment = getReportType('Employment')
fig_employment = px.bar(
    employment, x="Year", y="Total_Count", color="Metric",
    title="Employment in Indonesia",
    labels={"Total_Count": "Total Count", "Year": "Year", "Metric": "Metric"})
fig_employment.update_layout(width=1000, height=400, legend_orientation="h", legend_y=-0.15)
st.plotly_chart(fig_employment, use_container_width=True)


# with st.sidebar:
#     st.header(":blue[Report Type]")
#     type = st.radio("Please Select Report Type", report_types, index=None)
#     if type:
#         # Filter data berdasarkan Report Type yang dipilih
#         filtered_df = df[df["Report Type"] == type]

#         # Ambil nilai unik dari Subcategory & Metric
#         unique_subcategories = filtered_df["Subcategory"].unique()
#         unique_metrics = filtered_df["Metric"].unique()

#         st.write(unique_subcategories)
#         st.write(unique_metrics)
#         # # Multiselect untuk memilih Subcategory
#         # selected_subcategories = st.selectbox("Pilih Subcategory:", unique_subcategories)

#         # Multiselect untuk memilih Metric
#         selected_metrics = st.multiselect("Pilih Metric:", unique_metrics)
#         show = st.button("Show Data")

# st.title("UNWTO Tourism Data")


# if type:
#     st.write(f"## {type}")
#     if show:
#         show_df = filtered_df[
#             (filtered_df["Metric"].isin(selected_metrics)) 
#             & (filtered_df["Country"] == "INDONESIA")
#         ]

#         show_df = show_df.drop(['Country', 'Report Type', 'Subcategory', 'Category'], axis=1)
#         st.write(show_df)

#         # Gunakan pivot untuk mengubah 'Metric' menjadi kolom baru
#         df_pivot = show_df.pivot(index="Year", columns="Metric", values="Total")
#         st.write(df_pivot)

#         # Reset index agar "Year" kembali menjadi kolom dan mengisi nilai kosong dengan mean
#         df_pivot.reset_index(inplace=True)
#         df_pivot.fillna(df_pivot.mean(), inplace=True)
#         st.write(df_pivot)

#         # Ubah DataFrame ke format long (melt) untuk plot dengan warna berdasarkan Metric
#         df_melted = df_pivot.melt(id_vars=["Year"], var_name="Metric", value_name="Total_Count")
#         st.write(df_melted)

#         # Buat Line Plot dengan Plotly Express
#         fig = px.line(
#             df_melted, x="Year", y="Total_Count", color="Metric",
#             title="Data in Indonesia",
#             labels={"Total_Count": "Total Count", "Year": "Year", "Metric": "Subcategory"},
#             markers=True)

#         # Tampilkan plot di Streamlit
#         st.plotly_chart(fig)
        
# else:
#     st.write("Belum ada Report Type yang dipilih.")