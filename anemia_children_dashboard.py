import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Child Anemia Dashboard", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        .stSidebar { background-color: #FAFAFA; }
        .stRadio > div { flex-direction: column; }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("your_cleaned_anemia_dataset.csv")  # UPDATE with your dataset name
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filters")
residence = st.sidebar.radio("Select Residence", df["Residence"].unique())
age_group = st.sidebar.radio("Select Age Group", sorted(df["Age_Group"].unique()))
wealth = st.sidebar.selectbox("Select Wealth Index", df["Wealth_Index"].unique())
iron_supp = st.sidebar.radio("Taking Iron Supplements", df["Iron_Supplements"].unique())

# --- Apply Filters ---
filtered_df = df[
    (df["Residence"] == residence) &
    (df["Age_Group"] == age_group) &
    (df["Wealth_Index"] == wealth) &
    (df["Iron_Supplements"] == iron_supp)
]

# --- Color Map for Anemia Level ---
color_map = {
    "Not anemic": "#4A90E2",
    "Mild": "#F88379",
    "Moderate": "#D0021B"
}

# =======================
#        Charts
# =======================

# --- Top Row ---
col1, col2 = st.columns(2)

# Map Chart (Replace with your real map chart)
with col1:
    st.plotly_chart(
        px.scatter_mapbox(
            filtered_df,
            lat="lat", lon="lon", zoom=5,
            color="Anemia_Level",
            color_discrete_map=color_map,
            mapbox_style="carto-positron"
        ),
        use_container_width=True
    )

# Box Plot (Age vs Wealth Index)
with col2:
    fig_box = px.box(
        filtered_df,
        x="Wealth_Index",
        y="Age_at_Birth",
        color="Anemia_Level",
        color_discrete_map=color_map,
        title="Age of Respondent at Birth by Wealth Index"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- Second Row ---
col3, col4 = st.columns(2)

# Anemia in Children Without Iron Supplements
with col3:
    st.subheader("Anemia in Children Without Iron Supplements")
    st.caption("Only among non-supplemented cases")
    fig_iron = px.histogram(
        filtered_df[filtered_df["Iron_Supplements"] == "No"],
        x="Anemia_Level",
        color="Anemia_Level",
        color_discrete_map=color_map
    )
    st.plotly_chart(fig_iron, use_container_width=True)

# Proportion of Anemia by Mother's Education
with col4:
    st.subheader("Proportion of Anemia by Mother's Education")
    df_edu = filtered_df.groupby(["Mother_Education", "Anemia_Level"]).size().reset_index(name="count")
    df_total = df_edu.groupby("Mother_Education")["count"].transform("sum")
    df_edu["Proportion"] = df_edu["count"] / df_total

    fig_edu = px.bar(
        df_edu,
        x="Mother_Education",
        y="Proportion",
        color="Anemia_Level",
        color_discrete_map=color_map,
        barmode="stack"
    )
    st.plotly_chart(fig_edu, use_container_width=True)
