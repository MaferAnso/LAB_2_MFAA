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
    :param sheet_name
    :return
    Debugging
    ---------
    param_archivo
    """

    # Leer archivo
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name=sheet_name)

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

    # encontrar y eliminar _
    # inst = param_ins.replace('_', '')

    # transformar a minusculas
    param_ins = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'eurusd': 10000,'de30usd': 10000,'gbpusd': 10000,'audusd': 10000,'usdcad': 100,'nzdjpy': 100}
    return pips_inst[param_ins]


# -- ---------------------------------- FUNCION: Calcular el tiempo de una posición abierta -- #


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

    # convertir columna de 'closetime' y 'opentime' utilizando pd.to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # tiempo transcurrido de una operacion
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in param_data.index]

    return param_data['tiempo']


# -- ------------------------------------------ FUNCION: Perdida/ganacia experesada en pips -- #


def f_columnas_pips(param_data):
    """
    Parameters
    ----------
    param_data : 
    Returns
    -------
    df_data : pd.DataFrame :
    Debugging
    ---------
    param_archivo
    
    """
    param_data['pips'] = np.zeros(len(param_data['type']))
    
    for i in range(0,len(param_data['type'])):
        
        if param_data['type'][i] == 'buy':
            
            param_data['pips'][i] = (param_data.closeprice[i] - param_data.openprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
            
        else:
            
            param_data['pips'][i] = (param_data.openprice[i] - param_data.closeprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
    
    param_data['pips_acm'] = np.zeros(len(param_data['type']))
    param_data['profit_acm'] = np.zeros(len(param_data['type']))    
    param_data['pips_acm'][0] = param_data['pips'][0]
    param_data['profit_acm'][0] = param_data['profit'][0]
            
    for i in range(1,len(param_data['pips'])):
        
         param_data['pips_acm'][i] = param_data['pips_acm'][i-1] + param_data['pips'][i]
            param_data['profit_acm'][i] = param_data['profit_acm'][i-1] + param_data['profit'][i]
        
    return param_data


def f_estdisticas_ba (param_data):

    def rank_currency(currency,data):
        data = data.loc[data["symbol"]==currency]
        proportion = len(data.loc[data["profit"]>0])/len(data)
        return proportion



    measure_names = ["Ops totales", "Ganadoras","Ganadoras_c","Ganadoras_v","Perdedoras","Perdedoras_c","Perdedoras_v",
                     "Media(Profit)","Media(pips)","r_efectividad","r_proporción","r_efectividad_c","r_efectividad_v"]
    df1_tabla = pd.DataFrame()
    median = lambda data: data.iloc[int((len(data)+1)/2)] if len(data)%2 != 0 else (data.iloc[int(len(data)-1)] +
                                                                                    data.iloc[int((len(data)+1)/2)])

    measures = {'Ops totales': len(param_data),
               'Ganadoras':len(param_data.loc[param_data["profit"] > 0]),
               'Ganadoras_c': len(param_data.loc[(param_data["type"] == "buy") & (param_data["profit"] > 0)]),
               'Ganadoras_v': len(param_data.loc[(param_data["type"] == 'sell') & (param_data["profit"] > 0)]),
               'Perdedoras': len(param_data.loc[param_data["profit"] < 0]),
               'Perdedoras_c': len(param_data.loc[(param_data["type"] == "buy") & (param_data["profit"] < 0)]),
               'Perdedoras_v': len(param_data.loc[(param_data["type"] == "sell") & (param_data["profit"] < 0)]),
               'Media(Profit)' : median(param_data["profit"]),
               'Media(pips)': median(param_data["pips"]),
               'r_efectividad': len(param_data.loc[param_data["profit"]>0])/len(param_data["profit"]),
               'r_proporción': len(param_data.loc[param_data["profit"]<0])/len(param_data["profit"]),
               'r_efectividad_c':len(param_data.loc[(param_data["type"]=="buy") & (param_data["profit"]>0)])/len(
                                     param_data["profit"]),
               'r_efectividad_v':len(param_data.loc[(param_data["type"]=="sell") & param_data["profit"]<0])/len(
                                     param_data["profit"])

                                   }

    traded_currencies = param_data["symbol"].unique()
    df2_ranking = pd.DataFrame({"Symbol":traded_currencies,"rank":0})
    df2_ranking["rank"]= (list((rank_currency(i,param_data)) for i in traded_currencies))
    df2_ranking=df2_ranking.sort_values(by="rank",ascending=False)

    df1_tabla["Medias"] = list([measures[i] for i in measure_names])

    stats_dict = {'df_1_tabla':df1_tabla,
                  'df_2_ranking': df2_ranking}
    return stats_dict


