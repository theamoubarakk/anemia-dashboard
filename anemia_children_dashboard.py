import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Child Anemia Dashboard", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        .block-container { padding-top: 0.1rem; padding-bottom: 0.1rem; }
        .stSidebar { background-color: #FAFAFA; }
        .stRadio > div { flex-direction: column; }
        h2, h3, h4, h5, h6 { margin-top: 0rem; margin-bottom: 0.2rem; font-size: 1rem !important; }
        .stCaption { font-size: 0.9rem !important; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🩸‍ Child Anemia Dashboard ⚕️")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Final_Children_Anemia_Adjusted.csv"")
    df["Anemia level"] = df["Anemia level"].str.strip()
    df["Anemia level.1"] = df["Anemia level.1"].str.strip()
    df["Anemia_Level"] = df["Anemia level"].combine_first(df["Anemia level.1"])
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
residence = st.sidebar.radio("Select Residence", df["Type of place of residence"].unique())
age_group = st.sidebar.radio("Select Age Group", sorted(df["Age in 5-year groups"].unique()))
wealth = st.sidebar.radio("Select Wealth Index", sorted(df["Wealth index combined"].unique()))
iron_supp = st.sidebar.radio("Taking Iron Supplements", df["Taking iron pills, sprinkles or syrup"].unique())

# --- Apply Filters ---
filtered_df = df[
    (df["Type of place of residence"] == residence) &
    (df["Age in 5-year groups"] == age_group) &
    (df["Wealth index combined"] == wealth) &
    (df["Taking iron pills, sprinkles or syrup"] == iron_supp)
]

color_map = {
    "Not anemic": "#4F83C1",   # Softer Steel Blue (refined)
    "Mild": "#9B4F96",         # Plum
    "Moderate": "#B22222"      # Firebrick Red
}



# ============ CHARTS ==============

# --- First Row ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📍 Geographic Distribution of Anemia**")
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        color="Anemia_Level",
        color_discrete_map=color_map,
        hover_data=["City", "Anemia_Level"],
        zoom=5,
        height=280
    )
    fig_map.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.markdown("**👩‍🍼 Mother's Age at First Birth by Wealth Index**")
    fig_box = px.box(
        filtered_df,
        x="Wealth index combined",
        y="Age of respondent at 1st birth",
        color="Anemia_Level",
        color_discrete_map=color_map,
        points="all",
        height=280
    )
    st.plotly_chart(fig_box, use_container_width=True)


# --- Second Row ---
col3, col4 = st.columns(2)

# --- Second Row ---
col3, col4 = st.columns(2)

with col3:
    st.markdown("**💊 Child Anemia by Mother's Iron Supplement Intake**")
    
    iron_group = (
        df[df["Taking iron pills, sprinkles or syrup"].isin(["Yes", "No"])]
        .groupby("Taking iron pills, sprinkles or syrup")["Anemia_Level"]
        .value_counts(normalize=True)
        .rename("Proportion")
        .reset_index()
    )

    fig_iron = px.bar(
        iron_group,
        x="Taking iron pills, sprinkles or syrup",
        y="Proportion",
        color="Anemia_Level",
        color_discrete_map=color_map,
        barmode="stack",
        height=290
    )

    st.plotly_chart(fig_iron, use_container_width=True)


with col4:
    st.markdown("**🎓 Proportion of Anemia by Mother's Education**")
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
        height=290
    )
    st.plotly_chart(fig_edu, use_container_width=True)
