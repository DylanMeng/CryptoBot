'''
Created on 18 juill. 2019

@author: jean-francois
'''
from datetime import datetime
def init():
    global NowPrice, num_ETH,num_USDT, gain, premier_prix, TirtyMinLast
    global TirtyMinNew, BidPrice, BidQty, AskPrice, AskQty, NbVentePossible, TimeNow, TimeTirty
    global SellAllNowGain, BuyPrice, SellPrice, ShadowPrice, LastBuys, LastSells
    global nb_sell, nb_buy, nb_Timeout, nb_ConnectionError, nb_VIP, start, Fichier, Fichier_excel, Buys_Qty
    global BuyOrderId, SellOrderId, ShadowOrderId, Pairs_contraints, Buy_multiplication_list, Sell_multiplication_list, price_contraints, quantity_contraints
    global Last_Agressivity, Agressivity, mean_2min_index_first, mean_2min_index_last, mean2min, mean30min, mean_tab_2min, mean_30min_index_first, mean_30min_index_last, mean30min, mean_tab_30min
    TimeNow = datetime.today()
    TimeTirty = datetime.today()

    num_USDT = 0

    BuyOrderId = {}
    BuyOrderId['ETHUSDT'] = 0

    SellOrderId = {}
    SellOrderId['ETHUSDT'] = 0
    #BuyOrderId['BTCUSDT'] = 0
    #SellOrderId['BTCUSDT'] = 0

    ShadowOrderId = 1

    # 'PAIRS': chiffre apres la virgule (Prix)
    price_contraints = { 'ETHUSDT': 2,
                        'ETHBTC': 6,
                        'BTCUSDT': 2,
                       }
    quantity_contraints = { 'ETHUSDT': 5,
                        'ETHBTC': 6,
                        'BTCUSDT': 2,
                       }

    Buys_Qty = {}
    Buys_Qty['ETHUSDT'] = [0.08, 0.0872, 0.09505, 0.1036 , 0.11293, 0.12309, 0.13417, 0.14624, 0.15941, 0.17375, 0.18939, 0.20643, 0.22501, 0.24526, 0.26734, 0.2914, 0.31762]
    #Buys_Qty['ETHBTC'] = []
    #Buys_Qty['BTCUSDT'] = []

    Buy_multiplication_list = {}
    Buy_multiplication_list['ETHUSDT'] = [2, 2.4, 2.8, 3.2, 3.6, 4, 4.4, 4.8, 5.2, 5.6, 6, 6.4, 6.8, 7.2, 7.6, 8, 8.4]
    #Buy_multiplication_list['ETHBTC'] = []
    # Buy_multiplication_list['BTCUSDT'] = []

    Sell_multiplication_list = {}
    Sell_multiplication_list['ETHUSDT'] = [2, 2.4, 2.8, 3.2, 3.6, 4, 4.4, 4.8, 5.2, 5.6, 6, 6.4, 6.8, 7.2, 7.6, 8, 8.4]
    #Sell_multiplication_list['ETHBTC'] = []
    # Sell_multiplication_list['BTCUSDT'] = []

    Agressivity = 1
    Last_Agressivity = 1

    ' le premier prix dachat de la simulation et variable de prix pour les 30 dernieres min'
    premier_prix = 0
    TirtyMinLast = 0
    TirtyMinNew =  0

    NowPrice = {}
    NowPrice['ETHUSDT'] = 0
    #NowPrice['BTCUSDT'] = 0
    #NowPrice['ETHBTC'] = 0


    BidPrice = {}
    BidPrice['ETHUSDT'] = 0
    #BidPrice['BTCUSDT'] = 0
    #BidPrice['ETHBTC'] = 0

    AskPrice = {}
    AskPrice['ETHUSDT'] = 0
    #AskPrice['BTCUSDT'] = 0
    #AskPrice['ETHBTC'] = 0

    #BuyPrice['ETHUSDT'] = 0
    #BuyPrice['BTCUSDT'] = 0
    #BuyPrice['ETHBTC'] = 0
    #SellPrice['ETHUSDT'] = 0
    #SellPrice['BTCUSDT'] = 0
    #SellPrice['ETHBTC'] = 0

    BuyPrice = {}
    BuyPrice['ETHUSDT'] = 0

    SellPrice = {}
    SellPrice['ETHUSDT'] = 0

    ShadowPrice = 0

    gain = {}
    gain['ETHUSDT'] = 0

    NbVentePossible = {}
    NbVentePossible['ETHUSDT'] = 0

    mean_tab_2min = {}
    mean_tab_2min['ETHUSDT'] = [0 for i in range(30)]
    #mean_tab_2min['BTCUSDT'] = [0 for i in range(30)]
    mean_2min_index_first = 0
    mean_2min_index_last = 29
    mean2min = {}
    mean2min['ETHUSDT'] = 0

    mean_tab_30min = {}
    mean_tab_30min['ETHUSDT'] = [0 for i in range(450)]
    #mean_tab_2min['BTCUSDT'] = [0 for i in range(450)]
    mean_30min_index_first = 0
    mean_30min_index_last = 29
    mean30min = {}
    mean30min['ETHUSDT'] = 0

    SellAllNowGain = {}
    SellAllNowGain['ETHUSDT'] = 0

    #Dictionnaire des derniers achats
    LastBuys = {}
    LastBuys['ETHUSDT'] = {}
    LastBuys['ETHUSDT']['List'] = []
    LastBuys['ETHUSDT']['Nb'] = 0
    LastBuys['ETHUSDT']['Price_Average'] = 0
    LastBuys['ETHUSDT']['Sum'] = 0
    LastBuys['ETHUSDT']['Qty'] = 0
    LastBuys['ETHUSDT']['Time'] = 0

    # LastBuys['BTCUSDT'] = {}
    # LastBuys['BTCUSDT']['List'] = []
    # LastBuys['BTCUSDT']['Nb'] = 0
    # LastBuys['BTCUSDT']['Price_Average'] = 0
    # LastBuys['BTCUSDT']['Sum'] = 0
    # LastBuys['BTCUSDT']['Qty'] = 0
    # LastBuys['BTCUSDT']['Time'] = 0

    #Dictionnaire des dernieres ventes
    LastSells = {}
    LastSells['ETHUSDT'] = {}
    LastSells['ETHUSDT']['List'] = []
    LastSells['ETHUSDT']['Nb'] = 0
    LastSells['ETHUSDT']['Time'] = 0

    #LastSells['BTCUSDT'] = {}
    #LastSells['BTCUSDT']['List'] = []
    #LastSells['BTCUSDT']['Nb'] = 0
    #LastSells['BTCUSDT']['Time'] = 0

    'nombre d achat et de vente'
    nb_sell = 0
    nb_buy = 0
    nb_Timeout = 0
    nb_ConnectionError = 0
    nb_VIP = 0 
    start = False
    Fichier = 'caca.txt'
    Fichier_excel = 'LOG_6.xlsx'