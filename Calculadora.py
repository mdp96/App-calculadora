#!/usr/bin/env python
# coding: utf-8

# # 1. Imports

# In[1]:


import pandas as pd
import streamlit as st


# # 2. Lectura de datos

# In[2]:


path = r"C:\Users\mdepaz\OneDrive - Improven Consulting, SL\Proyectos internos\1. Calculadora"
file1 = "\Tabla1.csv"
file2 = "\Tabla2.csv"
file3 = "\Tabla2.2.csv"
file4 = "\Tabla3.csv"
file5 = "\Tabla3.3.csv"
file6 = "\Tabla4.csv"

t1 = pd.read_csv(path + file1,sep =';')
t2 = pd.read_csv(path + file2,sep =';')
t22 = pd.read_csv(path + file3,sep =';')
t3 = pd.read_csv(path + file4,sep =';')
t33 = pd.read_csv(path + file5,sep =';')
t4 = pd.read_csv(path + file6,sep =';')


# # 3. Parámetros

# In[3]:


# area = 'COMERCIAL'
# puesto = 'D.COMERCIAL'
# trabajador = 'JAVIER'
# nivel = 'N3: 8 - 10 AÑOS'
# nivel_g = 'N3: 8 - 10 AÑOS'


#with st.form(key='Calculadora'):
dummy = 'Selecciona una opción'
error1 = 'No has seleccionado un área o departamento'
areas = t1['ÁREA'].drop_duplicates().to_list()

st.header('Calculadora de retribuciones')
area = st.selectbox('Área / Departamento',options = [dummy] + areas,index = 0)

if area is not dummy:
    puestos = t1[t1['ÁREA'] == area]['PUESTO'].drop_duplicates().to_list()
    puesto = st.selectbox('Puesto',[dummy] + puestos, index = 0)

else:
    puesto = st.selectbox('Puesto',[error1])


if (puesto is not dummy) and (puesto is not error1):
    trabajadores = t1[(t1['ÁREA'] == area) & (t1['PUESTO'] == puesto)]['NOMBRE'].drop_duplicates().to_list()
    trabajador = st.selectbox('Empleado',[dummy]+trabajadores, index = 0)
else:
    trabajador = st.selectbox('Trabajador',['No has seleccionado un puesto'])


niveles = t22['Nivel'].drop_duplicates().to_list()
nivel = st.selectbox('Nivel',[dummy] + niveles, index = 0)
nivel_g = st.selectbox('Nivel Gerencia',[dummy] + niveles, index = 0)

#    submit_button = st.form_submit_button('Calcular')





# In[7]:


# area = 'CAD'
# puesto = 'D.CAD'
# trabajador = 'MAR'
# nivel = 'N3: 8 - 10 AÑOS'
# nivel_g = 'N3: 8 - 10 AÑOS'


# # 4. Cálculos

# In[8]:


#bs = pd.DataFrame(columns = ['Banda salarial actual','Banda salarial Responsable','Banda salarial Gerencia','PROPUESTA DE RETRIBUCIÓN','DIFERENCIA DE RETRIBUCIÓN'])

bs = pd.DataFrame(columns = ['Banda \n salarial \n actual','Banda \n salarial \n Responsable',
                             'Banda \n salarial \n Gerencia','PROPUESTA \n DE RETRIBUCIÓN','DIFERENCIA \n DE RETRIBUCIÓN'])


# In[9]:


bsact = float(t4[(t4['NOMBRE'] == trabajador) & (t4['PUESTO'] == puesto)]['SALARIO BRUTO AÑO'].iloc[0].replace(',','.'))
bsresp = float(t33[(t33['PUESTO']==puesto) & (t33['Nivel']==nivel)]['Rango Retributivo'].iloc[0].replace(',','.'))
bsger = float(t33[(t33['PUESTO']==puesto) & (t33['Nivel']==nivel_g)]['Rango Retributivo'].iloc[0].replace(',','.'))
propret = 0.5*(bsresp+bsger)
difret = propret-bsact


# In[10]:


bsresp = float(t33[(t33['Nivel']==nivel) & (t33['PUESTO'] == puesto)]['Rango Retributivo'].to_list()[0].replace(',','.'))


# In[11]:


bs.loc[len(bs)] = [round(bsact,2),round(bsresp,2),round(bsger,2),round(propret,2),round(difret,2)]


# In[12]:


v = pd.DataFrame(columns = ['Valoración Responsable','Valoración Gerencia','Nivel Esperado - Comparador Responsable',
                            'Nivel Esperado - Comparador Gerencia','Diferencia Nivel - Valoración Responsable',
                            'Diferencia Nivel - Valoración Gerencia'])

zoom = pd.DataFrame(columns = ['ID','Conocimientos Técnicos','Valoración Responsable','Valoración Gerencia',
                               'Nivel Esperado - Comparador Responsable','Nivel Esperado - Comparador Gerencia',
                               'Diferencia Nivel - Valoración Responsable','Diferencia Nivel - Valoración Gerencia'])


# In[13]:


IDS = t1[t1['NOMBRE']==trabajador]['ID CONOCIMIENTO'].to_list()
IDS = list(map(int,IDS))
conoc = t1[t1['NOMBRE']==trabajador]['CONOCIMIENTO'].to_list()
valres = t1[t1['NOMBRE']==trabajador]['VALORACIÓN'].to_list()
valres = list(map(int, valres))
# valger = t1[t1['NOMBRE']==trabajador]['VALORACIÓN GERENCIA'] # actualmente no existe pero si se crea un campo de 
# evaluación por gerencia, bastará con descomentar esta línea y adecuar el nombre de la columna que contenga esa información
# Aun así, para poder seguir con el código y que los cálculos funciones, vamos a crear una lista con todos los valores igual
# a 0, simulando ser esa la puntuación por gerencia
valger = [0]*len(valres)

necr = []
necg = []

for i in range(0,len(IDS)):
    val = t22[(t22['ID CONOCIMIENTO']==IDS[i]) & (t22['CONOCIMIENTO']==conoc[i]) & (t22['Nivel']==nivel)]['Valor'].to_list()[0]
    val_g = t22[(t22['ID CONOCIMIENTO']==IDS[i]) & (t22['CONOCIMIENTO']==conoc[i]) & (t22['Nivel']==nivel_g)]['Valor'].to_list()[0]
    necr.append(int(val))
    necg.append(int(val_g))

zoom['ID'] = IDS
zoom['Conocimientos Técnicos'] = conoc
zoom['Valoración Responsable'] = valres
zoom['Valoración Gerencia'] = valger
zoom['Nivel Esperado - Comparador Responsable'] = necr
zoom['Nivel Esperado - Comparador Gerencia'] = necg

zoom['Diferencia Nivel - Valoración Responsable'] = zoom['Valoración Responsable'] - zoom['Nivel Esperado - Comparador Responsable']
zoom['Diferencia Nivel - Valoración Gerencia'] = zoom['Valoración Gerencia'] - zoom['Nivel Esperado - Comparador Gerencia']


for col in v.columns:
    total= int(zoom[col].sum(axis=0))
    v.loc[0,col]= total


# # 5. Frontend

# In[14]:


def highlight_cells(val):
    if val > 0:
        color = 'green'
    elif val < 0:
        color = 'red'
    else:
        return ''  # No aplicar ningún estilo si es 0
    return f'color: {color}'

def formato_euro(val):
    return f"{val:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

if st.button('Calcular'):
    BS = bs.style.applymap(highlight_cells, subset=['DIFERENCIA \n DE RETRIBUCIÓN']).format(formato_euro)
    st.markdown(
    """
    <style>
    /* Ajustar el tamaño del texto de los encabezados */
    .dataframe thead th {
        word-wrap: break-word;
        white-space: normal;
        height: 150px;
    }
    </style>
    """, unsafe_allow_html=True
)
    st.dataframe(BS,width = 700, height = 100, hide_index = True)
    st.dataframe(v,width = 700, height = 100, hide_index = True)
    st.dataframe(zoom,width = 700, height = 40*len(zoom),hide_index = True)
    
    st.write(BS)
    
    col1,col2 = st.columns(2)
    value = bs['Banda \n salarial \n actual'].iloc[0]
    delta = bs['DIFERENCIA \n DE RETRIBUCIÓN'].iloc[0]
    value_f = f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') + " €"
    delta_f = f"{delta:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') + " €"
    
    col1 = st.metric(label = 'Banda salarial',value = value_f, 
                     delta =  delta_f)
    
    
    


# # 6. Comentarios

# numero_formateado = "{:,.2f}".format(numero).replace(',', 'X').replace('.', ',').replace('X', '.')
# 
# Base de datos son SQLite debería funcionar y si escala a algo muy grande podemos migrarlo a postgreSQL. También se puede 
# usar la base de datos para guardar usuarios y contraseñas e incluso se pueden cifrar.
# 
# En streamlit, cuando se implemente, podemos hacer por ahora que el excel se lea tipo drop file here

# # 7. Mejoras

# 1. Se puede implementar que cuando una selección no tenga más que una opción en sus subselecciones, el programa coja esa opción única por defecto, si necesidad de que el usuario tenga que especificarla.
# 2. Información del excel que se comunique por web con un widget tipo "drop file"
# 3. Conectar con BBDD que tengan para hacer los cuestionarios o crear directamete un apartado de cuestionario en la app web
# 

# In[ ]:




