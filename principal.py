# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Mafer Anso
# -- repositorio: https://github.com/MaferAnso/LAB_2_MFAA
# -- ------------------------------------------------------------------------------------ -- #


import funciones as fn
# datos de entrada pre-formateados
df_data = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')

# Agregar operaciones con columnas de tiempos
df_data = fn.f_columnas_datos(param_data=df_data)


fn.f_pip_size(param_ins='usdjpy')



