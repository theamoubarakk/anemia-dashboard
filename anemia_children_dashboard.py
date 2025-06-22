import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned dataset with geolocation
df = pd.read_csv("children_anemia_with_cities.csv")

# Rename for convenience
df = df.rename(columns={
    'Type of place of residence': 'Residence',
    'Age in 5-year groups': 'Age_Group',
    'Wealth index combined': 'Wealth',
    'Highest educational level': 'Education',
    'Smokes cigarettes': 'Smoking',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Age of respondent at 1st birth': 'Age_First_Birth',
    'Anemia level': 'Anemia_Level'
})

# Page config and styling
st.set_page_config(page_title="Child Anemia Map Dashboard", layout="wide")
st.markdown("""
<style>
.block-container { padding-top: 0.2rem; padding-bottom: 0rem; }
.stTitle { margin-bottom: 0.3rem; font-size: 1.8rem; }
.row-widget.stRadio > div{ flex-direction: row; }
.stPlotlyChart { padding: 0rem !important; margin: 0rem !important; }
section[data-testid="stSidebar"] div[class^="css"] {
    position: fixed;
    top: 0rem;
    left: 0;
    height: 100vh;
    overflow-y: auto;
    background: #f5f5f5;
    border-right: 1px solid #ddd;
    padding-top: 0.1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🩸 Child Anemia Dashboard")

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    selected_res = st.radio("Select Residence", df["Residence"].unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].unique())
    selected_wealth = st.radio("Select Wealth Index", sorted(df["Wealth"].unique()))

# Filtered Data
filtered_df = df[
    (df["Residence"] == selected_res) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth)
]

color_map = {
    'Not anemic': '#1f77b4', 'Mild': '#d62728',
    'Moderate': '#9467bd', 'Severe': '#17becf'
}

# Row 1: Map + Boxplot
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    map_fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude",
                                color="Anemia_Level", zoom=5,
                                color_discrete_map=color_map,
                                mapbox_style="carto-positron",
                                title="Geographic Distribution of Anemia")
    st.plotly_chart(map_fig, use_container_width=True)

with col2:
    fig2 = px.box(filtered_df, x="Wealth", y="Age_First_Birth", color="Anemia_Level",
                  color_discrete_map=color_map,
                  title="Mother's Age at First Birth by Wealth Index")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Pie + Histogram
col3, col4 = st.columns([1, 1], gap="small")
with col3:
    no_iron_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not no_iron_df.empty:
        pie_fig = px.pie(no_iron_df, names='Anemia_Level', color='Anemia_Level',
                         color_discrete_map=color_map, hole=0.4,
                         title='Anemia in Children Without Iron Supplements')
        st.plotly_chart(pie_fig, use_container_width=True)

with col4:
    fig4 = px.histogram(filtered_df, x='Age_First_Birth', facet_col='Smoking',
                        color='Anemia_Level', color_discrete_map=color_map,
                        title='Anemia Levels by Smoking and Age at First Birth')
    st.plotly_chart(fig4, use_container_width=True)
