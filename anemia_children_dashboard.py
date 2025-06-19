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
    'Have mosquito bed net for sleeping (from household questionnaire)': 'Bed_Net',
    'When child put to breast': 'Breastfeed_Timing'
})

df = df[df["Anemia_Level"].notna()]

st.set_page_config(page_title="Children's Anemia Dashboard", layout="wide")
st.title("🩸 Childhood Anemia Dashboard")

# Filter selector
res_filter = st.selectbox("Select Residence Type", options=df["Residence"].dropna().unique())
filtered_df = df[df["Residence"] == res_filter]

# Plot 1: Education Pie Chart
col1, col2 = st.columns(2)
with col1:
    fig1 = px.pie(filtered_df, names='Education', title="Education Distribution of Mothers")
    st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Iron Supplement Histogram
with col2:
    fig4 = px.histogram(filtered_df, x='Iron_Intake', color='Anemia_Level', barmode='group', title="Anemia by Iron Supplement Intake")
    st.plotly_chart(fig4, use_container_width=True)

# Plot 3: Breastfeeding Bar Plot
col3, col4 = st.columns(2)
with col3:
    top_bf = filtered_df['Breastfeed_Timing'].value_counts().nlargest(5).index
    bf_df = filtered_df[filtered_df['Breastfeed_Timing'].isin(top_bf)]
    fig5 = px.bar(bf_df, x='Breastfeed_Timing', color='Anemia_Level', title="Anemia by Breastfeeding Timing")
    st.plotly_chart(fig5, use_container_width=True)

# Plot 4: Hemoglobin Scatter Plot
with col4:
    fig6 = px.scatter(filtered_df, x='Hemoglobin', y='Age_Group', color='Anemia_Level', title="Hemoglobin vs Age Group by Anemia Level")
    st.plotly_chart(fig6, use_container_width=True)
