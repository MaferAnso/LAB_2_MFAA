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
import pandas_datareader.data as web

# -- --------------------------------------------------------- FUNCION: Leer archivo excel -- #

def f_leer_archivo(param_archivo, sheet_name='Sheet 1'):
    """
   Parameters
    ----------
    param_archvo: archivo a leer
  
    Returns
    -------
    df_data: pd.DataFrame con los datos del archivo
   
   
    Debugging
    ---------
    param_archivo: 'archivo_tradeview_1.xlsx'
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
    pips_inst: lista de pips por instrumento
  
    Returns
    -------
    pips_inst: pips del intrumento
    
    Debugging
    ---
    
    """

    inst = param_ins.lower()

    # lista de pips por instrumento
    pips_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                'chfjpy': 100, 'audjpy': 100,
                'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                'audusd': 10000, 'nzdusd': 10000, 'usdchf': 10000, 'eurgbp': 10000,
                'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000, 'gbpnzd': 10000,
                'gbpchf': 10000, 'gbpaud': 10000, 'audnzd': 10000, 'nzdcad': 10000,
                'nzdjpy': 10000, 'audchf': 10000, 'cadchf': 10000, 'gbpcad': 10000, 
                'audcad': 10000, 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pips_inst[inst]


# -- ---------------------------------- FUNCION: Calcular los segundos transcurridos entre el momento de apertura y el momento de cierre de cada operación -- #


def f_columnas_tiempos(param_data):
    """
    Parameters
    ----------
    param_data: pd.Dataframe: tabla con transacciones
  
    Returns
    -------
    param_data: pd.DataFrame: se agrega la columna de tiempo
    
    Debugging
    --------
    
    """

   # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    

    return param_data


# -- ------------------------------------------ FUNCION: Perdida/ganacia experesada en pips -- # #Profesor, para esta parte Oscar me ayudo en clase, antes de la contingencia.

def f_columnas_pips(datos):
    """
    Parameters
    ----------
    datos: pd.DataFrame: tabla con la nueva columna de tiempos
    
    Returns
    -------
    datos: pd.DataFrame : tabla con los pips y pips acumulados
    
    Debugging
    -------
    
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
    datos: pd.DataFrame: tabla con las nuevas columnas de pips y profit_acm
    
    Returns
    -------
    df_1_tabla: pd.DataFrame: tabla en donde aparecen todas las operaciones, perdedoras de venta o compra y las ganadoras de compra o venta
    df_2_ranking: pd.DataFrame: tabla con los ranking de las operaciones con mayores ganancias una vez que fueron cerradas
    
    Debugging
    -------
    
    """
    #Creacion de diccionario con dos llaves
    # Para la creacion de la primera tabla es necesario contar el número total de operaciones que se hicieron en el rango de fechas utilizando la tabla de datos antes creadas, luego, todas aquellas que tienen pips acumulados mayores a 0 son ganadoras, con type, clasificamos las de compra y las de ventas, lo mismo con las perdidas, los pips acumulados menores a 0 son predidas y se clasifican entre compra y venta. Se usa la funcion median para sacar la mediana de los profits y los pips acumulados, para la efectividad se deben de dividir las ganancias totales entre las operaciones totales, para la proporcion debe de dividirse los pips acumulados mayor a cero y los menores a cero luego ganadoras totales entre perdedoras totales, ganadoras de compras entre operaciones totales y ganadoras ventas entre opeoraciones totales.
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
#para la tabla dos de ranking fue necesario sacar los datos del profit mayores a cero y dividirlos, además de acomodarlos de forma ascendete 

    x = pd.DataFrame({i: len(datos[datos.profit>0][datos.symbol == i])/len(datos[datos.symbol == i])
                      for i in datos.symbol.unique()}, index = ['rank']).T
    df_2_ranking = x.sort_values(by='rank', ascending=False)

    return  {'df_1' : df_1_tabla.copy(), 'df_2': df_2_ranking.copy()}

# -- -------------------------------- FUNCION: Una función para saber la evolución del capital en la cuenta de trading, inicializala con 5,000 Usd y ve sumando (restando) las ganancias (perdidas) de la columna 'capital_acm'--#

def f_capital_acm(datos):
    """
    Parameters
    ----------
    datos: pd.Dataframe: tabla con las ganancias y perdidas de las operaciones
   
    Returns
    -------
    datos: pd.DataFrame: tabla con el capital acumulado
    
    Debugging
    -------
    
    """
    datos['capital_acm'] = datos.pips_acm + 5000
    
    return datos.copy()


# -- -------------------------------- FUNCION: Una función para saber las ganancias/perdidas diarias--#

def f_profit_d(datos):
    """
    Parameters
    ----------
    datos: pd.Dataframe: tabla con el capital acumulado
   
    Returns
    -------
    datos: pd.DataFrame: tabla con el timestamp, type, profit_d y profit_acm_d
    
    Debugging
    -------
    
    """
    date=datos.closetime

    df=pd.DataFrame()

    
    df['Timestamp']=pd.date_range(start="2019-08-27", end="2019-09-25", freq='D')
    df['profit_acm_d']=datos['capital_acm']
    df['type']=datos['type']

    for i in range(1,len(df)):
        df.loc[0,'profit_d']=df.loc[0,'profit_acm_d']-5000
        df.loc[i,'profit_d']= df.loc[i,'profit_acm_d']-df.loc[i-1,'profit_acm_d']
        df.sort_values('profit_d', ascending=True)

    return df



   
# -- -------------------------------- FUNCION: Una función para saber los diferentes ratios diarios de la base de datos--#

def f_estadisticas_mad(datos):
    """
    Parameters
    ----------
    datos: pd.Dataframe: tabla con el capital acumulado
   
    Returns
    -------
    datos: pd.DataFrame: tabla con el timestamp, type, profit_d y profit_acm_d
    
    Debugging
    -------
    
    """
    
    #Sharpe Ratio
    pr= datos['capital_acm']
    rp=np.diff(np.log(pr))
    rf=0.08/300

    sharpe_ratio=(np.mean(rp-rf))/np.std(rp)
    
    # Sortino_c (Compras)
    mar=0.3 / 300
    profit_c =f_profit_d(datos[datos['type'] == 'buy'])
    rp_c = np.diff(np.log(profit_c['profit_acm_d']))
    x = []
    for i in range(len(rp_c)):
        if rp_c[i] > mar:
            x.append(rp_c[i])
    std_sortino_c = np.std(x)
    sortino_c = round(np.mean(rp_c - mar) / std_sortino_c,4)

    
    # Sortino_v (ventas)
    profit_v =f_profit_d(datos[datos['type'] == 'sell'])
    rp_v = np.diff(np.log(profit_v['profit_acm_d']))
    y = []
    for i in range(len(rp_v)):
        if rp_v[i] > mar:
            x.append(rp_v[i])
    std_sortino_v = np.std(y)
    sortino_v = round(np.mean(rp_v - mar) / std_sortino_v,4)
    
    #Calcular el drawdown capital
    df = f_profit_d(datos)
    
    valmin = df.profit_acm_d.min()
    rend = df.loc[df['profit_acm_d'] == df.profit_acm_d.min()]
    index = rend.index.tolist()
    val = df.loc[0:index[0]]
    vmax = val.max()
    vmin = val.min()
    vt = vmax['profit_acm_d'] - valmin
    drawdown_cap = list([vmin['Timestamp'], vmax['Timestamp'], vt])
    
    #Calcular el drawup capital
    val2 = df.loc[index[0]:]
    vmax2 = val2.max()
    vmin2 = val2.min()
    vt2 = vmax2['profit_acm_d'] - valmin
    drawup_cap = list([vmin2['Timestamp'], vmax2['Timestamp'], vt2])
    
    
    #Calcular el information Ratio
    
    #Descargar precios masivos (Profesor, utilice una función que vi en simulacion matematica, genere mi token en OANDA varias veces pero no me dejo descargar los precios, decia que no tenia acceso suficiente...... :(    )
    
    def get_historical_closes(ticker, start_date, end_date=None):
        closes = web.YahooDailyReader(ticker, start_date, end_date).read()
    #closes = web.YahooDailyReader(symbols=ticker, start=start_date, end=end_date).read()
    #closes.set_axis(closes.loc['date',:,ticker[0]].values, axis=1, inplace=True)
    #closes = closes.loc['adjclose'].sort_index().dropna()
    #closes = pd.DataFrame(np.array(closes.as_matrix(), dtype=np.float64), columns=ticker, index=closes.index)
    #closes.index.name = 'Date'
        return pd.DataFrame(closes.loc[:, 'Adj Close'])
    #return closes
    
    # Definimos los instrumentos que vamos a descargar. 
    ticker = 'SPY'
    # Queremos los datos desde 27/08/2019 hasta 26/09/2019.
    start_date = '2019-08-27'
    end_date = '2019-09-26'
    # Usamos la función anterior. Si, así de fácil...
    closes = get_historical_closes(ticker, start_date, end_date)
    #Sacamos los rendimientos logaritmicos diarios
    r = np.log(closes/closes.shift(1)).dropna()
    r_mean=r.mean()
    pr= datos['capital_acm']
    rp=np.diff(np.log(pr))
    rp_mean=rp.mean()
    for i in range(len(rp)):
        bench = rp[i] - r
    bench= bench.mean()
    

    inf_ratio = (rp_mean-r_mean)/bench
    

    
    
    
    
    
    mad_data = {'Metrica': ['Sharpe', 'Sortino_c', 'Sortino_v', 'Drawdown_cap', 'Drawup_cap', 'Information_r'],
                'Valor': [sharpe_ratio, sortino_c, sortino_v, drawdown_cap, drawup_cap, inf_ratio],
                'Descripción': ['Sharpe Ratio', 'Sortino Ratio para posiciones de compra',
                                'Sortino Ratio para posiciones de venta', 'DrawDown de Capital', 'DrawUp de Capital',
                                'Information Ratio']}
    df_mad = pd.DataFrame(mad_data)
    return df_mad
    
# -- -------------------------------- FUNCION: Una función para sesgos cognitivos---------------------------------------#

def f_be_de(datos):
    
    # Principio 1: Punto de referencia
    #Proporcion del capital ganado y capital perdido vs capital
    #Utilizar el dataframe de operaciones historicas
    #Calcular el ratio (capital_ganado/capital_acm)*100 y (capital_perdido/capital_acm)*100 para cada operación
    #Nota, hacerlo con una iteración [i]
    
    datos['ratio_capital_acm'] = 0
    datos['ratio_capital_acm'] = [(datos['profit'][i] / 5000) * 100 if i == 0 else
                                  (datos['profit'][i] /datos['capital_acm'][i - 1]) * 100
                                       for i in range(len(datos))]

    
    