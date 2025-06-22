import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("Children_Anemia_with_Location.csv")

# Standardize anemia column
df["Anemia level"] = df["Anemia level"].str.strip()
df["Anemia level.1"] = df["Anemia level.1"].str.strip()
df["Anemia_Level"] = df["Anemia level"].combine_first(df["Anemia level.1"])

# Color mapping
anemia_color_map = {
    "Moderate": "#F44336",
    "Mild": "#FFC107",
    "Not anemic": "#1A237E"
}

# Sidebar Filters
st.sidebar.header("Filters")
residence = st.sidebar.radio("Select Residence", df["Type of place of residence"].unique())
age_group = st.sidebar.radio("Select Age Group", df["Age in 5-year groups"].unique())
wealth = st.sidebar.selectbox("Select Wealth Index", sorted(df["Wealth index combined"].unique()))
supplement = st.sidebar.radio("Taking Iron Supplements", df["Taking iron pills, sprinkles or syrup"].unique())

# Apply filters
filtered = df[
    (df["Type of place of residence"] == residence) &
    (df["Age in 5-year groups"] == age_group) &
    (df["Wealth index combined"] == wealth) &
    (df["Taking iron pills, sprinkles or syrup"] == supplement)
]

st.set_page_config(layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>🩸 Child Anemia Dashboard </h1>
""", unsafe_allow_html=True)

# Layout in 2 columns (no scroll layout)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Geographic Distribution of Anemia")
    fig_map = px.scatter_mapbox(
        filtered,
        lat="Latitude",
        lon="Longitude",
        color="Anemia_Level",
        color_discrete_map=anemia_color_map,
        hover_data=["City", "Anemia_Level"],
        zoom=5,
        height=400
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("Mother's Age at First Birth by Wealth Index")
    fig_box = px.box(
        filtered,
        x="Wealth index combined",
        y="Age of respondent at 1st birth",
        color="Anemia_Level",
        color_discrete_map=anemia_color_map,
        points="all"
    )
    st.plotly_chart(fig_box, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Anemia in Children Without Iron Supplements")
    without_iron = filtered[filtered["Taking iron pills, sprinkles or syrup"] == "No"]
    fig_pie = px.pie(
        without_iron,
        names="Anemia_Level",
        color="Anemia_Level",
        color_discrete_map=anemia_color_map,
        title="Only among non-supplemented cases"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("Proportion of Anemia by Mother's Education")
    edu_group = filtered.groupby("Highest educational level")["Anemia_Level"]\
        .value_counts(normalize=True).rename("Proportion").reset_index()
    fig_bar = px.bar(
        edu_group,
        x="Highest educational level",
        y="Proportion",
        color="Anemia_Level",
        barmode="group",
        color_discrete_map=anemia_color_map
    )
    st.plotly_chart(fig_bar, use_container_width=True)
