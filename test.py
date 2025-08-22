import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/lck_sample.csv")

st.title("🎮 LCK Sample Dashboard")
st.dataframe(df)

fig = px.bar(df, x="Player", y="KDA", color="Team", title="선수별 KDA")
st.plotly_chart(fig)
