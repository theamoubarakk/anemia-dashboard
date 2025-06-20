import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("children anemia.csv")
df = df.rename(columns={
    'Age in 5-year groups': 'Age_Group',
    'Type of place of residence': 'Residence',
    'Highest educational level': 'Education',
    'Wealth index combined': 'Wealth',
    'Hemoglobin level adjusted for altitude (g/dl - 1 decimal)': 'Hemoglobin',
    'Anemia level.1': 'Anemia_Level',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Smokes cigarettes': 'Smoking',
    'Current marital status': 'Marital_Status'
})

df = df[df['Anemia_Level'].notna()]

# Page configuration and CSS
st.set_page_config(page_title="Anemia Dashboard", layout="wide")
st.markdown("""
    <style>
        .block-container { padding-top: 0.5rem; padding-bottom: 0rem; }
        .stTitle { margin-bottom: 0.3rem; font-size: 1.8rem; }
        .element-container { margin-bottom: 0.1rem; }
        .row-widget.stRadio > div{ flex-direction: row; }
        .stPlotlyChart { padding: 0rem !important; margin: 0rem !important; }
        section[data-testid="stSidebar"] div[class^="css"] { position: fixed; top: 3rem; left: 0; height: 100%; overflow-y: auto; background: #f5f5f5; border-right: 1px solid #ddd; padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🩸 Childhood Anemia Dashboard")

# Sidebar Filters (Fixed)
with st.sidebar:
    st.header("Filters")
    selected_residence = st.selectbox("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.selectbox("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.selectbox("Select Wealth Level", df["Wealth"].dropna().unique())
    selected_marital = st.selectbox("Marital Status", df["Marital_Status"].dropna().unique())

# Filter data
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Updated color palette for better visuals
color_map = {
    'Not anemic': '#4E79A7',
    'Mild': '#F28E2B',
    'Moderate': '#E15759',
    'Severe': '#76B7B2'
}

# Row 1: Donut Chart + Education Bar Chart
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    fig1 = px.pie(filtered_df, names='Anemia_Level', hole=0.5,
                  color='Anemia_Level', color_discrete_map=color_map,
                  title="Overall Anemia Distribution", width=360, height=300)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(filtered_df, x="Education", color="Anemia_Level", barmode="group",
                  color_discrete_map=color_map,
                  title="Anemia by Mother's Education", width=360, height=300)
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Iron Intake Bar Chart + Facet Histogram
col3, col4 = st.columns([1, 1], gap="small")
with col3:
    fig3 = px.bar(filtered_df, x='Iron_Intake', color='Anemia_Level', barmode='group',
                 color_discrete_map=color_map,
                 title='Iron Supplement Intake vs Anemia Level', width=360, height=300)
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.histogram(filtered_df, x='Hemoglobin', facet_col='Smoking', color='Anemia_Level',
                        color_discrete_map=color_map,
                        title='Hemoglobin Distribution by Smoking Status', width=360, height=300)
    st.plotly_chart(fig4, use_container_width=True)
