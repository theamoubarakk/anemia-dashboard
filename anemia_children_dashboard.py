import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("children_anemia_with_cities.csv")
df = df.rename(columns={
    'Type of place of residence': 'Residence',
    'Highest educational level': 'Education_Level',
    'Wealth index combined': 'Wealth',
    'Age in 5-year groups': 'Age_Group',
    'Age of respondent at 1st birth': 'Age_First_Birth',
    'Smokes cigarettes': 'Smoking',
    'Taking iron pills, sprinkles or syrup': 'Iron_Intake',
    'Had fever in last two weeks': 'Fever',
    'Anemia level': 'Anemia_Level'
})
df = df[df['Anemia_Level'].notna() & df['latitude'].notna() & df['longitude'].notna()]

# Streamlit settings
st.set_page_config(page_title="Anemia Dashboard", layout="wide")
st.markdown("""
<style>
.block-container { padding-top: 0.2rem; padding-bottom: 0rem; }
.stPlotlyChart { padding: 0rem !important; margin: 0rem !important; }
section[data-testid="stSidebar"] { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("🩸 Child Anemia Dashboard")

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    selected_residence = st.radio("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.radio("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.radio("Select Wealth Index", sorted(df["Wealth"].dropna().unique()))

# Filtered data
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth)
]

# Color map
color_map = {
    'Not anemic': '#1f77b4',
    'Mild': '#d62728',
    'Moderate': '#9467bd',
    'Severe': '#17becf'
}

# Top row: Map + Boxplot
top1, top2 = st.columns(2)
with top1:
    fig_map = px.scatter_mapbox(filtered_df,
        lat='latitude', lon='longitude', color='Anemia_Level',
        color_discrete_map=color_map,
        zoom=5, mapbox_style="carto-positron", height=300,
        title='Geographic Distribution of Anemia'
    )
    st.plotly_chart(fig_map, use_container_width=True)

with top2:
    fig_box = px.box(filtered_df, x='Wealth', y='Age_First_Birth', color='Anemia_Level',
                     color_discrete_map=color_map,
                     title="Mother's Age at First Birth by Wealth Index", height=300)
    st.plotly_chart(fig_box, use_container_width=True)

# Bottom row: Pie + Histogram
bot1, bot2 = st.columns(2)
with bot1:
    no_iron_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
    if not no_iron_df.empty:
        pie = px.pie(no_iron_df, names='Anemia_Level', hole=0.4,
                     color='Anemia_Level', color_discrete_map=color_map,
                     title="Anemia in Children Without Iron Supplements", height=300)
        st.plotly_chart(pie, use_container_width=True)

with bot2:
    fig_hist = px.histogram(filtered_df, x="Age_First_Birth", color="Anemia_Level",
                            facet_col="Smoking", color_discrete_map=color_map,
                            title="Anemia Levels by Smoking and Age at First Birth", height=300)
    st.plotly_chart(fig_hist, use_container_width=True)
