import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("children_anemia_with_cities.csv")
df = df.rename(columns={
    'Type of place of residence': 'Residence',
    'Highest educational level': 'Education_Level',
    'Wealth index combined': 'Wealth',
    'Age in 5-year groups': 'Age_Group',
    'Age of respondent at 1st birth': 'Age_First_Birth',
    'Smokes cigarettes': 'Smoking',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Anemia level': 'Anemia_Level',
    'Current marital status': 'Marital_Status'
})

# Drop rows with missing key values
df = df[df['Anemia_Level'].notna() & df['latitude'].notna() & df['longitude'].notna()]

# Page configuration and style
st.set_page_config(page_title="Anemia Dashboard", layout="wide")
st.markdown("""
<style>
.block-container { padding-top: 0.2rem; padding-bottom: 0rem; }
.stTitle { margin-bottom: 0.3rem; font-size: 1.8rem; }
.element-container { margin-bottom: 0.1rem; }
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

st.title("\U0001F9B8\u200D\u2640\uFE0F Child Anemia Dashboard")

# Sidebar Filters
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

# Row 1: Map + Boxplot
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    map_fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", color="Anemia_Level",
                                color_discrete_map=color_map, zoom=5,
                                mapbox_style="open-street-map",
                                title="Geographic Distribution of Anemia")
    st.plotly_chart(map_fig, use_container_width=True)

with col2:
    fig2 = px.box(filtered_df, x="Wealth", y="Age_First_Birth", color="Anemia_Level",
                  color_discrete_map=color_map,
                  title="Mother's Age at First Birth by Wealth Index")
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Pie Chart + Education Bar Plot
col3, col4 = st.columns([1, 1], gap="small")
with col3:
    sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not sub_df.empty:
        pie_fig = px.pie(sub_df, names='Anemia_Level', hole=0.4, color='Anemia_Level',
                         color_discrete_map=color_map, title='Anemia in Children Without Iron Supplements')
        st.plotly_chart(pie_fig, use_container_width=True, config={'displayModeBar': False})

with col4:
    edu_group = filtered_df.groupby("Education_Level")["Anemia_Level"].value_counts(normalize=True).rename("Proportion").reset_index()
    fig4 = px.bar(edu_group, x="Education_Level", y="Proportion", color="Anemia_Level", barmode="group",
                  title="Proportion of Anemia by Mother's Education", color_discrete_map=color_map)
    st.plotly_chart(fig4, use_container_width=True)
