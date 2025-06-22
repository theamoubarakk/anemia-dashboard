import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("children_anemia_with_cities.csv")

# Clean and rename columns
df = df.rename(columns={
    'Age in 5-year groups': 'Age_Group',
    'Type of place of residence': 'Residence',
    'Highest educational level': 'Education_Level',
    'Wealth index combined': 'Wealth_Index',
    'Hemoglobin level adjusted for altitude (g/dl - 1 decimal)': 'Hemoglobin',
    'Anemia level.1': 'Anemia_Level',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Smokes cigarettes': 'Smoking',
    'Current marital status': 'Marital_Status',
    'Age of respondent at 1st birth': 'Age_First_Birth'
})

df = df[df['Anemia_Level'].notna() & df['latitude'].notna() & df['longitude'].notna()]

# Streamlit config
st.set_page_config(page_title="Anemia Map Dashboard", layout="wide")

st.title("🩸 Child Anemia Dashboard")

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    selected_res = st.radio("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.radio("Select Wealth Index", sorted(df["Wealth_Index"].dropna().unique()))

# Apply filters
filtered_df = df[
    (df["Residence"] == selected_res) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth_Index"] == selected_wealth)
]

# Color mapping
color_map = {
    'Not anemic': '#1f77b4',
    'Mild': '#d62728',
    'Moderate': '#9467bd',
    'Severe': '#17becf'
}

# Layout - 2 rows of 2 columns (fit in 1 screen)
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="latitude", lon="longitude",
        color="Anemia_Level",
        color_discrete_map=color_map,
        zoom=5,
        height=300,
        mapbox_style="carto-positron",
        title="Geographic Distribution of Anemia"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    fig_box = px.box(
        filtered_df,
        x="Wealth_Index", y="Age_First_Birth",
        color="Anemia_Level",
        color_discrete_map=color_map,
        title="Mother's Age at First Birth by Wealth Index"
    )
    st.plotly_chart(fig_box, use_container_width=True)

col3, col4 = st.columns([1, 1], gap="small")
with col3:
    sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not sub_df.empty:
        pie_fig = px.pie(
            sub_df,
            names='Anemia_Level',
            hole=0.4,
            color='Anemia_Level',
            color_discrete_map=color_map,
            title='Anemia in Children Without Iron Supplements'
        )
        st.plotly_chart(pie_fig, use_container_width=True)

with col4:
    fig_hist = px.histogram(
        filtered_df,
        x='Age_First_Birth',
        facet_col='Smoking',
        color='Anemia_Level',
        color_discrete_map=color_map,
        title='Anemia Levels by Smoking and Age at First Birth'
    )
    st.plotly_chart(fig_hist, use_container_width=True)
