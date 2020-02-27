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

    Parameters
    -------

    """

    # Leer archivo de datos y guardarlo en un DataFrame
    df_data = pd.read_excel('archivos/'+param_archivo, sheet_name='Hoja1')

    # Convertir en minusculas el nombre de las columnas haciendo compresión de listas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0,len(df_data.columns))]

    # Asegurar que ciertas columnas son del tipo numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap',
               'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)


    return df_data

def f_pip_size(param_ins):
    """
    Parameters
    ---------
    param_ins

    Returns
    -------
    object
    """

    # transformar a minusculas
    inst = param_ins.lower()

    # lista de pips por instrumentos
    pip_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy':100, 'cadjpy': 100,
                'chfjpy':100, 'eurusd':10000}

    return  pip_inst[inst]

def f_columnas_datos (param_data):
    """

    Returns
    -------
    object
    """

    # Convertir columna de 'closetime' y 'opentime' utilizando pd.to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    # tiempo transcurrido de una operacion
    param_data['tiempo']= [(param_data.loc[i, 'closetime'] -
                                 param_data.loc[i, 'opentime']).delta/1e9
                                for i in range(0, len(param_data['closetime']))]

    return
