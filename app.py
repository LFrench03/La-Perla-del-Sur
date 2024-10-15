###################
# I - Dependences #
###################

import streamlit as st
from streamlit_mermaid import st_mermaid
from json import load
from streamlit_folium import st_folium
import pandas as pd
from folium import Map, GeoJson, GeoJsonTooltip, Choropleth
from geopandas import read_file, GeoDataFrame
from random import randint
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
from collections import Counter


# Funcion para descargar csv's
@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")

# Funcion para eliminar espacios adicionales en los csv
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

# Configuracion de la pagina
st.set_page_config(page_title="La Perla del Sur", page_icon="app/img/perla.jpeg", layout="centered")

# Encabezado
st.markdown('<h1 align="center"><img src="https://readme-typing-svg.herokuapp.comfont=Righteous&size=35&center=true&vCenter=true&width=500&height=60&duration=4000&lines=La+Perla+del+Sur+⚪️;" /> </h1>',unsafe_allow_html=True)
with st.container(border=True):
    st.image(image="app/img/perla4.jpeg", use_column_width=True)
    st.markdown('<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#236d7f;">Un análisis de los procesos migratorios de la provincia de Cienfuegos. <br><l style= "color:gray;font-size:15px;">Los factores del empleo, la educación y la familia.</l></b></l></div', unsafe_allow_html=True)
    st.divider()
    st.markdown("",unsafe_allow_html=True)
    # Conceptos
    with st.expander("**Conceptos**", icon="📚"):
        tab1, tab2, tab3 = st.tabs(["Población", "Educación", "Salario"])
        with tab1:
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:#5665E2;">Población residente:</b> Se refiere a la población que residencia permanentemente en el nivel de la División Político Administrativa.</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:#5665E2;">Población en edad laboral:</b> Corresponde a la población masculina de 17 a 64 años y a la femenina de 17 a 59 años.</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:#5665E2;">Movimiento migratorio:</b> Es el movimiento de la población, en el cual se trespasa una línea de migración que implica un cambio de la residencia habitual.</p>', unsafe_allow_html=True)
            st.markdown('- <p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;">Es <b style="color:#5665E2;">interno</b> cuando se lleva a cabo entre los términos de la División Político Administrativa del país. La migración <b style="color:#5665E2;">externa<b style="color:gray;">, por otro lado, implica un cambio de la residencia habitual en el que se traspasan los límites fronterizos del país.</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:#5665E2;">Saldo migratorio:</b> Es la diferencia entre los inmigrantes (entradas) y los emigrantes (salidas) en un territorio dado para un período de tiempo definido conocido como intervalo de migración. y que regularmente es un año.</p>', unsafe_allow_html=True)
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:#5665E2;">Tasa de migración:</b> Es la relación por cociente entre la diferencia del número de inmigrantes y emigrantes de un territorio dado, con respecto a su población media, durante un intervalo de migración.</p>', unsafe_allow_html=True)
        with tab2:
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:#5665E2;">Graduados:</b> Alumnos que han finalizado satisfactoriamente los estudios correspondientes a un nivel o tipo de educación.</p>', unsafe_allow_html=True)
        with tab3:
            st.markdown('<p style="font-family: sans-serif;font-size:12px;font-weight:bold;color:gray;"><b style="color:#5665E2;">Salario medio mensual:</b> Es el importe de las retribuciones directas devengadas como promedio por un trabajador en un mes. Se calcula dividiendo el salario devengado en un territorio y período determinados entre el promedio de trabajadores y lo obtenido se divide entre el número del mes que se esté analizando.</p>', unsafe_allow_html=True)


st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">En la pintoresca localidad de Rodas, perteneciente a la provincia de Cienfuegos, vivía <b style="color:#5665E2;">Perla</b>, una joven de espíritu indomable que se esforzaba por forjar su propio destino entre el vaivén de las adversidades cotidianas. Su existencia se sostenía sobre tres pilares esenciales: la educación, el trabajo de su madre Lucía y el abrazo cálido de su familia.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;"><b style="color:#5665E2;">Rodas</b>, alejada del bullicio del centro urbano, se encontraba en un rincón donde las limitaciones de la infraestructura pública eran evidentes y las posibilidades económicas parecían un horizonte distante. Esta lejanía del municipio cabecera traía consigo la llegada tardía de servicios básicos y una conectividad con el resto de la ciudad que dejaba mucho que desear, y, además por si fuera poco, la escasez de transporte público dificultaba el desplazamiento intermunicipal, limitando las oportunidades de trabajo y estudio. Sin embargo, <b style="color:#5665E2;">Perla</b> no se dejaba desanimar; en su corazón ardía la determinación de transformar su realidad y abrirse paso hacia un futuro mejor.</p>', unsafe_allow_html=True) 

########################
# II - Data Initialice #
########################

# Rutas de los csv
files = ["app/data/csv/ Población residente según edad laboral por zonas urbana y rural (a) (cálculos al 31 de diciembre de 2019).csv",
         "app/data/csv/ Salario medio mensual en entidades estatales por municipios.csv",
         "app/data/csv/Graduados educacion superiory matricula inicial.csv",
         "app/data/csv/Movimiento migratorio interno por sexos y provincias.csv",
         "app/data/csv/Salario medio mensual en entidades estatales y mixtas por provincias.csv",
         "app/data/csv/Saldos migratorios y tasas de migracion interna y externa por provincias-.csv",
         "app/data/csv/Saldos migratorios y tasas de migración interna y externa, por municipios.csv",
         "app/form/data/La-Perla-del-Sur-Form.csv"]

# Movimientos migratorios por provincias
df_mm = pd.read_csv(files[3]) #Read csv

def migratory_movements(df: pd.core.frame.DataFrame, type:str="prov") -> list[pd.core.frame.DataFrame]:
    # Funcion para el procesamiento de los datos y particion de dataframes
    if type == "prov":
        year2012, year2013, year2014, year2015, year2016, year2017, year2018, year2019, year2020, year2021, year2022 = 0,0,0,0,0,0,0,0,0,0,0
        dfs = [year2012, year2013, year2014, year2015, year2016, year2017, year2018, year2019, year2020, year2021, year2022]
        i = 1
        for index in range(len(dfs)):
            j = i + 49
            dfs[index] = df.iloc[i:j:3,:]
            dfs[index].set_index("PROCEDENCIA/DESTINO", inplace=True)
            dfs[index].index.name='Año'
            i = j + 3
    elif type == "mun":
        year2019, year2020, year2021, year2022 = 0,0,0,0
        dfs = [year2019, year2020, year2021, year2022]
        i = 1
        for index in range(len(dfs)):
            j = i + 8
            dfs[index] = df.iloc[i:j,:]
            dfs[index].set_index("AÑOS", inplace=True)
            dfs[index].index.name='Año'
            i = j + 1
    elif type == "etc":
        prov1, prov2, prov3, prov4, prov5, prov6, prov7, prov8, prov9, prov10, prov11, prov12, prov13, prov14, prov15 = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        dfs = [prov1, prov2, prov3, prov4, prov5, prov6, prov7, prov8, prov9, prov10, prov11, prov12, prov13, prov14, prov15]
        i = 1
        for index in range(len(dfs)):
            j = i + 12
            dfs[index] = df.iloc[i:j,:]
            dfs[index].set_index("PROVINCIAS/AÑOS", inplace=True)
            dfs[index].index.name='Año'
            i = j + 1                    
    return dfs

df_mm = migratory_movements(df_mm) #DataFrame Movimientos migratorios

# Cargar Geojson 
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

# Saldo & tasa de migracion interprovincial interno & externo
skipinitalspace_csv(files[-3])
df_sm = pd.read_csv(files[-3])
prov_order_2 = list(df_sm.iloc[::13]["PROVINCIAS/AÑOS"])
prov_order_2[-1] = "Isla de la Juventud"
last = df_sm.iloc[-12:,:]
last.set_index("PROVINCIAS/AÑOS", inplace=True)
last.index.name=None
df_sm = migratory_movements(df_sm, 'etc')#
df_sm[prov_order_2.index("Guantánamo")] = df_sm[prov_order_2.index("Guantánamo")].iloc[:-1,:]
df_sm.append(last) # All this to correct an exception where the province of Isla de la Juventud is missed

# Graduados & matrícula inicial 
df_gm = pd.read_csv(files[2]) #
df_gm.set_index("Periodo", inplace=True)
df_gm.index.name = None

# Salario medio por municipios
df_sal_mun = pd.read_csv(files[1]) #
df_sal_mun.set_index("PROVINCIA/MUNICIPIOS(Pesos)", inplace=True)
df_sal_mun.index.name = None

# Salario medio por provincias
df_sal_total = pd.read_csv(files[4]) #
df_sal_total.set_index("PROVINCIA", inplace=True)
df_sal_total.index.name = None

# Poblacion residente por municipios
skipinitalspace_csv(files[0])
df_poblacion = pd.read_csv(files[0]) #
df_poblacion = migratory_movements(df_poblacion, 'mun')

# Resultados de la encuesta 
df_form = pd.read_csv(files[-1]) #


########################
# III - Data visualice #
########################

st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">En este contexto si consideramos los datos que nos ofrecen los anuarios estadísticos provinciales en la sección de distribución poblacional general de la provincia según edad laboral por grupos de zonas urbanas y rurales, se muestra de manera clara que más del <b style="color:#5665E2;">40%</b> de la población del municipio reside en la cabecera municipal (<b style="color:#5665E2;">Cienfuegos</b>), lo que indica una concentración significativa de habitantes en esta área. Este comportamiento resalta la atracción que ejerce la cabecera por ofrecer mayores oportunidades de empleo, educación y servicios en comparación con las zonas periféricas. A medida que se desciende en la jerarquía de los asentamientos, la población se dispersa, lo que sugiere que las localidades más alejadas enfrentan retos asociados a la falta de infraestructura y recursos. Esto se ve reflejado diréctamente para <b style="color:#5665E2;">Rodas</b>, que representa menos de un <b style="color:#5665E2;">10%</b> de la distribucion poblacional general contra cerca de un <b style="color:#5665E2;">40%</b> del municipio cabecera. Esta tendencia hacia la centralización demográfica resalta la importancia de desarrollar políticas que fomenten el crecimiento equilibrado y la mejora de las condiciones de vida en todas las áreas del municipio.</p>', unsafe_allow_html=True)

mun_years = [x for x in range(2019,2023)]
year_pobl = st.select_slider("Año: ",mun_years)

colors = ['#00a498','#002b43','#261c93','#2aecde','#5ba5cf', '#366078', '#1d2f39']
toggle3 = st.toggle("Edad laboral")
data_poblacion = np.transpose(df_poblacion[mun_years.index(year_pobl)]).iloc[0,:] if toggle3 else np.transpose(df_poblacion[mun_years.index(year_pobl)]).iloc[3,:]   
# Pie chart para la densidad poblacional dividida en edad laboral y no laboral
fig5 = go.Figure(data = go.Pie(labels=list(data_poblacion.index), values = data_poblacion, pull= 0.1, textposition="outside", hoverinfo='value',textinfo='label+percent', 
    marker=dict(colors=colors, line=dict(color='black', width=3))))
fig5.update_layout(
    width=1300,  
    height=500,  
    margin=dict(l=100, r=100, t=100, b=100))
try:
    st.plotly_chart(fig5)
except Exception as e: 
    raise(f"Error: {e}")
    
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;"><b style="color:#5665E2;">Perla</b> vivía con sus dos abuelos (Andrés y Marta), a quienes cuidaba con dedicación. Por otro lado, su madre trabajaba incansablemente para mantener a la familia, realizando diversos empleos temporales y precarios. Esta situación le permitía a <b style="color:#5665E2;">Perla</b>  enfocarse en sus estudios, pero también le enseñaba la importancia del trabajo duro y la perseverancia.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">La educación era para <b style="color:#5665E2;">Perla</b>  su única salida real para mejorar su situación económica; trabajaba arduamente en sus estudios, sin embargo, la falta de recursos en el municipio afectaba significativamente su acceso a materiales didácticos y a profesores calificados. Su madre, aunque trabajadora incansable, encontraba empleos precarios y mal remunerados, esto llevó a <b style="color:#5665E2;">Perla</b> a reflexionar sobre la relación entre educación y empleo. Veía cómo su madre, con menos educación, tenía pocas opciones de trabajo mejor remunerado, mientras que ella, con más conocimientos, podría acceder a mejores oportunidades.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;"><b style="color:#5665E2;">Perla</b>, en período de exámenes de ingreso, se sentía emocionada y un poco nerviosa al pensar en su futuro académico. Con un buen promedio en las pruebas de ingreso, tenía la oportunidad de elegir libremente su carrera universitaria. Sin embargo, esta decisión no era tan sencilla como parecía. Por un lado, siempre había soñado con estudiar en la capital del país,imaginaba caminar por las calles famosas, conocer gente de diferentes partes del mundo y tener acceso a recursos y experiencias que solo la capital podía ofrecer; pero al mismo tiempo, el pensamiento de dejar atrás a su familia y amigos en <b style="color:#5665E2;">Rodas</b> le causaba angustia.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Mientras tanto, otra opción comenzaba a ganar terreno en su mente. En  <b style="color:#5665E2;">Cienfuegos</b>, específicamente en el municipio cabecera, se ofrecía la posibilidad de estudiar medicina veterinaria. Esta opción tenía algo especial para <b style="color:#5665E2;">Perla</b>: algunas asignaturas afines a sus gustos y pasiones, como los animales y la bioquímica.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Con respecto a dicho asunto, se propone evaluar, mediante una visualización que nos muestre el contraste de matriculas iniciales en relación con los graduados de la educación superior en  <b style="color:#5665E2;">Cienfuegos</b>.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Alcanzando a reflejarse el poco volumen de matrículas y la enorme diferencia referente al número de graduados para cada año en una provincia cuyas unicas instituciones de educación superior radican en la cabecera, por lo que claramente las características del entorno para el escenario de quedarse en su provincia natal van esfumando toda idea o interés por seguir en ese sitio.</p>', unsafe_allow_html=True)


df_gm = np.transpose(df_gm)
df_gm.index.name = "Curso"
# Grafico de area para graduados & matriculas iniciales 
fig4 = px.area(df_gm,markers=True,color_discrete_sequence=["#0c367f", "#5b94f7"], hover_name='value', hover_data={'value':None})
fig4.update_layout(width=1300, height=600, 
        yaxis_title = "Cantidad", xaxis_title = "Cursos", 
        legend=dict(title=dict(text="Leyenda"))) 
try:
    st.plotly_chart(fig4)
except Exception as e: 
    raise(f"Error: {e}")

st.markdown('<p style="font-size:16px;font-weight:bold;color:gray;"><b style="color:#5665E2;">¿Podría encontrar mejores oportunidades en la capital que en <b style="color:#5665E2;">Cienfuegos</b> ¿Qué impacto tendría esta elección en su futuro personal y profesional</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Mientras reflexionaba sobre estas opciones, <b style="color:#5665E2;">Perla</b> no podía evitar pensar en su padre, Andrés, quien desde que ella era pequeña no ha vuelto a verla. Se rumoreaba que se había trasladado a otra región del país por trabajo, dejando atrás a su familia sin explicaciones. Esta ausencia había marcado profundamente la infancia y adolescencia de <b style="color:#5665E2;">Perla</b>, por lo que la idea de estudiar en la capital parecía representar una especie de escapismo, alejándola de las heridas del pasado y ofreciendo nuevas posibilidades. Por otro lado, quedarse en  <b style="color:#5665E2;">Cienfuegos</b> representaba una conexión más fuerte con su familia y su historia personal, pero también podía significar quedarse atrás en términos profesionales.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;"><b style="color:#5665E2;">Perla</b> sabía que esta decisión iba a marcar un punto de inflexión importante en su vida. Mientras tanto, seguía cuidando a sus abuelos, ayudando a su madre con los trabajos domésticos y manteniendo sus estudios como prioridad. Con cada nuevo día, se acercaba más a tomar una decisión que cambiaría el rumbo de su futuro académico y profesional.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">La educación, que siempre había sido su escapismo y su esperanza, ahora se convertía en un dilema personal y emocional. <b style="color:#5665E2;">¿Qué camino elegiría</b>.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Con el objetivo de abordar estas cuestiones se realiza un estudio provincial migratorio para abordar este tema que tanto carcome a la joven de <b style="color:#5665E2;">Perla</b>. Por ello es que se desarrollo este recurso interactivo para analizar de forma interactiva y con precision utilizando datos reales de parte de la cobertura anual de la Oficina Nacional de Estadísticas e Información (ONEI) y así apreciar mejor la situación.</p>', unsafe_allow_html=True)

st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Entonces, en el contexto migratorio desde  <b style="color:#5665E2;">Cienfuegos</b>, se observa que los flujos más significativos se dirigen principalmente hacia las provincias de  <b style="color:#d2952c;">Villa Clara</b>,  <b style="color:#d2952c;">Matanzas</b> y  <b style="color:#d2952c;">La Habana</b>. Por otro lado hacia <b style="color:#5665E2;">Cienfuegos</b> se tiene, en muy pocos volumenes, a provincias como <b style="color:#d2952c;">Sancti Spírictus</b>, <b style="color:#d2952c;">La Habana</b>, <b style="color:#d2952c;">Matanzas</b> y en mayores valores con <b style="color:#5665E2;">532 unidades para el año 2012</b> se encuentra <b style="color:#d2952c;">Villa Clara</b> como principal origen.</p>',  unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">A diferencia de otras regiones de Cuba,  <b style="color:#5665E2;">Cienfuegos</b> presenta una notable estabilidad en su saldo migratorio interno, lo que significa que los movimientos migratorios interprovinciales se equilibran de manera más favorable en comparación con el típico saldo negativo que caracteriza al país en su conjunto de forma general.</p>', unsafe_allow_html=True)
ids = ["art","cam","cav","cfg", "gra", "gtm", "hol" , "ijv" ,"lha","ltu" ,"mat","may","pri","ssp","stg","vcl"]
with st.popover("Filtrado de datos"):
    provincia = st.selectbox("Provincia", lista_prov,index = 3)
    year = st.select_slider("Año",[x for x in range(2012, 2023)])
    if year:
        st.info('La provincia también varía para la gráfica de abajo', icon="ℹ️")
st.markdown(f'<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#56654;">Movimientos migratorios de {provincia} en el año {year}</b></l></div', unsafe_allow_html=True)
def mapa(city:str,year:int):
    # Instanciando Mapa
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
    # Tooltip
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
    
map_data = mapa(provincia, year) # Mapa de densidad

# Scatter plot con tasas y saldos migrorios
toggle = st.toggle("Tasa") # Interruptor para evaluar la tasa en lugar del saldo
if toggle:
    st.markdown(f'<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#56654;">Tasa de migración interna y externa en {provincia}</b></l></div', unsafe_allow_html=True)
    fig = px.scatter(df_sm[prov_order_2.index(provincia)].iloc[:,1::2], color_discrete_sequence=["#f7eb5b", "#d2952c"],hover_name='value', hover_data={'variable':None,'value':None})
    fig.update_layout(width=1200, height=400,
                                        yaxis_title = "Tasa de Migración",xaxis_title="Años",
                                        legend=dict(title=dict(text="Leyenda")))      
else:
    st.markdown(f'<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#56654;">Saldos migratorios internos y externos en {provincia}</b></l></div', unsafe_allow_html=True)
    fig = px.scatter(df_sm[prov_order_2.index(provincia)].iloc[:,::2], color_discrete_sequence=["#0c367f", "#5b94f7"],hover_name='value', hover_data={'variable':None,'value':None})
    fig.update_layout(width=1200, height=400,
                                        yaxis_title = "Saldo migratorio",xaxis_title="Años",
                                        legend=dict(title=dict(text="Leyenda")))  
try:
    st.plotly_chart(fig)
except Exception as e:
    raise(f"Error: {e}")

st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Sin embargo, al analizar la dinámica migratoria a nivel municipal, se evidencia una tendencia significativa hacia el municipio de cabecera,  <b style="color:#5665E2;">Cienfuegos</b>, dominando la densidad poblacional del municipio agrupando a más del  <b style="color:#5665E2;">40%</b> de la población residente. Este dato revela que, a pesar de la estabilidad general de  <b style="color:#5665E2;">Cienfuegos</b>, existe un posible desbalance intermunicipal que podría estar impulsado por la búsqueda de mejores oportunidades laborales, educación y calidad de vida</p>', unsafe_allow_html=True)

mun_year = st.select_slider("Año:  ", mun_years)
# Scatter plot con tasas y saldos migrorios por municipios
toggle_mun = st.toggle(" Tasa ") # Interruptor para evaluar la tasa en lugar del saldo
if toggle_mun:
    st.markdown(f'<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#56654;">Tasa de migración interna y externa por municipios de Cienfuegos en el año {mun_year}</b></l></div', unsafe_allow_html=True)
    figmun = px.scatter(df_mun[mun_years.index(mun_year)].iloc[:,1:-2:2], color_discrete_sequence=["#f7eb5b", "#d2952c"],hover_name='value', hover_data={'variable':None,'value':None})
    figmun.update_layout(width=1200, height=400,
                                        yaxis_title = "Tasa de Migración",xaxis_title="Municipio",
                                        legend=dict(title=dict(text="Leyenda")))      
else:
    st.markdown(f'<div align=center><l style="font-family: serif;font-size:17px;"><b style="color:#56654;">Saldos migratorios internos y externos por municipios de Cienfuegos en el año {mun_year}</b></l></div', unsafe_allow_html=True)
    figmun = px.scatter(df_mun[mun_years.index(mun_year)].iloc[:,0:3:2], color_discrete_sequence=["#0c367f", "#5b94f7"],hover_name='value', hover_data={'variable':None,'value':None})
    figmun.update_layout(width=1200, height=400,
                                        yaxis_title = "Saldo migratorio",xaxis_title="Municipio",
                                        legend=dict(title=dict(text="Leyenda")))  
try:
    st.plotly_chart(figmun)
except Exception as e:
    raise(f"Error: {e}")

st.markdown('<p style="font-size:14px;font-weight:bold;color:gray;"><b style="color:gray;">Además, al considerar los diferentes tipos de saldos migratorios, se concluye que, en términos generales, el saldo externo es el que se lleva la delantera con valores negativos (excluyendo la diferencia de saldo interno del municipio <b style="color:#5665E2;">Cienfuegos</b>). Esto sugiere que, si bien  <b style="color:#5665E2;">Cienfuegos</b> mantiene un equilibrio interno más sólido, la migración hacia el extranjero también juega un papel crucial en la configuración de su demografía y, por ende, en el futuro desarrollo de la región.</p>', unsafe_allow_html=True)
df_sal_mun.index.name = "Municipio"
df_sal_total.index.name = "Municipio"
# Grafico de barra para salarios medios por municipios y de linea para por provincias
bar1, bar2 = st.tabs(["Por municipios", "Por provincias"])
with bar1:
    toggle2 = st.toggle("Excluir año 2021")
    dataframe = np.transpose(df_sal_mun).iloc[:-1,1:] if toggle2 else np.transpose(df_sal_mun).iloc[:,1:]
    fig2 = px.bar(dataframe, hover_name='value', hover_data={'value':None}, orientation='h')
    fig2.update_layout(
                yaxis_title = "Años", xaxis_title = "Salario medio por municipios de Cienfuegos (Pesos)", legend=dict(title=dict(text="Leyenda")))       
    fig2.update_traces(width=0.7,
                        marker_line_color="black",
                        marker_line_width=1.5, opacity=0.4,
                        showlegend = True)
    try:
        st.plotly_chart(fig2)
        with st.expander("**Explicación**"):
            st.info('Aunque ciertamente esta representación a priori puede que no presente un caracter visualmente significativo, se considera emplear este recurso y la interactividad del mismo para aprovechar el formato de pila barras y reflejar las diferencias de cada municipio con respecto al resto (y de forma general también el desarrollo anual del salario medio del municipio entre los considerados). Para evaluar de forma independiente cada municipio pulse dos veces en el cuadrado de color en la leyenda correspondiente al deseado (y pulse una vez para agregar o quitar de la gráfica). Para conocer el valor del salario correspondiente a cada municipio deslice el cursor (pulse si es desde un celular) sobre la representación en la barra que le corresponda con su color y año, se mostrará en un tooltip.', icon="ℹ️")
    except Exception as e:
        raise(f"Error: {e}")
    
with bar2:
    toggle2 = st.toggle("Excluir años 2021 & 2022")
    dataframe = np.transpose(df_sal_total).iloc[:-2,1:] if toggle2 else np.transpose(df_sal_total).iloc[:,1:]
    fig3 = px.line(dataframe, hover_name='value', hover_data={'value':None}, markers=True)
    fig3.update_layout(
                yaxis_title = "Salario medio por provincias de Cuba (Pesos)", xaxis_title = "Años", legend=dict(title=dict(text="Leyenda")))          
    try:
        st.plotly_chart(fig3)
    except Exception as e: 
        raise(f"Error: {e}")    

st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">En el ámbito de las oportunidades laborales,  <b style="color:#d2952c;">La Habana</b> se posiciona como un imán para quienes buscan una mejor calidad de trabajo y un nivel de vida más elevado. En comparación con  <b style="color:#5665E2;">Cienfuegos</b>, la capital ofrece mayores posibilidades de empleo, con una variedad más amplia de sectores y empresas que garantizan salarios medios más altos. Además, en  <b style="color:#d2952c;">La Habana</b>, es más común acceder a créditos y a una gama de servicios que facilitan el desarrollo personal y profesional, lo que atrae a muchos migrantes de otras provincias en busca de un futuro más prometedor.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Este contexto de oportunidades podría explicar, aunque de manera dolorosa, la decisión de Andrés, el padre de <b style="color:#5665E2;">Perla</b>, de abandonar a su familia. La búsqueda de una vida mejor, repleta de mayores oportunidades laborales y económicas, puede haberle hecho sentir que su única opción para subsistir y prosperar era dejar atrás su hogar en busca de esos beneficios en la capital. Su partida, aunque injusta para <b style="color:#5665E2;">Perla</b> y su madre, refleja una realidad compleja en la que la atracción de  <b style="color:#d2952c;">La Habana</b> por sus mejores condiciones de trabajo y calidad de vida puede haber superado su responsabilidad familiar, llevándolo a tomar una decisión que dejó una marca profunda en su familia.</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">De igual forma se puede decir si consideramos las diferencias intermunicipales, que se mantienen con ligera superioridad general los valores de media salarial para la cabeza del municipio, resaltando en parte nuevamente el desblanace estructural de distribución de recursos municipales existente en dicho territorio.</p>', unsafe_allow_html=True)
st.divider()
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">La búsqueda de mejores oportunidades de empleo y educación es un impulso fundamental que motiva a las personas a migrar, tanto a nivel interno como externo. Este fenómeno refleja no solo la aspiración individual de alcanzar una vida más digna y satisfactoria, sino también un contexto socioeconómico que, en muchos casos, limita el desarrollo personal y profesional en sus lugares de origen. La decisión de emprender este camino, aunque a menudo dolorosa y compleja, simboliza la lucha por la superación y el deseo de construir un futuro mejor. Al mismo tiempo, pone de manifiesto las disparidades entre regiones, donde lugares como La Habana ofrecen un abanico más amplio de oportunidades comparado con provincias como <b style="color:#5665E2;">Cienfuegos</b>. En última instancia, este deseo de progreso se convierte en una fuerza dinámica que puede transformar realidades, tanto para los individuos como para las comunidades a las que pertenecen.</p>', unsafe_allow_html=True)
st.divider()
st.divider()


##################
# IV - Interview #
##################


st.markdown('<div align=center><l style="font-family: serif;font-size:60px;"><b style="color:#236d7f;">Encuesta</b></l></div', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Con el objetivo de recopilar perspectivas sobre el tema en cuestión, se llevó a cabo una encuesta online utilizando la aplicación <b style="color:#5665E2;">forms.app</b>, la cual fue realizada por <b style="color:#5665E2;">45 personas</b>. Aunque es importante señalar que los resultados de esta encuesta no poseen valor estadístico general debido a su carácter no representativo, no obstante la cantidad de participantes y la estructura intuitiva del cuestionario fomentaron interacciones valiosas y significativas.</p',unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">La encuesta fue diseñada para facilitar la participación y animar a los encuestados a compartir sus opiniones, lo que permitió obtener una variedad de respuestas que enriquecen el análisis del tema. A pesar de no ser un conjunto de datos estadísticamente válido, la diversidad de voces y experiencias recogidas brinda un panorama interesante que puede ser considerado para profundizar en la discusión. A continuación, procederé a presentar los resultados y las opiniones surgidas durante este ejercicio, resaltando las temáticas que han captado más atención entre los participantes y las luces que aportan al entendimiento del fenómeno estudiado.</p',unsafe_allow_html=True)
with st.expander("**Diagrama de flujo de la encuesta**"):
    mermaid_code = """
%%{init:{'theme':'base', 'themeVariables':{'primaryColor': '#5665E2','edgeLabelBackground': '#236d7f', 'primaryTextColor': '#ffffff', 'lineColor': 'gray','primaryBorderColor': '#ffffff', 'font-size':'20px','font-family':'monospace, monaco'}}}%%
graph TD
Y[Comienzo]-->A[Rango de Edad]
A--10-16-->B{Cuál es tu género}
A--17-25-->B
A--26-50-->B
A--51-66-->B
A--68 o más-->B
B--Masculino-->C[Historia de Perla y decisión de carrera]
B--Femenino-->C
B--Otro-->C
C--Lic. Bioquímica en la UH-->D{Qué elegirías}
C--Medicina Veterinaria en Cienfuegos-->D
C--Otro-->D
D--Por qué-->E{Estaría en tus planes futuros emigrar en algún momento}
E--Sí... Por qué-->F{Cómo sería tu proceso migratorio}
E--No... Por qué-->K{Buscarías a tu padre}
F--Interno-->G{Intermunicipal o interprovincial}
F--Externo-->M{Hacia dónde irías}
G--Intermunicipal-->L{Cuál sería tu lugar de destino}
G--Interprovincial-->H{Cuál sería tu destino}
H--Provincia-->I{Por qué crees que decidirías emigrar}
I-->J{Cómo les ofrecerías apoyo a la familia}
J-->K
K--Sí...Por qué-->N{Te llamó la atención la imagen de la chica al principio del cuestionario}
K--No...Por qué-->N
N-->X[FIN]
L--La capital de mi provincia natal-->I
L--Otro municipio-->I
M-- Región-->I
"""
    st_mermaid(mermaid_code, height="500px")
st.divider()
st.markdown('<div align=center><l style="font-family: serif;font-size:40px;"><b style="color:#236d7f;">Audiencia</b></l></div', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Como parte de la audiencia, como fue comentado anteriormente, se contó con la participación de 45 personas con interacciones completas para la mayoría. De ellas se tiene que, en respuesta a las primeras preguntas de identificación, hubo un predominio de edad entre los <b style="color:#5665E2;">17-25</b> años y de <b style="color:#5665E2;">masculino</b> como parte del género. Como se observa visualmente presentado por la órden de las preguntas como encabezado.</p',unsafe_allow_html=True)

def form_chart(column:str):
    data = list(df_form[column])
    age_counts = Counter(data)
    labels = list(age_counts.keys())
    values = list(age_counts.values())
    fig6 = go.Figure(data = go.Pie(labels=labels, values = values, pull= 0.1, textposition="outside", hoverinfo='value',textinfo='label+percent', marker=dict(colors= ['#002b43','#261c93','#2aecde','#5ba5cf', '#366078', '#1d2f39', '#00a498'], line=dict(color='black', width=3))))
    fig6.update_layout(
            width=1300,  
            height=500,  
            margin=dict(l=100, r=100, t=100, b=100))
    return fig6
try:
    st.markdown('<div align=center><l style="font-family: serif;font-size:20px;"><b style="color:#5665E2;">Selecciona tu grupo de edad, por favor</b></l></div', unsafe_allow_html=True)
    st.plotly_chart(form_chart("Selecciona tu grupo de edad, por favor."))
    
except Exception as e: 
    raise(f"Error: {e}")
try:
    st.markdown('<div align=center><l style="font-family: serif;font-size:20px;"><b style="color:#5665E2;">¿Cuál es tu género</b></l></div', unsafe_allow_html=True)
    st.plotly_chart(form_chart("¿Cuál es tu género"))
except Exception as e: 
    raise(f"Error: {e}")
st.divider()
st.markdown('<div align=center><l style="font-family: serif;font-size:40px;"><b style="color:#236d7f;">Resultados</b></l></div', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Con respecto al tema de los resultados se tienen a las preguntas referentes a la naturaleza de la problemática en cuestión obteniendose que prefirieron optar por el futuro académico de <b style="color:#5665E2;">Perla</b> con una mayoría de votos para la <b style="color:#5665E2;">Licenciatura en Bioquimica</b> en <b style="color:#5665E2;">LaUniversidad de La Habana</b>.</p',unsafe_allow_html=True)

try:
    st.markdown('<div align=center><l style="font-family: serif;font-size:20px;"><b style="color:#5665E2;">¿Qué elegirías</b></l></div', unsafe_allow_html=True)
    st.plotly_chart(form_chart("¿Qué elegirías"))
except Exception as e: 
    raise(f"Error: {e}")
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">En un contexto más personal, para descubrir el caracter de las inclinaciones de la audiencia con respecto a la migración, se tuvo que el <b style="color:#5665E2;">93.6%</b> de las personas presentaban intereses migratorios, resaltando el deseo común de mejora mencionado anteriormente.</p',unsafe_allow_html=True)

try:
    st.markdown('<div align=center><l style="font-family: serif;font-size:20px;"><b style="color:#5665E2;">¿Estaría en tus planes futuros emigrar en algún momento</b></l></div', unsafe_allow_html=True)
    st.plotly_chart(form_chart("¿Estaría en tus planes futuros emigrar en algún momento"))
except Exception as e: 
    raise(f"Error: {e}")

st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Luego, con fines de ahondar más en el asunto de los intereses migratorios de la audiencia se tuvo (al no considerar los "-" -respuestas vacias-) que alrededor de un <b style="color:#5665E2;">95%</b> prefirieron un carácter <b style="color:#5665E2;">externo</b>, algo bastante normal considerando la situación de descontento general de la población del país y que se evidencia además en los hallazgos referentes a nuestro objeto de estudio.</p',unsafe_allow_html=True)
try:
    st.markdown('<div align=center><l style="font-family: serif;font-size:20px;"><b style="color:#5665E2;">¿Cómo seria tu proceso migratorio</b></l></div', unsafe_allow_html=True)
    st.plotly_chart(form_chart("¿Cómo seria tu proceso migratorio"))
except Exception as e: 
    raise(f"Error: {e}")

st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Y, para concluir con las respuestas se le quiso plantear al público, en función de evaluar desde el punto de la historia como seguirían su desarrollo en el ambiente delicado que se presentó y así ver reflejadas de forma general que dirección predomina. De esta forma se tuvo una respuesta equilibrada a la consideración de la situación futura su padre Andrés, con una ligera superioridad resultante de un <b style="color:#5665E2;">52.3f%</b> de afirmación al deseo de reencontrarse con el.</p>',unsafe_allow_html=True)
try:
    st.markdown('<div align=center><l style="font-family: serif;font-size:20px;"><b style="color:#5665E2;">Y por último, ¿buscarías a tu padre</b></l></div', unsafe_allow_html=True)
    st.plotly_chart(form_chart("¿Buscarías a tu padre"))
except Exception as e: 
    raise(f"Error: {e}")
st.divider()
st.markdown('<div align=center><l style="font-family: serif;font-size:40px;"><b style="color:#236d7f;">Opiniones</b></l></div', unsafe_allow_html=True)
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Se considera dedicar un apartado específico para las opiniones particulares de los internautas, empleando un sistema de selección aleatoria para mostrar algunas de las razones y luces de los participantes en el cuestionario.</p>',unsafe_allow_html=True)

def random(cuestion:str) -> str:
    # Funcion para devolver respuesta aleatoria
    cuestion = [x for x in list(df_form[cuestion]) if x!="-"] # Saltar las respuestas vacias
    value = randint(0,len(cuestion)-1)
    return cuestion[value]
# Opiniones aleatorias
cuestion1, cuestion2 = st.tabs(["¿Qué elegirías", "¿Buscarías a tu padre"])
with cuestion1:
    st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Referente a la pregunta de <b style="color:#5665E2;">¿Qué elegirías</b> se tienen razones como:</p',unsafe_allow_html=True)
    st.button("Reset", type="primary", use_container_width=True)
    if st.button("Respuesta aleatoria", use_container_width=True):
        st.markdown('<p style="font-size:16px;font-weight:bold;color:black;">Respuesta: <b style="color:#236d7f;"> {} </b></p>'.format(random("¿Por qué")),unsafe_allow_html=True)
        st.markdown('<p style="font-size:16px;font-weight:bold;color:gray;">Pulsa el botón <b style="color:#236d7f;">Reset</b> para empezar de nuevo o el botón <b style="color:#236d7f;">Respuesta Aleatoria</b> para recibir otra respuesta.</p>',unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:16px;font-weight:bold;color:gray;">Pulsa el botón <b style="color:#236d7f;">Respuesta aleatoria</b> para comenzar.</p>',unsafe_allow_html=True) 
with cuestion2:
    st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">Y, finalmente, a la cuestión de <b style="color:#5665E2;">¿porqué buscarías o no a tu padre</b> se tuvo que:</p',unsafe_allow_html=True)
    st.button(" Reset ", type="primary", use_container_width=True)
    if st.button(" Respuesta aleatoria ", use_container_width=True):
        st.markdown('<p style="font-size:16px;font-weight:bold;color:black;">Respuesta: <b style="color:#236d7f;"> {} </b></p>'.format(random("¿Por qué.2")),unsafe_allow_html=True)
        st.markdown('<p style="font-size:16px;font-weight:bold;color:gray;">Pulsa el botón <b style="color:#236d7f;">Reset</b> para empezar de nuevo o el botón <b style="color:#236d7f;">Respuesta Aleatoria</b> para recibir otra respuesta.</p>',unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:16px;font-weight:bold;color:gray;">Pulsa el botón <b style="color:#236d7f;">Respuesta aleatoria</b> para comenzar.</p>',unsafe_allow_html=True) 

st.divider()
st.markdown('<p style="font-size:14px;font-weight:bold;"><b style="color:gray;">La toma de una decisión en una situación tan comprometida como la de  <b style="color:#5665E2;">Perla</b> es algo sumamente complejo, intervienen muchos factores y resulta inadecuado asumir o dar una respuesta genérica para este tipo de situaciones. Lo más adecuado en estos casos considero que sea consultarlo con familiares, amistades y evaluar bien cada factor para saber que riesgos se consideran asumir con objetivos claros. Las respuestas de los participantes sin duda contribuyeron a reafirmar por medio de terceros al proceso decisivo de  <b style="color:#5665E2;">Perla</b>, y además, el antecedente de su padre, quien como ella tuvo que tomar una decisión teniendo sus propias consideraciones, influyen directamente en su proceso. Pero, independientemente de cual sea el camino que elija, deseemosle la mejor de las suertes y éxitos a <b style="color:#5665E2;">Perla</b>.</p',unsafe_allow_html=True)
st.divider()

st.markdown('<l style="font-family: serif;font-size:55px;"><b style="color:#236d7f;">Gracias por tu atención :)</b></l>', unsafe_allow_html=True)
st.divider()
st.divider()

##################
# V - References #
##################

st.markdown('<div align=center><l style="font-family: serif;font-size:25px;"><b style="color:black;">Referencias</b></l></div', unsafe_allow_html=True)
st.markdown('* *Repositorio del proyecto [Entrar aquí](https://github.com/LFrench03/La-Perla-del-Sur)*')
st.markdown('* *Sitio web de la Oficina Nacional de Estadísticas e Información [Entrar aquí](https://www.onei.gob.cu/)*')
st.markdown('* *Repositorio de Yudivian Almeida con los datos geolocalizables en formato geojson de las provincias y municipios de Cuba [Entrar aquí](https://github.com/yudivian/cuba-geojsons/tree/master)*')
st.markdown('* *Documentación de Plotly [Entra aquí](https://plotly.com/python/)*')
st.markdown("* *Panorámica del comportamiento de la movilidad intermunicipal en la provincia de Cienfuegos.[Entra aquí](http://scielo.sld.cu/scielo.phpscript=sci_arttext&pid=S1817-40782021000100038#B10)*")
st.markdown('* *Documentación de Streamlit [Entra aquí](https://docs.streamlit.io/develop/api-reference)*')
st.divider()

#############################
# VI - Downloadble contents #
#############################

st.markdown('<div align=center><l style="font-family: serif;font-size:25px;"><b style="color:gray;">Contenido descargable</b></l></div', unsafe_allow_html=True)
csv1, csv2, csv3, csv4, csv5, csv7, csv8 = convert_df(pd.read_csv(files[0])), convert_df(pd.read_csv(files[1])), convert_df(pd.read_csv(files[2])), convert_df(pd.read_csv(files[3])), convert_df(pd.read_csv(files[4])), convert_df(pd.read_csv(files[6])), convert_df(pd.read_csv(files[7]))
with st.popover("Descargar CSV's",use_container_width=True):
    d1, d2, d3, d4 = st.columns(4)
    d5, d7, d8 = st.columns(3)

    with d1:
        st.download_button( 
            label="Poblacion residente",
            data=csv1,
            file_name="Poblacion residente.csv",
            mime="text/csv")                  
    with d2:
        st.download_button( 
            label="Salario por municipios",
            data=csv2,
            file_name="Salario medio mensual por municipios de Cienguegos.csv",
            mime="text/csv")  
    with d3:
        st.download_button( 
            label="Graduados&matrícula",
            data=csv3,
            file_name="graduados y matrícula inicial.csv",
            mime="text/csv")
    with d4:
        st.download_button( 
            label="Movimientos Migratorios",
            data=csv4,
            file_name="movimientos migratorios.csv",
            mime="text/csv")          
    with d5:
        st.download_button( 
            label="Salario por provincia",
            data=csv5,
            file_name="Salario medio por provincias.csv",
            mime="text/csv")        
    with d7:
        st.download_button( 
            label="Saldos&Tasa por tipos",
            data=csv7,
            file_name="Saldo&Tasa por provincia por tipos.csv",
            mime="text/csv")                             
    with d8:
        st.download_button( 
            label="Saldo&Tasa municipal",
            data=csv8,
            file_name="Saldo&Tasa municipal.csv",
            mime="text/csv")             

#############
# VII - End #
#############