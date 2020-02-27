# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Mafer Anso
# -- repositorio: https://github.com/MaferAnso/LAB_2_MFAA
# -- ------------------------------------------------------------------------------------ -- #

# -- ---------------------------------------------------------FUNCION: Leer archivo para  -- #

import pandas as pd

def f_leer_archivo(param_archivo):
    """

    Returns
    -------
    object
    """

    # Leer archivo de datos y guardarlo en un DataFrame
    df_data = pd.read_excel('archivos/'+param_archivo, sheet_name='Hoja1')

    # Convertir en minusculas el nombre de las columnas haciendo compresión de listas
    df_data.columns = [list(df_data.colums)[i].lower()
                       for i in range(0,len(df_data.colums))]

    # Asegurar que ciertas columnas son del tipo numerico
    numcols = ['s/l', 't/p', 'comission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
               'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)


    return df_data

