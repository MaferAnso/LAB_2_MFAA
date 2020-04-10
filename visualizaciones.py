# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: visualizaciones.py - para visualizacion de datos
# -- mantiene: Mafer Anso
# -- repositorio: https://github.com/MaferAnso/LAB_2_MFAA
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import numpy as np
import funciones as fn

# Funcion para leer los datos
datos1 = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx', sheet_name = 0)

datos1

# Agregar columna de tiempo
datos2 = fn.f_columnas_tiempos(datos)

datos2

#Agregar columna de pips
datos3 = fn.f_columnas_pips(datos)

datos3

#Agregar columna de capital acumulado
datos4 = fn.f_capital_acm(datos)

datos4

#Estadisticas de la tabla
stats= fn.f_estadisticas_ba(datos)

stats

#Crear un nuevo dataframe con los profits diarios
df = fn.f_profit_d(datos)
df

#Creacion de tabla con metricas  
mad= fn.f_estadisticas_mad(datos)

mad
# Creación de tabla sobre los sesgos cognitivos 

sesgos = fn.f_be_de(datos)

sesgos