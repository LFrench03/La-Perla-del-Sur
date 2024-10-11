#Dependences
import streamlit as st
from json import load
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium import Map, GeoJson, GeoJsonPopup, GeoJsonTooltip, Choropleth, LayerControl
from geopandas import read_file, GeoDataFrame
import numpy as np
import plotly_express as px
import plotly.graph_objects as go

#Function to convert each dataframe to a downloadable csv
@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")

#Function to skip initial space on csv's files
def skipinitalspace_csv(path:str):
    from csv import reader, writer
    data = []
    with open(path, "r") as f:
        reader = reader(f, skipinitialspace=True)
        for i in reader:
            data.append(i)
    with open(path, 'w') as f:
        writer = writer(f)
        writer.writerows(data)

#Page configuration
st.set_page_config(page_title="La Perla del Sur", page_icon="app/img/perla.jpeg", layout="centered")

#Header
st.markdown('<h1 align="center"><img src="https://readme-typing-svg.herokuapp.com?font=Righteous&size=35&center=true&vCenter=true&width=500&height=60&duration=4000&lines=La+Perla+del+Sur+⚪️;" /> </h1>',unsafe_allow_html=True)
with st.container(border=True):
    st.image(image="app/img/cienfuegos2.jpeg", use_column_width=True)
    st.markdown('<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#2ec9f0;">Análisis migratorio de la provincia de Cienfuegos. <br><l style= "color:#236d7f;">Los factores del empleo, la educación y la familia.</l></b></l></div', unsafe_allow_html=True)
    st.divider()
    st.markdown("",unsafe_allow_html=True)

# CSV's paths
files = ["app/data/csv/ Matrícula inicial educacion superior por curso.csv",
         "app/data/csv/ Población residente según edad laboral por zonas urbana y rural (a) (cálculos al 31 de diciembre de 2019).csv",
         "app/data/csv/ Salario medio mensual en entidades estatales por municipios.csv",
         "app/data/csv/Graduados educacion superior por cursos.csv",
         "app/data/csv/Movimiento migratorio interno por sexos y provincias.csv",
         "app/data/csv/Salario medio mensual en entidades estatales y mixtas por provincias.csv",
         "app/data/csv/Saldos migratorios y tasa de saldo migratorio total por provincias.csv",
         "app/data/csv/Saldos migratorios y tasas de migracion interna y externa por provincias-.csv",
         "app/data/csv/Saldos migratorios y tasas de migración interna y externa, por municipios.csv",
         "app/form/data/La-Perla-del-Sur-Form.csv"]


# I-Migratory movments:
df_mm = pd.read_csv(files[4]) #Read csv
def migratory_movements(df: pd.core.frame.DataFrame, type:str="prov") -> list[pd.core.frame.DataFrame]:
    if type == "prov":
        year2012, year2013, year2014, year2015, year2016, year2017, year2018, year2019, year2020, year2021, year2022 = 0,0,0,0,0,0,0,0,0,0,0
        dfs = [year2012, year2013, year2014, year2015, year2016, year2017, year2018, year2019, year2020, year2021, year2022]
        i = 1
        for index in range(len(dfs)):
            j = i + 49
            dfs[index] = df.iloc[i:j:3,:]
            dfs[index].set_index("PROCEDENCIA/DESTINO", inplace=True)
            dfs[index].index.name=None
            i = j + 3
    elif type == "mun":
        year2019, year2020, year2021, year2022 = 0,0,0,0
        dfs = [year2019, year2020, year2021, year2022]
        i = 1
        for index in range(len(dfs)):
            j = i + 8
            dfs[index] = df.iloc[i:j,:]
            dfs[index].set_index("AÑOS", inplace=True)
            dfs[index].index.name=None
            i = j + 1        
    return dfs
df_mm = migratory_movements(df_mm)

#Load Geojson
with open("app/data/geojsons/cuba.geojson") as json_file:
    data = load(json_file)


lista_prov, data2012, data2013, data2014, data2015, data2016, data2017, data2018, data2019, data2020, data2021, data2022 = sorted(["Artemisa", "Camagüey","Ciego de Ávila","Cienfuegos","Granma","La Habana","Matanzas","Sancti Spíritus","Las Tunas","Holguín","Santiago de Cuba","Isla de la Juventud","Villa Clara","Guantánamo","Pinar del Río","Mayabeque"]), {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
ids, years, values = ["art","cam","cav","cfg", "gra", "gtm", "hol" , "ijv" ,"lha","ltu" ,"mat","may","pri","ssp","stg","vcl"], [x for x in range(2012,2023)], [data2012,data2013,data2014,data2015,data2016,data2017,data2018,data2019,data2020,data2021,data2022] 

for df, year in list(zip(values, [x for x in range(2012, 2023)])):
    for i in lista_prov:
        df[i] = {}
        for id, prov in list(zip(ids, lista_prov)):            
            value = df_mm[years.index(year)].loc[i,prov]
            df[i][id] = int(value) if value != "-" else 0

# Movimientos migratorios intermunicipales 
df_mun = migratory_movements(df, "mun")

# Saldo & tasa de migracion interprovincial total
df_smt = pd.read_csv(files[6])
prov_order = list(df_smt.iloc[::13]["PROVINCIAS/AÑOS"])
df_smt = migratory_movements(df_smt, 'etc')

# Saldo & tasa de migracion interprovincial interno & externo
skipinitalspace_csv(files[7])
df_sm = pd.read_csv(files[7])
df_sm = migratory_movements(df_sm, 'etc')






