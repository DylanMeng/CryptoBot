'''
Created on 18 juill. 2019

@author: jean-francois
'''
from datetime import datetime
def init():
    global NowPrice, num_ETH,num_USDT, gain, premier_prix, TirtyMinLast
    global TirtyMinNew, BidPrice, BidQty, AskPrice, AskQty, NbVentePossible, TimeNow, TimeTirty
    global SellAllNowGain, BuyPrice, SellPrice, ShadowPrice, LastBuys, LastSells
    global nb_sell, nb_buy, nb_Timeout, nb_ConnectionError, nb_VIP, stop, Fichier, Fichier_excel, Buys_Qty
    global BuyOrderId, SellOrderId, ShadowOrderId, Pairs_contraints, Buy_multiplication_list, Sell_multiplication_list
    global Last_Agressivity, Agressivity
    TimeNow = datetime.today()
    TimeTirty = datetime.today()
    NowPrice = 0
    num_ETH = 0
    num_USDT = 0
    gain = 0

    #BuyOrderId['ETHUSDT'] = 0
    #SellOrderId['ETHUSDT'] = 0
    #BuyOrderId['BTCUSDT'] = 0
    #SellOrderId['BTCUSDT'] = 0
    #BuyOrderId['ETHBTC'] = 0
    #SellOrderId['ETHBTC'] = 0

    SellOrderId = 0
    SellOrderId = 0
    ShadowOrderId = 1

    # 'PAIRS': chiffre apres la virgule (Prix)
    Pairs_contraints = { 'ETHUSDT': 2,
                        'ETHBTC': 6,
                        'BTCUSDT': 2,
                       }

    #Buys_Qty = {}
    #Buys_Qty['ETHUSDT'] = [0.07,0.07,0.07,0.14,0.21,0.21,0.28,0.28,0.35,0.35]
    #Buys_Qty['ETHBTC'] = []
    #Buys_Qty['BTCUSDT'] = []

    #Buys_Qty = [0.1,0.1,0.12,0.12,0.14,0.14,0.16,0.16,0.18,0.18]
    Buys_Qty = [0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.21, 0.22, 0.23, 0.24]

    #Buy_multiplication_list = [1,1.25,2.7,3.3,3.8,4,4.2,5,5.2, 5.2,5.2, 5.2]
    #Sell_multiplication_list = [1, 1.2, 1.5, 2.2, 2.8, 3.2, 3.7, 4, 4, 4, 4]

    Buy_multiplication_list = [3, 3.4, 3.8, 4.2, 4.6, 5, 5.4, 5.8, 6.2, 6.6, 7, 7.4, 7.8, 8.2, 8.6, 9, 9.4]
    Sell_multiplication_list = [3, 3.4, 3.8, 4.2, 4.6, 5, 5.4, 5.8, 6.2, 6.6, 7, 7.4, 7.8, 8.2, 8.6, 9, 9.4]
    Agressivity = 1
    Last_Agressivity = 1

    ' le premier prix dachat de la simulation et variable de prix pour les 30 dernieres min'
    premier_prix = 0
    TirtyMinLast = 0
    TirtyMinNew =  0

    #BidPrice['ETHUSDT'] = 0
    #BidPrice['BTCUSDT'] = 0
    #BidPrice['ETHBTC'] = 0
    #AskPrice['ETHUSDT'] = 0
    #AskPrice['BTCUSDT'] = 0
    #AskPrice['ETHBTC'] = 0

    BidPrice = 0
    AskPrice = 0

    #BuyPrice['ETHUSDT'] = 0
    #BuyPrice['BTCUSDT'] = 0
    #BuyPrice['ETHBTC'] = 0
    #SellPrice['ETHUSDT'] = 0
    #SellPrice['BTCUSDT'] = 0
    #SellPrice['ETHBTC'] = 0

    BuyPrice = 0
    SellPrice = 0
    ShadowPrice = 0

    NbVentePossible = 0
    SellAllNowGain = 0

    'liste des prix des derniers achats et ventes'
    LastBuys = {}
    #LastBuys['ETHUSDT'] = {}
    #LastBuys['ETHUSDT']['Price_Average'] = 0
    # LastBuys['ETHUSDT']['List'] = []
    # LastBuys['ETHUSDT'] = {}
    # LastBuys['ETHUSDT']['Price_Average'] = 0
    # LastBuys['ETHUSDT']['List'] = []
    LastBuys['ETHUSDT']  = []


    LastSells = {}
    LastSells['ETHUSDT'] = []
    'nombre d achat et de vente'
    nb_sell = 0
    nb_buy = 0
    nb_Timeout = 0
    nb_ConnectionError = 0
    nb_VIP = 0 
    stop = False
    Fichier = 'caca.txt'
    Fichier_excel = 'LOG_6.xlsx'