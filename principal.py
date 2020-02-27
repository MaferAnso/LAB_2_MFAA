# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - flujo principal del proyecto
# -- mantiene: Mafer Anso
# -- repositorio: https://github.com/MaferAnso/LAB_2_MFAA
# -- ------------------------------------------------------------------------------------ -- #


import funciones as fn

datos = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')
fn.f_pip_size(param_ins='usdjpy')
datos = fn.f_columnas_datos(param_data=datos)
