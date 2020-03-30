# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Mafer Anso
# -- repositorio: https://github.com/MaferAnso/LAB_2_MFAA
# -- ------------------------------------------------------------------------------------ -- #


import funciones as fn

# Funcion para leer los datos
datos = fn.f_leer_archivo(param_archivo='archivos/archivo_tradeview_1.xlsx', sheet_name= 0)

# Agregar columna de  tiempo de la operación
datos = fn.f_columnas_tiempos(datos)

# Agregar columna de número de pips
datos = fn.f_columnas_pips(datos)

# Agregar columna de capital acumulado ($)
datos = fn.f_capital_acm(datos)

# Función donde se calculan las estadísticas básicas
stats = fn.f_basic_stats(datos)

# Estadísticas de desempeño de movimientos
profit_d = fn.f_profit_diario(datos)

