import streamlit as st
import pandas as pd
import plotly.express as px

# --- DATA LOADING & CLEANING (No changes here) ---
# It's good practice to wrap this in a cached function to improve performance
@st.cache_data
def load_data():
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
    return df

df = load_data()


# --- PAGE CONFIGURATION & STYLING ---
st.set_page_config(page_title="Anemia Dashboard", layout="wide")

# Simplified CSS - The problematic "position: fixed" rule has been removed.
st.markdown("""
    <style>
        .block-container { 
            padding-top: 2rem; 
            padding-bottom: 2rem; 
        }
        .stTitle { 
            font-size: 2.5rem; 
        }
    </style>
""", unsafe_allow_html=True)


# --- SIDEBAR FILTERS (Your implementation was already correct) ---
with st.sidebar:
    st.header("Filters")
    selected_residence = st.selectbox("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.selectbox("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.selectbox("Select Wealth Level", df["Wealth"].dropna().unique())
    selected_marital = st.selectbox("Marital Status", df["Marital_Status"].dropna().unique())


# --- MAIN PAGE ---
st.title("🩸 Childhood Anemia Dashboard")

# Filter data based on sidebar selections
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Check if the filtered dataframe is empty to avoid errors
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
else:
    # Custom color palette for consistency
    color_map = {
        'Not anemic': '#1f77b4',   # Blue
        'Mild': '#d62728',         # Red
        'Moderate': '#9467bd',     # Purple
        'Severe': '#17becf'        # Light Blue
    }

    # Row 1: Mother's Education Bar + Hemoglobin Box
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.subheader("Anemia by Mother's Education")
        fig1 = px.bar(filtered_df, x="Education", color="Anemia_Level", barmode="group",
                      color_discrete_map=color_map)
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Hemoglobin by Wealth")
        fig2 = px.box(filtered_df, x="Wealth", y="Hemoglobin", color="Anemia_Level",
                      color_discrete_map=color_map)
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2: Iron Intake Pie Charts + Smoking Histogram
    col3, col4 = st.columns(2, gap="medium")
    with col3:
        st.subheader("Anemia Levels (No Iron Intake)")
        sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
        if not sub_df.empty:
            pie_fig = px.pie(sub_df, names='Anemia_Level', hole=0.4, 
                             color='Anemia_Level', color_discrete_map=color_map)
            pie_fig.update_layout(height=400, showlegend=True)
            st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.info("No data for 'No Iron Intake' with current filters.")
            
    with col4:
        st.subheader("Hemoglobin by Smoking Status")
        fig4 = px.histogram(filtered_df, x='Hemoglobin', facet_col='Smoking', color='Anemia_Level',
                            color_discrete_map=color_map)
        fig4.update_layout(height=400)
        st.plotly_chart(fig4, use_container_width=True)
