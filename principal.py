# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Mafer Anso
# -- repositorio: https://github.com/MaferAnso/LAB_2_MFAA
# -- ------------------------------------------------------------------------------------ -- #




import funciones as fn

# Funcion para leer los datos
datos = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx', sheet_name = 0)

# Agregar columna de tiempo
datos = fn.f_columnas_tiempos(datos)

#Agregar columna de pips
datos = fn.f_columnas_pips(datos)

#Agregar columna de capital acumulado
datos = fn.f_capital_acm(datos)

#Estadisticas de la tabla
stats = fn.f_estadisticas_ba(datos)

#Crear un nuevo dataframe con los profits diarios
datos_profit = fn.f_profit_d(datos)

#Creacion de tabla con metricas  
mad= fn.f_estadisticas_mad(datos)

# Creación de tabla sobre los sesgos cognitivos 

sesgos = fn.f_be_de(datos)

