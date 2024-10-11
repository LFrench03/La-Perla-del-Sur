#Dependences
import streamlit as st
from json import load
from streamlit_folium import st_folium
import pandas as pd
from folium import Map, GeoJson, GeoJsonPopup, GeoJsonTooltip, Choropleth, LayerControl
from geopandas import read_file, GeoDataFrame
from random import randint
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

# Page configuration
st.set_page_config(page_title="La Perla del Sur", page_icon="app/img/perla.jpeg", layout="centered")

# Header
st.markdown('<h1 align="center"><img src="https://readme-typing-svg.herokuapp.com?font=Righteous&size=35&center=true&vCenter=true&width=500&height=60&duration=4000&lines=La+Perla+del+Sur+⚪️;" /> </h1>',unsafe_allow_html=True)
with st.container(border=True):
    st.image(image="app/img/perla4.jpeg", use_column_width=True)
    st.markdown('<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#236d7f;">Análisis migratorio de la provincia de Cienfuegos. <br><l style= "color:gray;">Los factores del empleo, la educación y la familia.</l></b></l></div', unsafe_allow_html=True)
    st.divider()
    st.markdown("",unsafe_allow_html=True)
    with st.expander("**Definciones**", icon="📚"):
        tab1, tab2, tab3 = st.tabs(["Población", "Educación", "Salario"])
        with tab1:
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:black;">Población residente:</b> Se refiere a la población que residencia permanentemente en el nivel de la División Político Administrativa .</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:black;">Población en edad laboral:</b> Corresponde a la población masculina de 17 a 64 años y a la femenina de 17 a 59 años.</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:black;">Movimiento migratorio:</b> Es el movimiento de la población, en el cual se trespasa una línea de migración que implica un cambio de la residencia habitual.</p>', unsafe_allow_html=True)
            st.markdown('- <p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;">Es <b style="color:black;">interno</b> cuando se lleva a cabo entre los términos de la División Político Administrativa del país. La migración <b style="color:black;">externa<b style="color:gray;">, por otro lado, implica un cambio de la residencia habitual en el que se traspasan los límites fronterizos del país.</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:black;">Saldo migratorio:</b> Es la diferencia entre los inmigrantes (entradas) y los emigrantes (salidas) en un territorio dado para un período de tiempo definido conocido como intervalo de migración. y que regularmente es un año.</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:black;">Tasa de migración:</b> Es la relación por cociente entre la diferencia del número de inmigrantes y emigrantes de un territorio dado, con respecto a su población media, durante un intervalo de migración.</p>', unsafe_allow_html=True)
        with tab2:
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:black;">Graduados:</b> Alumnos que han finalizado satisfactoriamente los estudios correspondientes a un nivel o tipo de educación..</p>', unsafe_allow_html=True)
        with tab3:
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:black;">Salario medio mensual:</b> Es el importe de las retribuciones directas devengadas como promedio por un trabajador en un mes. Se calcula dividiendo el salario devengado en un territorio y período determinados entre el promedio de trabajadores y lo obtenido se divide entre el número del mes que se esté analizando.</p>', unsafe_allow_html=True)


#######################
# I - Data Initialice #
#######################

# CSV's paths
files = ["app/data/csv/ Población residente según edad laboral por zonas urbana y rural (a) (cálculos al 31 de diciembre de 2019).csv",
         "app/data/csv/ Salario medio mensual en entidades estatales por municipios.csv",
         "app/data/csv/Graduados educacion superiory matricula inicial.csv",
         "app/data/csv/Movimiento migratorio interno por sexos y provincias.csv",
         "app/data/csv/Salario medio mensual en entidades estatales y mixtas por provincias.csv",
         "app/data/csv/Saldos migratorios y tasa de saldo migratorio total por provincias.csv",
         "app/data/csv/Saldos migratorios y tasas de migracion interna y externa por provincias-.csv",
         "app/data/csv/Saldos migratorios y tasas de migración interna y externa, por municipios.csv",
         "app/form/data/La-Perla-del-Sur-Form.csv"]

# Movimientos migratorios por provincias
df_mm = pd.read_csv(files[3]) #Read csv

def migratory_movements(df: pd.core.frame.DataFrame, type:str="prov") -> list[pd.core.frame.DataFrame]:
    #Funcion para el procesamiento de los datos
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
    elif type == "etc":
        prov1, prov2, prov3, prov4, prov5, prov6, prov7, prov8, prov9, prov10, prov11, prov12, prov13, prov14, prov15 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        dfs = [prov1, prov2, prov3, prov4, prov5, prov6, prov7, prov8, prov9, prov10, prov11, prov12, prov13, prov14, prov15]
        i = 1
        for index in range(len(dfs)):
            j = i + 12
            dfs[index] = df.iloc[i:j,:]
            dfs[index].set_index("PROVINCIAS/AÑOS", inplace=True)
            dfs[index].index.name=None
            i = j + 1                    
    return dfs

df_mm = migratory_movements(df_mm) #DataFrame Movimientos migratorios

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
df_mun = pd.read_csv(files[-2])
df_mun = migratory_movements(df_mun, "mun") #

# Saldo & tasa de migracion interprovincial total
df_smt = pd.read_csv(files[6])
prov_order = list(df_smt.iloc[::13]["PROVINCIAS/AÑOS"])
df_smt = migratory_movements(df_smt, 'etc')

# Saldo & tasa de migracion interprovincial interno & externo
skipinitalspace_csv(files[-3])
df_sm = pd.read_csv(files[-3])
df_sm = migratory_movements(df_sm, 'etc')#

# Graduados y matricula inicial 
df_gm = pd.read_csv(files[2]) #
df_gm.set_index("Periodo", inplace=True)
df_gm.index.name = None

# Salario medio por municipios
df_sal_mun = pd.read_csv(files[1]) #
df_sal_mun.set_index("PROVINCIA/MUNICIPIOS(Pesos)", inplace=True)
df_sal_mun.index.name = None

# Salario medio por provnicias
df_sal_total = pd.read_csv(files[4]) #
df_sal_total.set_index("PROVINCIA", inplace=True)
df_sal_total.index.name = None

# Poblacion residente por municipios
skipinitalspace_csv(files[0])
df_poblacion = pd.read_csv(files[0]) #
df_poblacion = migratory_movements(df_poblacion, 'mun')

##### Encuesta ######
df_form = pd.read_csv(files[-1]) #

#######################
# II - Data visualice #
#######################

ids = ["art","cam","cav","cfg", "gra", "gtm", "hol" , "ijv" ,"lha","ltu" ,"mat","may","pri","ssp","stg","vcl"]
with st.popover("Filtrado de datos"):
    provincia = st.selectbox("Provincia", lista_prov,index = 3)
    year = st.select_slider("Año",[x for x in range(2012, 2023)])
def mapa(city:str,year:int):
        #Instanciando Mapa
    m = Map(location=[21.3, -79.6], tiles="CartoDB positron", zoom_start=6, no_touch=True)        

    mapdata = {}
    for i,j in zip(ids, lista_prov):
        mapdata[i] = int(df_mm[years.index(year)].loc[city,j])
    city_data = pd.DataFrame({"ID":list(mapdata.keys()),
                             "Val":list(mapdata.values())})  
    Choropleth(
                geo_data="app/data/geojsons/cuba.geojson",
                name="Entidades",
                data=city_data,
                columns = ['ID', 'Val'],
                key_on='feature.properties.province_id',
                fill_color='YlGnBu',
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name='Movimientos Migratorios (Unidad)',
                reset=True,
                control=False
        ).add_to(m)     
    #Tooltip
    geo_data = read_file("app/data/geojsons/cuba.geojson")
    geodf = GeoDataFrame.from_features(geo_data)
    geodf.crs = "EPSG:4326"    
    tooltip = GeoJsonTooltip(fields=["province", str(provincia)+str(year)], 
                                    aliases=["<strong>Provincia:</strong>", "<strong>Valor:</strong>"],
                                        sticky=False)
    GeoJson(
                geodf,
                name="Datos",
                style_function=lambda feature: {"color":"#767676"},
                highlight_function=lambda feature: {"fillColor": "#ffff00"},
                tooltip=tooltip,
                control=False  
    ).add_to(m)
    return st_folium(m, use_container_width=True, height=550)
map_data = mapa(provincia, year)



