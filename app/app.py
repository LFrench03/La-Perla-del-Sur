#Dependences
import streamlit as st
import csv
import json
import pandas as pd
import numpy as np
import plotly_express as ps
import plotly.graph_objects as go


#Function to convert each dataframe to a downloadable csv
@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")

#Header
st.set_page_config(page_title="La Perla del Sur", page_icon="img/perla.jpeg", layout="centered")
st.markdown('<h1 align="center"><img src="https://readme-typing-svg.herokuapp.com?font=Righteous&size=35&center=true&vCenter=true&width=500&height=60&duration=4000&lines=La+Perla+del+Sur+⚪️;" /> </h1>',unsafe_allow_html=True)
with st.container(border=True):
    st.image(image="app/img/cienfuegos2.jpeg", use_column_width=True)
    st.markdown('<div align=center><l style="font-family: serif;font-size:20px;"><b style="color:#2ec9f0;">Análisis migratorio de la provincia de Cienfuegos. <br><l style= "color:#236d7f;">El factor determinante de la educación y la familia</l></b></l></div', unsafe_allow_html=True)
    st.divider()
    st.markdown("",unsafe_allow_html=True)





