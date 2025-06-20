import streamlit as st
import pandas as pd
import plotly.express as px

# --- DATA LOADING (Using cache for performance) ---
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


# --- PAGE CONFIGURATION & CSS FOR A FIXED, NON-SCROLLING LAYOUT ---
st.set_page_config(page_title="Anemia Dashboard", layout="wide")

# This CSS is the key to achieving the non-scrolling layout.
st.markdown("""
    <style>
        /* This hides the main scrollbar and locks the body */
        html, body {
            overflow: hidden;
        }
        /* This makes the main container fill the viewport height */
        .main .block-container {
            height: 95vh; /* 95% of viewport height to leave a little margin */
            overflow-y: hidden;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Hide the "Made with Streamlit" footer to save space */
        footer {
            visibility: hidden;
        }
        /* Reduce top margin of the title */
        .stTitle {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)


# --- SIDEBAR (Your original code was correct) ---
with st.sidebar:
    st.header("Filters")
    selected_residence = st.selectbox("Select Residence", df["Residence"].dropna().unique())
    selected_age = st.selectbox("Select Age Group", df["Age_Group"].dropna().unique())
    selected_wealth = st.selectbox("Select Wealth Level", df["Wealth"].dropna().unique())
    selected_marital = st.selectbox("Marital Status", df["Marital_Status"].dropna().unique())

# --- MAIN PAGE CONTENT ---

st.title("🩸 Childhood Anemia Dashboard")

# Filter data
filtered_df = df[
    (df["Residence"] == selected_residence) &
    (df["Age_Group"] == selected_age) &
    (df["Wealth"] == selected_wealth) &
    (df["Marital_Status"] == selected_marital)
]

# Custom color palette
color_map = {
    'Not anemic': '#1f77b4', 'Mild': '#d62728',
    'Moderate': '#9467bd', 'Severe': '#17becf'
}

# --- LAYOUT - RESTORING YOUR FIXED HEIGHTS ---
# The fixed height values are now CRITICAL to make everything fit.
# You may need to adjust these pixel values slightly to look perfect on your screen.

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    # Row 1
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        fig1 = px.bar(filtered_df, x="Education", color="Anemia_Level", barmode="group",
                      color_discrete_map=color_map,
                      title="Anemia by Mother's Education",
                      height=350) # Fixed height
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.box(filtered_df, x="Wealth", y="Hemoglobin", color="Anemia_Level",
                      color_discrete_map=color_map,
                      title="Hemoglobin by Wealth",
                      height=350) # Fixed height
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col3, col4 = st.columns(2, gap="medium")
    with col3:
        sub_df = filtered_df[filtered_df['Iron_Intake'] == 'No']
        if not sub_df.empty:
            pie_fig = px.pie(sub_df, names='Anemia_Level', hole=0.4, color='Anemia_Level',
                             color_discrete_map=color_map,
                             title='Anemia Levels - Iron Intake: No',
                             height=350) # Fixed height
            st.plotly_chart(pie_fig, use_container_width=True)
        else:
            st.info("No data for 'No Iron Intake' with current filters.")

    with col4:
        fig4 = px.histogram(filtered_df, x='Hemoglobin', facet_col='Smoking', color='Anemia_Level',
                            color_discrete_map=color_map,
                            title='Hemoglobin Distribution by Smoking Status',
                            height=350) # Fixed height
        st.plotly_chart(fig4, use_container_width=True)
