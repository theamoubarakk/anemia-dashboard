import streamlit as st
import pandas as pd
import plotly.express as px



df = df[df["Anemia_Level"].notna()]

st.set_page_config(page_title="Children's Anemia Dashboard", layout="wide")
st.title("🩸 Childhood Anemia Risk Factors Dashboard")

# First row: Diverse visual types
col1, col2, col3 = st.columns(3)
with col1:
    fig1 = px.pie(df, names='Education', title="Education Distribution of Mothers")
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.box(df, x='Wealth', y='Hemoglobin', color='Anemia_Level', title="Hemoglobin Levels by Wealth")
    st.plotly_chart(fig2, use_container_width=True)
with col3:
    fig3 = px.violin(df, y='Hemoglobin', x='Residence', color='Anemia_Level', box=True, points='all', title="Hemoglobin by Residence")
    st.plotly_chart(fig3, use_container_width=True)

# Second row: More diversity
col4, col5, col6 = st.columns(3)
with col4:
    fig4 = px.histogram(df, x='Iron_Intake', color='Anemia_Level', barmode='group', title="Anemia by Iron Supplement Intake")
    st.plotly_chart(fig4, use_container_width=True)
with col5:
    top_bf = df['Breastfeed_Timing'].value_counts().nlargest(5).index
    bf_df = df[df['Breastfeed_Timing'].isin(top_bf)]
    fig5 = px.bar(bf_df, x='Breastfeed_Timing', color='Anemia_Level', title="Anemia by Breastfeeding Timing")
    st.plotly_chart(fig5, use_container_width=True)
with col6:
    fig6 = px.scatter(df, x='Hemoglobin', y='Age_Group', color='Anemia_Level', title="Hemoglobin vs Age Group by Anemia Level")
    st.plotly_chart(fig6, use_container_width=True)
