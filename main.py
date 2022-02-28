# This is a sample Python script.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Pasamos a variables los nombres de los ficheros
file_accident = 'accident-data.csv'
file_road = 'road-safety-lookups.csv'
# Cargamos los ficheros a DataFrames
accidents = pd.read_csv(file_accident)
roads = pd.read_csv(file_road)
# obtenemos los nombres de las columnas y las pasamos a una lista
column=accidents.columns
print("Los nombres de las columnas son: ")
print(column)
# Nos quedamso con las columnas inicialmente necesarias
accid = accidents[['accident_index', 'time', 'day_of_week', 'date', 'accident_severity']]
print(accid.shape)
accid.drop_duplicates()
print(accid.shape)
# Concatenamos las columnas date y time para tener en una misma columna la fecha y hora en formato DATETIME
#accid.loc[:, 'datetime'] = pd.to_datetime(accid.loc[:, 'date'] + ' ' + accid.loc[:, 'time'])
# Creamos una nueva columna en la que nos quedamso sólo con las horas
#accid['hour'] = accid['datetime'].dt.hour

# Agrupamos por día de la semana y hora y hacemos la cuenta para comprobar qué días de la semana y a qué horas hay
# más accidentes
#accid_by_time = accid.groupby(['day_of_week', 'hour'])['accident_index'].count()
#print(accid_by_time)
"""
accid_by_time.plot(kind='bar', color='g')
plt.xlabel("Day of Week / hour")
plt.ylabel("Number of accidents")
plt.title("Distribution of Number of accidents by day of week and hour")
plt.show()
# La hora con mayor número de accidentes es a las 17h, siendo mayor los días 6 y 5 (Viernes y jueves)
# El mayor número de accidentes se concentran entre las 16 y las 18h los días entre semana
# A las 8h hay un pico de accidentes en los días entre semana.

sns.relplot(x='hour', y=accid_by_time, data=accid_by_time, kind='line', hue='day_of_week')
plt.ylabel("Number of accidents")
plt.title("Distribution of Number of accidents by day of week and hour")
plt.legend(labels=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], title = "Day of Week")
plt.show()

# Analizamos únicamente número de accidentes por día de la semana
# Agrupamos por día de la semana y lo mostramos en plot para mayor comprensión
accid_by_day=accid.groupby('day_of_week')['accident_index'].count()
print(accid_by_day)
hue_colors={1:'#d800ff', 2:'#be00e1', 3:'#ab00ca', 4:'#8d00a7', 5:'#6f0084', 6:'#540064', 7:'#360040'}
sns.countplot(x='day_of_week', data=accid, palette= hue_colors)
plt.xticks(np.arange(0,7,1), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'))
plt.xlabel('')
plt.ylabel("Number of accidents")
plt.title("Number of accidents by day of week")
plt.show()
#accid_by_day.plot(kind='bar')
#plt.show()

# Se comprueba que el número de accidentes se concentra en los días entre semana, siendo mayores los jueves y viernes
# Se concluye que en las horas de salida del trabajo se concentra el mayor número de accidentes
# Los fines de semana, el número de accidentes cambia su distribución, produciendose el mayor número de accidentes
# en las horas centrales del día, sobre las 14h

# Ahora analizamos estos datos, pero nos quedamos sólo con los incidentes importantes.
# Los incidentes importantes se distribuyen en la columna accident_severity con valor 1 (fatal)
# Analizamos en primer lugar por días de la semana
accid_by_day_fatal=accid[accid['accident_severity']==1].groupby('day_of_week')['accident_severity'].count()
print(accid_by_day_fatal.sort_values(ascending=True))
sns.countplot(x='day_of_week', data=accid[accid['accident_severity']==1], palette= hue_colors)
plt.xticks(np.arange(0,7,1), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'))
plt.xlabel('')
plt.ylabel("Number of accidents")
plt.title("Number of major accidents by day of week")
plt.show()

# Analizamos por día de la semana y hora
accid_by_day_fatal_time=accid[accid['accident_severity']==1].groupby(['day_of_week', 'hour'])['accident_severity'].count()
print(accid_by_day_fatal_time.sort_values(ascending=False))
accid_by_day_fatal_time.plot(kind='bar')
plt.xlabel("Day of Week / hour")
plt.ylabel("Number of accidents")
plt.title("Distribution of Number of major accidents by day of week and hour")
plt.show()


sns.relplot(x='hour', y=accid_by_day_fatal_time, data=accid_by_day_fatal_time, kind='line', hue='day_of_week')
plt.ylabel("Number of accidents")
plt.title("Distribution of Number of major accidents by day of week and hour")
plt.show()
"""
"""
# Analizaremos la relacion entre accidentes graves por día de la semana y la hora
accid_day_fatal_ind=accid[accid['accident_severity']==1]['day_of_week']
accid_hour_fatal_ind=accid[accid['accident_severity']==1]['hour']

# Construimos un heatmap para ver la relacion
#sns.heatmap(pd.crosstab(accid_hour_fatal_ind,accid_day_fatal_ind))
#plt.show()
# Se aprecian ciertas relaciones entre las horas y os días dela semana. Para poder analizar en detalle procedemos:
# Agrupamos las horas en 4 grupos. Mañana, mediodía, noche y madrugada
hour_interval=['midnight', 'morning', 'afternoon', 'night']
hour_num=[0, 6, 12, 18, 23]
accid['time_interval']=pd.cut(accid['hour'], bins=hour_num, labels=hour_interval, ordered=False)
print(accid['time_interval'])
# volvemos a construir el heatmap
accid_interval_fatal_ind=accid[accid['accident_severity']==1]['time_interval']
sns.heatmap(pd.crosstab(accid_interval_fatal_ind, accid_day_fatal_ind), annot=True, cbar=False, cmap="YlGnBu", linewidths=1.5)
plt.xticks(np.arange(0,7,1), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'))
plt.xlabel('')
plt.ylabel('')
plt.title('Heatmap to finde the relation between day of day and hour/interval of time')
plt.show()
# Si observamos, existe una relación entre ciertos días y ciertas horas del día. Si bien es cierto que el mayor
# número de accidentes graves se da el sábado por la tarde. Hay una relación en que los días laborables por la tarde se
# concentra el mayor número de accidentes, bajando este número a las horas de madrugada. Se observa también un
# incremento de estos accidentes los jueves por la mañana.
# CONCLUSION: Existen principalmente dos motivos en los que se dan estos accidentes graves:
# 1. Debido a la mobilidad laboral, concentrandose en las horas de la tarde
# 2. Debido a la mobilidad por ocio, concentrandose en als hroas de la tarde, noche y madrugada
"""
# 3. What characteristics stand out in major incidents compared with other accidents?
""" 
# Vamos a ir analizando las caracteristicas principales, comparando entre accidentes fatales y no fatales
# Las principales caracteristicas que vamos a analizar son: 
Caracteristicas a estudiar:
- accident_severity: 1: Fatal; 2,3: Non-fatal
- time: day of week; hour, month
- road class:
- road type
- speed limit
- pedestrian crossing physical facilities
- light conditions
- weather conditions
- road surface conditions
- urban or rural
"""
# Creamos un nuevo DataFrame con las caracteristicas a estudiar
#accid_major=accidents[accidents['accident_severity']==1]
accidents_=accidents[['accident_severity', 'day_of_week', 'time', 'first_road_class', 'first_road_number', 'road_type', 'speed_limit',
                         'pedestrian_crossing_physical_facilities', 'light_conditions', 'weather_conditions',
                         'road_surface_conditions', 'urban_or_rural_area']]
print(accidents_.shape)
accidents_['fatal_or_not']=accidents_.apply(lambda x: 'fatal' if x["accident_severity"]==1 else "not_fatal", axis=1)
"""
# calculo el total de accidentes por accident_severity
fatal_accidents=accidents_['accident_severity'][accidents_['accident_severity']==1].count()
serious_accidents=accidents_['accident_severity'][accidents_['accident_severity']==2].count()
slight_accidents=accidents_['accident_severity'][accidents_['accident_severity']==3].count()
total=fatal_accidents+serious_accidents+slight_accidents
fatal_per=fatal_accidents/total
serious_per=serious_accidents/total
slight_per=slight_accidents/total
print("Total fatal: ")
print(fatal_per)
print("Total serious: ")
print(serious_per)
print("Total slight: ")
print(slight_per)
"""
"""
# A continuación mostramos 8 gráficos buscando cuál de estas caracteristicas tiene distinto comportamiento
fig, ax= plt.subplots(nrows=4, ncols=2, figsize=(17,7))

# Distribución de accidentes por first road class
ax[0,0]=sns.countplot(x='first_road_class', data=accidents_, hue='fatal_or_not', ax=ax[0,0])
# No hay diferencia significativa
# Distribución de accidentes por road_type
ax[0,1]=sns.countplot(x='road_type', data=accidents_, hue='fatal_or_not', ax=ax[0,1])
# No hay diferencia significativa
# Distribución de accidentes por speed_limit
ax[1,0]=sns.countplot(x='speed_limit', data=accidents_, hue='fatal_or_not', ax=ax[1,0])
# En los accidentes fatales se observa mayor incidencia en niveles de 60, en comparación con los no fatales
# Distribución de accidentes por pedestrian_crossing_physical_facilities
ax[1,1]=sns.countplot(x='pedestrian_crossing_physical_facilities', data=accidents_, hue='fatal_or_not', ax=ax[1,1])
# No hay diferencia significativa
# Distribución de accidentes por plight_conditions
ax[2,0]=sns.countplot(x='light_conditions', data=accidents_, hue='fatal_or_not', ax=ax[2,0])
# No hay diferencia significativa
# Distribución de accidentes por weather_conditions
ax[2,1]=sns.countplot(x='weather_conditions', data=accidents_, hue='fatal_or_not', ax=ax[2,1])
# No hay diferencia significativa
# Distribución de accidentes por road_surface_conditions
ax[3,0]=sns.countplot(x='road_surface_conditions', data=accidents_, hue='fatal_or_not', ax=ax[3,0])
# No hay diferencia significativa
# Distribución de accidentes por urban_or_rural_area
ax[3,1]=sns.countplot(x='urban_or_rural_area', data=accidents_, hue='fatal_or_not', ax=ax[3,1])

plt.show()
"""
# Sí se encuentra unaa mayor incidencia de accidentes fatales en rural que en urban

# On what areas would you recommend the planning team focus their brainstorming efforts to reduce major incidents?
# Primero vamos a comprobar el nivel total de accidentes por area
sns.countplot(x='urban_or_rural_area', data=accidents_)
plt.show()
#En general hay más accidentes en entornos urbanos que en rural
sns.countplot(x='urban_or_rural_area', data=accidents_[accidents_['fatal_or_not']=='fatal'])
plt.show()
# En los accidentes fatales, la incidencia es mayor en áreas rurales.
fig, ax= plt.subplots(nrows=2, ncols=2, figsize=(17,7))
ax[0,0]=sns.countplot(x='urban_or_rural_area', data=accidents_, hue='weather_conditions', ax=ax[0,0])
ax[0,1]=sns.countplot(x='urban_or_rural_area', data=accidents_, hue='speed_limit', ax=ax[0,1])
# Hay diferencia sobre el límite de velocidad. EN entornos rurales, los accidentes se dan en velocidades de 60, mientras que en urbanos a 30
ax[1,0]=sns.countplot(x='urban_or_rural_area', data=accidents_, hue='light_conditions', ax=ax[1,0])
# Hay un dato destacable en áreas rurales. Es caracteritico las condiciones de "Darkness - no lighting
ax[1,1]=sns.countplot(x='urban_or_rural_area', data=accidents_, hue='road_surface_conditions', ax=ax[1,1])
plt.show()
