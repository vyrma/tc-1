import streamlit as st
import plotly.express as px

def pie_chart(key, title, accuracy, description):
    accuracy = accuracy
    data = {'Category': ['Correct', 'Incorrect'], 'Value': [accuracy, 1 - accuracy]}
    fig = px.pie(data, values='Value', names='Category', title = title,
             color_discrete_sequence =['#66b3ff', '#ff9999'])
    return st.plotly_chart(fig, use_container_width=True, theme="streamlit", key=key)