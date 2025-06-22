import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("children_anemia_with_cities.csv")
df = df.rename(columns={
    'Type of place of residence': 'Residence',
    'Highest educational level': 'Education',
    'Wealth index combined': 'Wealth',
    'Age in 5-year groups': 'Age_Group',
    'Age of respondent at 1st birth': 'Age_First_Birth',
    'Smokes cigarettes': 'Smoking',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Anemia level': 'Anemia_Level',
    'Current marital status': 'Marital_Status'
})
df = df[df['Anemia_Level'].notna() & df['latitude'].notna() & df['longitude'].notna()]

# Page configuration and layout
st.set_page_config(page_title="Anemia Dashboard", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 0.2rem; padding-bottom: 0rem; }
    .stPlotlyChart { margin-bottom: 0rem !important; }
    section[data-testid="stSidebar"] div[class^="css"] {
        height: 100vh; overflow-y: auto; border-right: 1px solid #ddd;
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

# Apply filters
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Color map
color_map = {
    'Not anemic': '#1f77b4',
    'Mild': '#d62728',
    'Moderate': '#9467bd',
    'Severe': '#17becf'
}

# Row 1: Map + Boxplot
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="latitude", lon="longitude",
        color="Anemia_Level",
        color_discrete_map=color_map,
        zoom=5, height=300,
        mapbox_style="open-street-map",
        title="Geographic Distribution of Anemia"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    fig_box = px.box(
        filtered_df, x="Wealth", y="Age_First_Birth", color="Anemia_Level",
        color_discrete_map=color_map,
        title="Mother's Age at First Birth by Wealth Index", height=300
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Row 2: Pie + Histogram
col3, col4 = st.columns([1, 1], gap="small")
with col3:
    sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not sub_df.empty:
        pie_fig = px.pie(
            sub_df, names='Anemia_Level', hole=0.4, color='Anemia_Level',
            color_discrete_map=color_map,
            title='Anemia in Children Without Iron Supplements', height=280
        )
        st.plotly_chart(pie_fig, use_container_width=True)

with col4:
    fig_hist = px.histogram(
        filtered_df, x='Age_First_Birth', facet_col='Smoking', color='Anemia_Level',
        color_discrete_map=color_map,
        title='Anemia Levels by Smoking and Age at First Birth', height=280
    )
    st.plotly_chart(fig_hist, use_container_width=True)
