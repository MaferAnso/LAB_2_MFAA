# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para procesamiento de datos
# -- mantiene: Mafer Anso
# -- repositorio: https://github.com/MaferAnso/LAB_2_MFAA
# -- ------------------------------------------------------------------------------------ -- #

# -- ---------------------------------------------------------FUNCION: Leer archivo para  -- #

import numpy as np  
from datetime import timedelta 
import pandas as pd  




# -- --------------------------------------------------------- FUNCION: Leer archivo excel -- #

def f_leer_archivo(param_archivo, sheet_name='Sheet 1'):
    """
   Parameters
    ----------
  
    Returns
    -------
    :param param_archivo
   
    :return
    Debugging
    ---------
    param_archivo
    """

    # Leer archivo
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name = 0)

    # Convertir en minusculas los titulos de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]

    # Elegir renglones type == buy | type == sell
    df_data = df_data[df_data.type != 'balance']

    # Resetear indice
    df_data = df_data.reset_index()

    # Asegurar ciertas columnas de tipo numerico
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    return df_data


# -- -------------------------------- FUNCION: Diccionario de instrumentos y tamaño del pip -- #

def f_pip_size(param_ins):
    """
    Parameters
    ----------
  
    Returns
    -------
    :param param_ins
    :return
    Dwbugging
    ---
    param_inst
    """

    inst = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                 'chfjpy': 100,
                 'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                 'audusd': 10000, 'nzdusd': 10000,
                 'usdchf': 10000,
                 'eurgbp': 10000, 'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000,
                 'gbpnzd': 10000, 'gbpchf': 10000, 'gbpaud': 10000,
                 'audnzd': 10000, 'nzdcad': 10000, 'audcad': 10000,
                 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pips_inst[inst]


# -- ---------------------------------- FUNCION: Calcular los segundos transcurridos entre el momento de apertura y el momento de cierre de cada operación -- #


def f_columnas_tiempos(param_data):
    """
   Parameters
    ----------
  
    Returns
    -------
    :param param_data
    :return
    Debugging
    --------
    param_data
    """

   # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    

    return param_data


# -- ------------------------------------------ FUNCION: Perdida/ganacia experesada en pips -- #

def f_columnas_pips(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : df con información de transacciones ejecutadas en Oanda,
                                después de haber ejecutado f_columnas_tiempos
    Returns
    -------
    param_data : pandas.DataFrame : df modificado
    Debugging
    -------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    """

    datos['pips'] = [(datos.closeprice[i]-datos.openprice[i])*f_pip_size(datos.symbol[i]) for i in range(len(datos))]
    datos['pips'][datos.type=='sell'] *= -1
    datos['pips_acm'] = datos.pips.cumsum()
    datos['profit_acm'] = datos['profit'].cumsum()
    
    return datos.copy()
# -- -------------------------------- FUNCION: Una función cuya salida sea un diccionario, ese diccionario de salida debe de tener 2 llaves, 'df_1_tabla' y 'df_2_ranking -- #

def f_estadisticas_ba(datos):
    """
    Parameters
    ----------
   
    -------
 
    Debugging
    -------
    
    """
    df_1_tabla = pd.DataFrame({
        'Ops totales': [len(datos['order']), 'Operaciones totales'],
        'Ganadoras': [len(datos[datos['pips_acm']>=0]), 'Operaciones ganadoras'],
        'Ganadoras_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']>=0)]), 'Operaciones ganadoras de compra'],
        'Ganadoras_s': [len(datos[(datos['type']=='sell') & (datos['pips_acm']>=0)]), 'Operaciones ganadoras de venta'],
        'Perdedoras': [len(datos[datos['pips_acm'] < 0]), 'Operaciones perdedoras'],
        'Perdedoras_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']<0)]), 'Operaciones perdedoras de compra'],
        'Perdedoras_s': [len(datos[(datos['type']=='sell') & (datos['pips_acm']<0)]), 'Operaciones perdedoras de venta'],
        'Mediana_profit': [datos['profit'].median(), 'Mediana de rendimeintos de las operaciones'],
        'Mediana_pips': [datos['pips_acm'].median(), 'Mediana de pips de las operaciones'],
        'r_efectividad': [len(datos[datos['pips_acm']>=0])/len(datos['order']),
                          'Ganadoras Totales/Operaciones Totales'],
        'r_proporcion': [len(datos[datos['pips_acm']>=0])/len(datos[datos['pips_acm'] < 0]),
                            'Ganadoras Totales/ Perdedoras Totales'],
        'r_efectividad_c': [len(datos[(datos['type']=='buy') & (datos['pips_acm']>=0)])/len(datos[datos['type']=='buy']),
                            'Ganadoras Compras/ Operaciones Totales'],
        'r_efectividad_v': [len(datos[(datos['type']=='sell') & (datos['pips_acm']>=0)])/len(datos[datos['type']=='sell']),
                            'Ganadoras Ventas/ Operaciones Totales']},index=['Valor', 'Descripcion'])


    tmp = pd.DataFrame({i: len(datos[datos.profit>0][datos.symbol == i])/len(datos[datos.symbol == i])
                      for i in datos.symbol.unique()}, index = ['rank']).T
    df_2_ranking = tmp.sort_values(by='rank', ascending=False).T

    return  {'df_1' : df_1_tabla.copy(), 'df_2': df_2_ranking.copy()}

# -- -------------------------------- FUNCION: Una función para saber la evolución del capital en la cuenta de trading, inicializala con 5,000 Usd y ve sumando (restando) las ganancias (perdidas) de la columna 'profit_acm'--#

def f_capital_acm(datos):
    """
    Parameters
    ----------
   
    Returns
    -------
    
    Debugging
    -------
    
    """
    datos['capital_acm'] = datos.profit_acm + 5000
    
    return datos.copy()


# -- -------------------------------- FUNCION: Una función para saber las fechas en las cuales se hizo traiding--#


def f_profit_diario(datos):
    """
    Parameters
    ----------
  
    Returns
    -------
    
    -------
    
    """
    datos['ops'] = [i.date() for i in datos.closetime] # cantidad de operaciones cerradas ese dia
    diario = pd.date_range(datos.ops.min(),datos.ops.max()).date
    #groups = datos.groupby('ops')
    #profit = groups['profit'].sum()
    #profit_d = [profit[i] if i in profit.index else 0 for i in diario]
    df_profit_diario = pd.DataFrame(profit_diario,index = diario,columns = ['timestamp','capital_acm']).cumsum()+5000
    
    return df_profit_diario

def f_estadisticas_mad(datos):
     """
    Parameters
    ----------
  
    Returns
    -------
    
    -------
    
    """


