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
from oandapyV20 import API                               
import oandapyV20.endpoints.instruments as instruments



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


# -- ------------------------------------------ FUNCION: Perdida/ganacia experesada en pips -- #

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


# -- --------------------------------------------------------- FUNCION: Descargar precios -- #
# -- --------------------------------------------------------------------------------------- #
# -- Descargar precios historicos con OANDA

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Parameters
    ----------
    p0_fini : str : fecha inicial para descargar precios en formato str o pd.to_datetime
    p1_ffin : str : fecha final para descargar precios en formato str o pd.to_datetime
    p2_gran : str : M1, M5, M15, M30, H1, H4, H8, segun formato solicitado por OANDAV20 api
    p3_inst : str : nombre de instrumento, segun formato solicitado por OANDAV20 api
    p4_oatk : str : OANDAV20 API
    p5_ginc : int : cantidad de datos historicos por llamada, obligatorio < 5000
    Returns
    -------
    dc_precios : pd.DataFrame : Data Frame con precios TOHLC
    Debugging
    ---------
    p0_fini = pd.to_datetime("2019-01-01 00:00:00").tz_localize('GMT')
    p1_ffin = pd.to_datetime("2019-12-31 00:00:00").tz_localize('GMT')
    p2_gran = "M1"
    p3_inst = "USD_MXN"
    p4_oatk = Tu token
    p5_ginc = 4900
    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """
        Parameters
        ----------
        p0_start : str : fecha inicial
        p1_end : str : fecha final
        p2_inc : int : incremento en cantidad de elementos
        p3_delta : str : intervalo para medir elementos ('minutes', 'hours', 'days')
        Returns
        -------
        ls_result : list : lista con fechas intermedias a frequencia solicitada
        Debugging
        ---------
        p0_start = p0_fini
        p1_end = p1_ffin
        p2_inc = p5_ginc
        p3_delta = 'minutes'
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4990:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            # print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

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
    vmin2 = val_2.min()
    vt2 = vmax2['profit_acm_d'] - valmin
    drawup_cap = list([vmin2['Timestamp'], vmax2['Timestamp'], vt2])
    
    
    #Calcular el information Ratio
    
    #Descarga de precios masivos en OANDA
    
    oa_token = 'b' + 'a3da768d923e90da18ca36c7b736b3a-af1ffe52629d9751a4899a115062e16' + 'c'
    oa_in = "SPX500_USD"  # Instrumento
    oa_gn = "D"  # Granularidad de velas
    fini = pd.to_datetime(param_data['dates'].min()).tz_localize('GMT')  # Fecha inicial
    ffin = pd.to_datetime(param_data['dates'].max()).tz_localize('GMT')  # Fecha final

    df_pe = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=oa_gn,
                              p3_inst=oa_in, p4_oatk=oa_token, p5_ginc=4900)
    
    #Rendimientos logaritmicos de SPX500
    rend_close = pd.DataFrame(float(i) for i in df_pe['Close'])
    rend_sp = np.log(rend_close / rend_close.shift(1)).iloc[1:]
    rlog_sp = rend_sp.mean()
    

    
    mad_data = {'Metrica': ['Sharpe', 'Sortino_c', 'Sortino_v', 'Drawdown_capi', 'Drawup_capi', 'Information_r'],
                'Valor': [sharpe_ratio, sortino_c, sortino_v, drawdown_capi, drawup_capi, info_ratio],
                'Descripción': ['Sharpe Ratio', 'Sortino Ratio para posiciones de compra',
                                'Sortino Ratio para posiciones de venta', 'DrawDown de Capital', 'DrawUp de Capital',
                                'Information Ratio']}
    df_mad = pd.DataFrame(mad_data)
    return df_mad
    
# -- -------------------------------- FUNCION: Una función para sesgos cognitivos---------------------------------------#

#def f_be_de(datos):
    
    # Principio 1: Punto de referencia
    #Proporcion del capital ganado y capital perdido vs capital
    #Utilizar el dataframe de operaciones historicas
    #Calcular el ratio (capital_ganado/capital_acm)*100 y (capital_perdido/capital_acm)*100 para cada operación
    #Nota, hacerlo con una iteración [i]
    
#    datos['ratio_capital_acm'] = 0
#    datos['ratio_capital_acm'] = [(datos['profit'][i] / 5000) * 100 if i == 0 else
#                                       (datos['profit'][i] /datos['capital_acm'][i - 1]) * 100
#                                       for i in range(len(datos))]
