import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("children_anemia_with_cities.csv")
df = df.rename(columns={
    'Highest educational level': 'Education_Level',
    'Anemia level': 'Anemia_Level',
    'Hemoglobin level adjusted for altitude (g/dl - 1 decimal)': 'Hemoglobin',
    'Type of place of residence': 'Residence',
    'Age in 5-year groups': 'Age_Group',
    'Wealth index combined': 'Wealth',
    'Current marital status': 'Marital_Status',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Smokes cigarettes': 'Smoking',
    'Age at first birth': 'Age_First_Birth',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'Region': 'Region'
})
df = df[df["Anemia_Level"].notna() & df["Latitude"].notna() & df["Longitude"].notna()]

# Page layout configuration
st.set_page_config(page_title="Child Anemia Dashboard", layout="wide")

# Color map
color_map = {
    'Not anemic': '#1f77b4',
    'Mild': '#d62728',
    'Moderate': '#9467bd',
    'Severe': '#17becf'
}

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    selected_residence = st.radio("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.radio("Select Wealth Index", sorted(df["Wealth"].dropna().unique()))
    selected_marital = st.radio("Select Marital Status", df["Marital_Status"].dropna().unique())

# Apply filters
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Dashboard title
st.title("🩸 Child Anemia Dashboard")

# First row: Map + Box plot
col1, col2 = st.columns([1, 1])
with col1:
    map_fig = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        color="Anemia_Level",
        mapbox_style="carto-positron",
        zoom=5,
        color_discrete_map=color_map,
        title="Geographic Distribution of Anemia"
    )
    st.plotly_chart(map_fig, use_container_width=True)

with col2:
    fig2 = px.box(filtered_df, x="Wealth", y="Age_First_Birth", color="Anemia_Level",
                  title="Mother's Age at First Birth by Wealth Index",
                  color_discrete_map=color_map)
    st.plotly_chart(fig2, use_container_width=True)

# Second row: Pie + Education-level grouped bar
col3, col4 = st.columns([1, 1])
with col3:
    sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not sub_df.empty:
        pie_fig = px.pie(sub_df, names='Anemia_Level', hole=0.4, color='Anemia_Level',
                         color_discrete_map=color_map, title='Anemia in Children Without Iron Supplements')
        st.plotly_chart(pie_fig, use_container_width=True)

with col4:
    edu_group = filtered_df.groupby("Education_Level")["Anemia_Level"].value_counts(normalize=True).rename("Proportion").reset_index()
    fig4 = px.bar(edu_group, x="Education_Level", y="Proportion", color="Anemia_Level",
                  barmode="group", title="Proportion of Anemia by Mother's Education",
                  color_discrete_map=color_map)
    st.plotly_chart(fig4, use_container_width=True)
