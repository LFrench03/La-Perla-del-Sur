import json 
import pandas as pd
'''
Script para agregar los valores que se mostrarian en el tooltip del mapa al geojson
'''
with open("app/data/geojsons/cuba.geojson") as json_file:
    data = json.load(json_file)
path = "app/data/csv/Movimiento migratorio interno por sexos y provincias.csv"

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
skipinitalspace_csv(path)

df = pd.read_csv(path)
def migratory_movements(df: pd.core.frame.DataFrame) -> list[pd.core.frame.DataFrame]:
    year2012, year2013, year2014, year2015, year2016, year2017, year2018, year2019, year2020, year2021, year2022 = 0,0,0,0,0,0,0,0,0,0,0
    dfs = [year2012, year2013, year2014, year2015, year2016, year2017, year2018, year2019, year2020, year2021, year2022]
    i = 1
    for index in range(len(dfs)):
        j = i + 49
        dfs[index] = df.iloc[i:j:3,:]
        dfs[index].set_index("PROCEDENCIA/DESTINO", inplace=True)
        dfs[index].index.name=None
        i = j + 3
    return dfs

df = migratory_movements(df)
years = [x for x in range(2012,2023)] #Ordederd list of years
provincias = list(df[0].columns)[1:]

#Provincias en el orden que aparece en la estructura del GeoJson
lista_prov = ["La Habana","Matanzas","Cienfuegos","Sancti Spíritus","Las Tunas","Holguín","Granma","Santiago de Cuba","Isla de la Juventud"
              ,"Camagüey","Ciego de Ávila","Villa Clara","Guantánamo","Pinar del Río","Artemisa","Mayabeque"] 

index = 0
n = list(df[0].index)
for year in years:    
    for index, prov in enumerate(lista_prov):
        values = list(df[years.index(year)].iloc[:,n.index(prov)])[1:]
        for k, j in list(zip(provincias,values)):
            data["features"][index]["properties"][f"{k}{year}"] = j    
try:
    with open("app/data/geojsons/cuba.geojson", 'w') as archivo_json:
        json.dump(data, archivo_json, indent=4)
        print("GeoJson Actualizado de forma exitosa")
except Exception as e:
    print(f"Error al procesar el GeoJson: {e}")