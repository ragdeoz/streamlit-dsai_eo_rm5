import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import codecs

DATA_URL = '/content/Employees.csv'
E_ID = 'Employee_ID'

# Definición de funciones
@st.cache
def load_data(nrows):
    #doc = codecs.open(DATA_URL,'rU','latin1')
    data = pd.read_csv(DATA_URL, nrows=nrows) #(doc, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    return data

def filter_by_id(id):
    dfid = data[data[E_ID] == id]
    return dfid

def filter_by_location(location,col):
    filterbyloc = data[data[col].str.contains(location, case=False)]
    return filterbyloc

def filter_by_type(tipo,col):
    filterbytype = data[data[col] == tipo]
    return filterbytype

def gen_graph(gtype, attribute1, attribute2, bins, color, gtitle, xlabel, ylabel):
    fig, ax = plt.subplots()
    if gtype == 'hist':
        ax.hist(attribute1, bins=bins, color=color)
    elif gtype == 'barh':
        ax.barh(attribute1, attribute2, color=color)
    ax.set_title(gtitle)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return st.pyplot(fig)

# Creación del título de la aplicación, encabezados y texto de descripción del proyecto. 
st.title("Employees Dashboard")
st.header("DS&AI Reto M5")

st.write("""
Fenómeno de deserción laboral en empresas y organizaciones

Fuente de la hipótesis: Datos del Hackathon HackerEarth 2020.
""")

# Creación de la barra lateral
sidebar = st.sidebar
sidebar.title("Filtros:")

# Recuperar registros
count_rows = 0
DATA_QUOTA = sidebar.slider('Selecciar cantidad de registros del análisis', 0, 7000, 500, step=500)
data_load_state = sidebar.text('Loading Employees Data...')
data = load_data(DATA_QUOTA)
data_load_state.text("Done! (using s.cache)")
count_rows = data.shape[0]

if count_rows > 0:
    if sidebar.checkbox("Mostrar todas los empleados"): # Creación del CHECKBOX mostrar dataframe
       st.write("Total de Empleados:", count_rows)
       st.write(data)
    
    st.markdown("___")

    # TEXT_INPUT+BUTTON del buscador por Empleado, por Ciudad de Origen y por Unidades
    employee_id = sidebar.text_input('ID Empleado: ')
    id_btn = sidebar.button('BUSCAR EMPLEADO')
    if (id_btn):
        employee = filter_by_id(employee_id)
        if employee.shape[0] != 0:
            st.write(f"Registro del empleado con ID {employee_id}:")
        else:
            st.write(f"El ID {employee_id} no se encuantra en los datos!")
        st.write(employee)

    hometown = sidebar.text_input('Ciudad de Origen: ')
    hometown_btn = sidebar.button('FILTRAR X CIUDAD')
    if (hometown_btn):
        dfhometown = filter_by_location(hometown,'Hometown')
        st.write(f"{hometown} tiene una coincidencia de {dfhometown.shape[0]} de los {count_rows} registros de la muestra")
        st.write(dfhometown)

    unit = sidebar.text_input('Unidad: ')
    unit_btn = sidebar.button('FILTRAR X UNIDAD')
    if (unit_btn):
        dfunit = filter_by_location(unit, 'Unit')
        st.write(f"{unit} tiene una coincidencia de {dfunit.shape[0]} de los {count_rows} registros de la muestra")
        st.write(dfunit)

    st.markdown("___")

    # SELECTBOX del filtro de Empleados por Nivel Educativo / por Ciudad / y por Unidad Funcional
    education_level = sidebar.selectbox("Seleccionar Nivel Educativo", data['Education_Level'].unique(), index=2)
    if (education_level):
        dfeducatiolevel = filter_by_type(education_level,'Education_Level')
        st.write(f"{dfeducatiolevel.shape[0]} empleados en el nivel educativo [{education_level}]")
        st.write(dfeducatiolevel)

    city = sidebar.selectbox("Seleccionar Ciudad", np.append(['----'], data['Hometown'].unique()))
    if (city):
        if city != '----':
            dfcity = filter_by_type(city, 'Hometown')
            st.write(f"{dfcity.shape[0]} empleados en {city}")
            st.write(dfcity)

    funit = sidebar.selectbox("Seleccionar Unidad Funcional", np.append(['----'], data['Unit'].unique()))
    if (funit):
        if funit != '----':
            dffu = filter_by_type(funit, 'Unit')
            st.write(f"{dffu.shape[0]} empleados en la unidad funcional {funit}")
            st.write(dffu)

    st.markdown("___")

    # PRESENTACION DE GRAFICAS
    st.subheader("Visualización de Datos")

    gen_graph('hist', data.Age, '', [20,25,30,35,40,45,50,55,60,65,70], 'lightskyblue', 'Histograma de empleados agrupados por edad', 'Rangos de Edades', 'Cantidad de Empleados') # HISTOGRAMA por Edad, usando funciones

    st.markdown("___")

    empbyunit = data.groupby(by=["Unit"]).agg({"Unit":np.size})
    empbyunit = empbyunit.rename(columns = {"Unit" : "Total"})
    eubd = empbyunit.reset_index()

    gen_graph('barh', eubd.Unit, eubd.Total, 0, 'turquoise', 'Frecuencia de empleados por unidades funcionales', 'Cantidad de Empleados', '') # GRAFICA DE FRECUENCIAS de Unidades Funcionales, usando Funciones

    st.markdown("___")

    fig, axs = plt.subplots(3,1,figsize=(5,15))
    plt.subplots_adjust(hspace=0.3)
            # Ciudades con mayor índice de deserción
    axs[0].bar(data.Hometown, data.Attrition_rate, color='plum')
    axs[0].set_title('Índice de deserción por ciudad')
    axs[0].set_ylabel("Tasa de Deserción")
            # Edad e índice de deserción
    axs[1].scatter(data.Age, data.Attrition_rate, color='purple')
    axs[1].set_title('Índice de deserción por edad')
    axs[1].set_xlabel("Edad")
    axs[1].set_ylabel("Índice de Deserción")
            # Ciudades con mayor índice de deserción
    axs[2].scatter(data.Time_of_service, data.Attrition_rate, color='purple')
    axs[2].set_title('Índice de deserción por tiempo de servicio')
    axs[2].set_xlabel("Tiempo de Servicio")
    axs[2].set_ylabel("Índice de Deserción")

    st.pyplot(fig)

    st.markdown("___")

    st.write("""
    * Asociación NULA entre las variables numéricas.
      No existe correlación entre el Índice de Deserción y la Edad,
      ni entre el Índice de Deserción y el Tiempo de Servicio.
    """)
else:
    st.warning("0 registros; Indique la cantidad de datos para el análisis!")
