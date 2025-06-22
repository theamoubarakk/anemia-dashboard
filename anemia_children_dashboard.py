import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean main dataset
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

# Load global anemia data for map
geo_df = pd.read_csv("anemia_median_income_gdp.csv")

# Page layout config
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

st.title("🩸 Child Anemia Dashboard: Exploring Maternal Links")

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    selected_residence = st.radio("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.radio("Select Wealth Level", df["Wealth"].dropna().unique())
    selected_marital = st.radio("Marital Status", df["Marital_Status"].dropna().unique())

# Apply filters
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Color palette
color_map = {
    'Not anemic': '#1f77b4',
    'Mild': '#d62728',
    'Moderate': '#9467bd',
    'Severe': '#17becf'
}

# Row 1 - Education + Hemoglobin Box
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    fig1 = px.bar(filtered_df, x="Education", color="Anemia_Level", barmode="group",
                  color_discrete_map=color_map,
                  title="Impact of Maternal Education on Child Anemia Severity", width=360, height=300)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(filtered_df, x="Wealth", y="Hemoglobin", color="Anemia_Level",
                  color_discrete_map=color_map,
                  title="Hemoglobin Levels Across Economic Status", width=360, height=300)
    st.plotly_chart(fig2, use_container_width=True)

# Row 2 - Iron Pie + Smoking Histogram
col3, col4 = st.columns([1, 1], gap="small")
with col3:
    sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not sub_df.empty:
        pie_fig = px.pie(sub_df, names='Anemia_Level', hole=0.4, color='Anemia_Level',
                         color_discrete_map=color_map,
                         title='Iron Deficiency and Anemia',
                         width=320, height=260)
        st.plotly_chart(pie_fig, use_container_width=False, config={'displayModeBar': False})

with col4:
    fig4 = px.histogram(filtered_df, x='Hemoglobin', facet_col='Smoking', color='Anemia_Level',
                        color_discrete_map=color_map,
                        title='How Maternal Smoking Relates to Child Hemoglobin Levels', width=360, height=300)
    st.plotly_chart(fig4, use_container_width=True)

# Row 3 - Global Anemia Map
col5 = st.columns(1)[0]
with col5:
    map_fig = px.choropleth(
        geo_df,
        locations="Location",
        locationmode="country names",
        color="Anemia",
        hover_name="Location",
        animation_frame="Year",
        color_continuous_scale="Reds",
        title="🌍 Global Anemia Prevalence (2019)",
    )
    map_fig.update_layout(width=700, height=340, margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(map_fig, use_container_width=True)
