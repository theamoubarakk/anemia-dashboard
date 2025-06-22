import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Child Anemia Dashboard", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        .block-container { padding-top: 0.2rem; padding-bottom: 0.2rem; }
        .stSidebar { background-color: #FAFAFA; }
        .stRadio > div { flex-direction: column; }
        .stPlotlyChart { height: 250px !important; }
        .css-1kyxreq { padding-top: 0rem; padding-bottom: 0rem; }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data

def load_data():
    df = pd.read_csv("Children_Anemia_with_Location.csv")
    df["Anemia level"] = df["Anemia level"].str.strip()
    df["Anemia level.1"] = df["Anemia level.1"].str.strip()
    df["Anemia_Level"] = df["Anemia level"].combine_first(df["Anemia level.1"])
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
residence = st.sidebar.radio("Select Residence", df["Type of place of residence"].unique())
age_group = st.sidebar.radio("Select Age Group", sorted(df["Age in 5-year groups"].unique()))
wealth = st.sidebar.selectbox("Select Wealth Index", sorted(df["Wealth index combined"].unique()))
iron_supp = st.sidebar.radio("Taking Iron Supplements", df["Taking iron pills, sprinkles or syrup"].unique())

# --- Apply Filters ---
filtered_df = df[
    (df["Type of place of residence"] == residence) &
    (df["Age in 5-year groups"] == age_group) &
    (df["Wealth index combined"] == wealth) &
    (df["Taking iron pills, sprinkles or syrup"] == iron_supp)
]

# --- Color Map for Anemia Level ---
color_map = {
    "Not anemic": "#1A237E",
    "Mild": "#FFC107",
    "Moderate": "#F44336"
}

# =======================
#        Charts
# =======================

# --- Layout in a Single Row (2x2 grid compressed vertically) ---
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Map Chart
with col1:
    st.markdown("<h6 style='text-align: center;'>Geographic</h6>", unsafe_allow_html=True)
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        color="Anemia_Level",
        color_discrete_map=color_map,
        hover_data=["City", "Anemia_Level"],
        zoom=5,
        height=220
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

# Box Plot
with col2:
    st.markdown("<h6 style='text-align: center;'>Age at Birth vs Wealth</h6>", unsafe_allow_html=True)
    fig_box = px.box(
        filtered_df,
        x="Wealth index combined",
        y="Age of respondent at 1st birth",
        color="Anemia_Level",
        color_discrete_map=color_map,
        points="all",
        height=220
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Histogram (Iron supplements)
with col3:
    st.markdown("<h6 style='text-align: center;'>No Supplements</h6>", unsafe_allow_html=True)
    fig_iron = px.histogram(
        filtered_df[filtered_df["Taking iron pills, sprinkles or syrup"] == "No"],
        x="Anemia_Level",
        color="Anemia_Level",
        color_discrete_map=color_map,
        height=220
    )
    st.plotly_chart(fig_iron, use_container_width=True)

# Proportion Bar
with col4:
    st.markdown("<h6 style='text-align: center;'>By Mother's Education</h6>", unsafe_allow_html=True)
    df_edu = filtered_df.groupby(["Highest educational level", "Anemia_Level"]).size().reset_index(name="count")
    df_total = df_edu.groupby("Highest educational level")["count"].transform("sum")
    df_edu["Proportion"] = df_edu["count"] / df_total
    fig_edu = px.bar(
        df_edu,
        x="Highest educational level",
        y="Proportion",
        color="Anemia_Level",
        color_discrete_map=color_map,
        barmode="stack",
        height=220
    )
    st.plotly_chart(fig_edu, use_container_width=True)
