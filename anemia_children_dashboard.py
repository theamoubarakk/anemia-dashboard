import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("children_anemia_with_cities.csv")

# Rename columns for clarity
df = df.rename(columns={
    'Type of place of residence': 'Residence',
    'Highest educational level': 'Education_Level',
    'Wealth index combined': 'Wealth',
    'Age in 5-year groups': 'Age_Group',
    'Age of respondent at 1st birth': 'Age_First_Birth',
    'Smokes cigarettes': 'Smoking',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Anemia level': 'Anemia_Level',
    'City': 'City',
    'latitude': 'Latitude',
    'longitude': 'Longitude'
})

# Drop missing rows in key columns
df = df[df["Anemia_Level"].notna() & df["Latitude"].notna() & df["Longitude"].notna()]

# Page configuration and custom style
st.set_page_config(layout="wide")
st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #f5f5f5;
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🩸 Child Anemia Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    selected_residence = st.radio("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.radio("Select Wealth Index", sorted(df["Wealth"].dropna().unique()))
    selected_marital = st.radio("Select Marital Status", df["Marital_Status"].dropna().unique())

# Filtered data
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Custom color map
color_map = {
    'Not anemic': '#1f77b4',
    'Mild': '#d62728',
    'Moderate': '#9467bd',
    'Severe': '#17becf'
}

# Row 1: Map + Box Plot
col1, col2 = st.columns([1.1, 0.9])
with col1:
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        color="Anemia_Level",
        mapbox_style="carto-positron",
        color_discrete_map=color_map,
        zoom=5,
        height=320,
        title="Geographic Distribution of Anemia"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    if not filtered_df.empty:
        fig_box = px.box(filtered_df, x="Wealth", y="Age_First_Birth", color="Anemia_Level",
                         color_discrete_map=color_map,
                         title="Mother's Age at First Birth by Wealth Index")
        st.plotly_chart(fig_box, use_container_width=True)

# Row 2: Iron Pie + Education Bar
col3, col4 = st.columns([0.9, 1.1])
with col3:
    no_iron = filtered_df[filtered_df["Iron_Intake"] == "No"]
    if not no_iron.empty:
        fig_pie = px.pie(no_iron, names="Anemia_Level", color="Anemia_Level",
                         color_discrete_map=color_map, hole=0.4,
                         title="Anemia in Children Without Iron Supplements")
        st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    edu_group = filtered_df.groupby("Education_Level")["Anemia_Level"].value_counts(normalize=True).rename("Proportion").reset_index()
    fig_edu = px.bar(edu_group, x="Education_Level", y="Proportion", color="Anemia_Level",
                     barmode="group", color_discrete_map=color_map,
                     title="Proportion of Anemia by Mother's Education")
    st.plotly_chart(fig_edu, use_container_width=True)
