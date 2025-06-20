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
section[data-testid="stSidebar"] div[class^="css"] {
    position: fixed;
    top: 0rem;
    left: 0;
    height: 100%;
    overflow-y: hidden;
    background: #f5f5f5;
    border-right: 1px solid #ddd;
    padding-top: 0.1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🩸 Childhood Anemia Dashboard")

# Sidebar Filters (Fixed)
with st.sidebar:
    st.header("Filters")
    selected_residence = st.radio("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.radio("Select Wealth Level", df["Wealth"].dropna().unique())
    selected_marital = st.radio("Marital Status", df["Marital_Status"].dropna().unique())

# Filter data
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Updated custom color palette
color_map = {
    'Not anemic': '#1f77b4',   # Blue
    'Mild': '#d62728',         # Red
    'Moderate': '#9467bd',     # Purple
    'Severe': '#17becf'        # Light Blue
}

# Row 1: Mother's Education Bar + Hemoglobin Box
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    fig1 = px.bar(filtered_df, x="Education", color="Anemia_Level", barmode="group",
                  color_discrete_map=color_map,
                  title="Anemia by Mother's Education", width=360, height=300)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(filtered_df, x="Wealth", y="Hemoglobin", color="Anemia_Level",
                  color_discrete_map=color_map,
                  title="Hemoglobin by Wealth", width=360, height=300)
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Iron Intake Pie Chart + Smoking Histogram
col3, col4 = st.columns([1, 1], gap="small")
with col3:
    sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not sub_df.empty:
        pie_fig = px.pie(sub_df, names='Anemia_Level', hole=0.4, color='Anemia_Level',
                         color_discrete_map=color_map, title='Anemia Levels - Iron Intake: No',
                         width=300, height=250)
        st.plotly_chart(pie_fig, use_container_width=False, config={'displayModeBar': False})

with col4:
    fig4 = px.histogram(filtered_df, x='Hemoglobin', facet_col='Smoking', color='Anemia_Level',
                        color_discrete_map=color_map,
                        title='Hemoglobin Distribution by Smoking Status', width=360, height=300)
    st.plotly_chart(fig4, use_container_width=True)
