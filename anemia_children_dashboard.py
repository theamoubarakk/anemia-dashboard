import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("children_anemia_with_cities.csv")
df = df.rename(columns={
    'Type of place of residence': 'Residence',
    'Age in 5-year groups': 'Age_Group',
    'Wealth index combined': 'Wealth',
    'Age of respondent at 1st birth': 'Age_First_Birth',
    'Smokes cigarettes': 'Smoking',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Current marital status': 'Marital_Status',
    'Anemia level': 'Anemia_Level',
    'Highest educational level': 'Education'
})
df = df[df['Anemia_Level'].notna() & df['latitude'].notna() & df['longitude'].notna()]

# Page config
st.set_page_config(page_title="Anemia Dashboard", layout="wide")
st.title("🩸\u200d Child Anemia Dashboard ⚕️")

# Sidebar Filters
with st.sidebar:
    st.header("Filters")
    selected_residence = st.radio("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.radio("Select Wealth Index", df["Wealth"].dropna().unique())
    selected_marital = st.radio("Select Marital Status", df["Marital_Status"].dropna().unique())

# Filter data
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

# Row 1: Map + Box Plot
col1, col2 = st.columns([1, 1], gap="small")
with col1:
    fig_map = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", color="Anemia_Level",
                                color_discrete_map=color_map, zoom=5, height=300,
                                title="Geographic Distribution of Anemia in Nigeria")
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    fig2 = px.box(filtered_df, x="Wealth", y="Age_First_Birth", color="Anemia_Level",
                  title="Mother's Age at First Birth by Wealth Index",
                  color_discrete_map=color_map, height=300)
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: Iron Intake Pie Chart + Education Bar Chart
col3, col4 = st.columns([1, 1], gap="small")
with col3:
    sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not sub_df.empty:
        pie_fig = px.pie(sub_df, names='Anemia_Level', hole=0.4, color='Anemia_Level',
                         color_discrete_map=color_map, title='Anemia in Children Without Iron Supplements', height=300)
        st.plotly_chart(pie_fig, use_container_width=True)

with col4:
    edu_group = filtered_df.groupby("Education")["Anemia_Level"].value_counts(normalize=True).rename("Proportion").reset_index()
    fig = px.bar(edu_group, x="Education", y="Proportion", color="Anemia_Level", barmode="group",
                 title="Proportion of Anemia by Mother's Education", color_discrete_map=color_map, height=300)
    st.plotly_chart(fig, use_container_width=True)
