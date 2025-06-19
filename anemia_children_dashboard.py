import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
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

# Drop missing anemia values
df = df[df["Anemia_Level"].notna()]

st.set_page_config(page_title="Children's Anemia Dashboard", layout="wide")
st.title("🩸 Children's Anemia Analysis")

# Top row: Education, Wealth, Residence
t1, t2, t3 = st.columns(3)
with t1:
    fig1 = px.histogram(df, x='Education', color='Anemia_Level', barmode='group', title="Anemia by Mother's Education")
    st.plotly_chart(fig1, use_container_width=True)
with t2:
    fig2 = px.histogram(df, x='Wealth', color='Anemia_Level', barmode='group', title="Anemia by Wealth Index")
    st.plotly_chart(fig2, use_container_width=True)
with t3:
    fig3 = px.histogram(df, x='Residence', color='Anemia_Level', barmode='group', title="Anemia by Place of Residence")
    st.plotly_chart(fig3, use_container_width=True)

# Middle row: Iron intake, Breastfeeding, Hemoglobin
t4, t5, t6 = st.columns(3)
with t4:
    fig4 = px.histogram(df, x='Iron_Intake', color='Anemia_Level', barmode='group', title="Anemia vs Iron Intake")
    st.plotly_chart(fig4, use_container_width=True)
with t5:
    top_bf = df['Breastfeed_Timing'].value_counts().nlargest(5).index
    bf_df = df[df['Breastfeed_Timing'].isin(top_bf)]
    fig5 = px.histogram(bf_df, x='Breastfeed_Timing', color='Anemia_Level', barmode='group', title="Anemia vs Breastfeeding Time")
    st.plotly_chart(fig5, use_container_width=True)
with t6:
    fig6 = px.histogram(df, x='Hemoglobin', color='Anemia_Level', nbins=20, title="Hemoglobin by Anemia Level")
    st.plotly_chart(fig6, use_container_width=True)
