'''
Created on 27 mai 2019

@author: jean-francois
'''
from distutils.dist import command_re
from tkinter.constants import ACTIVE, FLAT, GROOVE, DISABLED, LEFT, RIGHT, \
    BOTTOM

# from builtins import False
'''
Created on 24 mai 2019

@author: jean-francois
'''

'Librairies utilise et Flag utilise'
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError
from binance.client import Client
from binance.enums import *
from datetime import datetime, timedelta
import time
import Keys
import Data
import tkinter as tk
import xlsxwriter

Data.init()
# Ouverture de la session avec l API
client = Client(api_key=Keys.api_key, api_secret=Keys.api_secret)
# en tete du fichier log qui sert de documentation sur les trades (fichier TXT pour garder en mémoire la condition lors du crash)
fichier = open(Data.Fichier, "w")
excel = xlsxwriter.Workbook(Data.Fichier_excel)
worksheet1 = excel.add_worksheet('Trades')
worksheet1.write(0, 0, 'TYPE')
worksheet1.write(0, 1, 'PRIX')
worksheet1.write(0, 2, 'GAIN')
worksheet1.write(0, 3, 'TEMPS')
worksheet1.write(0, 4, 'NOMBRE ETH')

'-------------------------------------------------------------------------------------------------------------------------------------------'
# FONCTION
'-------------------------------------------------------------------------------------------------------------------------------------------'

def log_condition():
    # Ouvrir le fichier en write mode clear son contenu
    fichier = open(Data.Fichier, "w")

    fichier.write('TimeNow: {}\n'.format(Data.TimeNow))
    fichier.write('NowPrice: {}\n'.format(Data.NowPrice['ETHUSDT']))
    fichier.write('num_ETH: {}\n'.format(Data.LastBuys['ETHUSDT']['Qty']))
    fichier.write('num_USDT: {}\n'.format(Data.num_USDT))
    fichier.write('gain: {}\n'.format(Data.gain['ETHUSDT']))
    fichier.write('BidPrice: {}\n'.format(Data.BidPrice['ETHUSDT']))
    fichier.write('AskPrice: {}\n'.format(Data.AskPrice['ETHUSDT']))
    fichier.write('NbVentePossible: {}\n'.format(Data.NbVentePossible['ETHUSDT']))
    fichier.write('SellAllNowGain: {}\n'.format(Data.SellAllNowGain['ETHUSDT']))
    fichier.write('BuyPrice: {}\n'.format(Data.BuyPrice['ETHUSDT']))
    fichier.write('SellPrice: {}\n'.format(Data.SellPrice['ETHUSDT']))
    fichier.write('LastBuys: {}\n'.format(Data.LastBuys['ETHUSDT']['List']))
    fichier.write('LastSells: {}\n'.format(Data.LastSells['ETHUSDT']['List']))
    fichier.write('nb_sell: {}\n'.format(Data.LastSells['ETHUSDT']['Nb']))
    fichier.write('nb_buy: {}\n'.format(Data.LastBuys['ETHUSDT']['Nb']))
    # fichier.write('nb_Timeout: {}'.format(Data.nb_Timeout))
    # fichier.write('nb_ConnectionError: {}'.format(Data.nb_ConnectionError))
    # fichier.write('nb_VIP: {}'.format(Data.nb_VIP))

    fichier.close()


def ecrire_vente_excel():
    row = Data.LastBuys['ETHUSDT']['Nb'] + Data.LastSells['ETHUSDT']['Nb']
    worksheet1.write(row, 0, 'VENTE')
    worksheet1.write(row, 1, Data.NowPrice['ETHUSDT'])
    worksheet1.write(row, 2, Data.gain['ETHUSDT'])
    worksheet1.write(row, 3, str(Data.TimeNow))
    worksheet1.write(row, 4, Data.LastBuys['ETHUSDT']['Qty'])
    worksheet1.write(row, 5, 'LastBuys: ')
    for i in range(len(Data.LastBuys['ETHUSDT']['List'])):
        worksheet1.write(row, i + 6, Data.LastBuys['ETHUSDT']['List'][i]['Price'])
    worksheet1.write(row, 7 + len(Data.LastBuys['ETHUSDT']['List']), 'LastSells')
    for i in range(len(Data.LastSells['ETHUSDT']['List'])):
        worksheet1.write(row, i + 8 + len(Data.LastBuys['ETHUSDT']['List']), Data.LastSells['ETHUSDT']['List'][i]['Price'])
    print('   SELL!')

def ecrire_achat_excel():
    row = Data.LastBuys['ETHUSDT']['Nb'] + Data.LastSells['ETHUSDT']['Nb']
    worksheet1.write(row, 0, 'ACHAT')
    worksheet1.write(row, 1, Data.NowPrice['ETHUSDT'])
    worksheet1.write(row, 2, Data.gain['ETHUSDT'])
    worksheet1.write(row, 3, str(Data.TimeNow))
    worksheet1.write(row, 4, Data.LastBuys['ETHUSDT']['Qty'])
    worksheet1.write(row, 5, 'LastBuys')
    for i in range(len(Data.LastBuys['ETHUSDT']['List'])):
        worksheet1.write(row, i + 6, Data.LastBuys['ETHUSDT']['List'][i]['Price'])
    worksheet1.write(row, 7 + len(Data.LastBuys['ETHUSDT']['List']), 'LastSells')
    for i in range(len(Data.LastSells['ETHUSDT']['List'])):
        worksheet1.write(row, i + 8 + len(Data.LastBuys['ETHUSDT']['List']), Data.LastSells['ETHUSDT']['List'][i]['Price'])
    print('   BUY!')


def get_NbCryp():
    info = client.get_account()
    for assets in info['balances']:
        # if(assets['asset'] == 'ETH'):

        if (assets['asset'] == 'USDT'):
            Data.num_USDT = float(assets['free'])


def cancel_order(side, pair):
    if side == "Sell":
        try:
            client.cancel_order(symbol=pair, orderId=Data.SellOrderId[pair]['orderId'])
            print('Sell Order canceled')
        except Exception as e:
            print("Buy Order Cancel has not worked: Pair: {}, OrderId: {}, Exception: {} ".format(pair, Data.BuyOrderId[pair]['orderId'], e))
            exit()
    elif side == "Buy":
        try:
            client.cancel_order(symbol=pair, orderId=Data.BuyOrderId[pair]['orderId'])
            print('Buy Order canceled')
        except Exception as e:
            print("Buy Order Cancel has not worked: Pair: {}, OrderId: {}, Exception: {} ".format(pair, Data.BuyOrderId[pair]['orderId'], e))
            exit()

def add_LastBuydic(Order):
    # function that add the new Buy to a dic (Should only be used in order_filled function)
    pair = Order['symbol']
    Data.LastBuys[pair]['Time'] = datetime.now()
    #si il existe deja un dictionnaire à ce prix
    if Order['price'] == Data.LastBuys[pair]['List'][0]['Price']:
        Data.LastBuys[pair]['List'][0]['Qty'] += float(Order['executedQty'])
        #sinon on ajoute un autre dictionnaire
    else:
        newBuydic = {'Price': Order['price'],
                     'Qty':   float(Order['executedQty'])}
        Data.LastBuys[pair]['List'].insert(0,newBuydic)
    #trie du plus cher aux moinx cher
    #Data.LastBuys[Order['symbol']]['List'] = sorted(Data.LastBuys[Order['symbol']]['List'], key= lambda i: i['Price'])

def add_LastSelldic(Order):
    pair = Order['symbol']
    Data.LastSells[pair]['Time'] = datetime.now()
    # function that add the new Buy to a dic (Should only be used in order_filled function)
    newSelldic = {'Price': Order['price'],
                 'Qty':   float(Order['executedQty'])}
    Data.LastSells[Order['symbol']]['List'].insert(0,newSelldic)
    #trie du plus cher aux moinx cher
    #Data.LastSells[Order['symbol']]['List'] = sorted(Data.LastSells[Order['symbol']]['List'], key= lambda i: i['Price'],reverse=True)

def price_mean_2min():
    mean = 0

    for pair in Data.LastBuys.keys():

        Data.mean_tab_2min[pair][Data.mean_index_last] = Data.NowPrice[pair]

        Data.mean2min[pair] -= 0.034483*Data.mean_tab_2min[pair][Data.mean_index_first]
        Data.mean2min[pair] += 0.034483*Data.mean_tab_2min[pair][Data.mean_index_last]

        Data.mean_index_first = (Data.mean_index_first + 1) % 30
        Data.mean_index_last = (Data.mean_index_last + 1) % 30

def order_filled(side, pair):
    if side == "Buy":
        try:
            Order = client.get_order(symbol=pair,
                                     orderId=Data.BuyOrderId[pair]['orderId'])
            if (Order['status'] == 'FILLED'):
                print("Buy order is filled")
                # on ajoute l achat courrant a la liste
                add_LastBuydic(Order)
                # Si possible, on enleve la vente qui a ete utilise pour lachat
                if (len(Data.LastSells[pair]['List']) > 0):
                    Data.LastSells[pair]['List'].pop(0)
                # gain, on compte egalement les fees (0.06% du trade)
                Data.gain[pair] -= float(Order['executedQty']) * float(Order['price']) * 1.0006
                return True
        except Exception as e:
            print("Buy Order info could not be fetch:pair: {} OrderId: {}, Exception: {} ".format(pair, Data.BuyOrderId[pair]['orderId'], e))
            return False

    elif side == "Sell":
        try:
            Order = client.get_order(symbol=pair,
                                     orderId=Data.SellOrderId[pair]['orderId'])
            if (Order['status'] == 'FILLED'):
                print("Sell order is filled")
                # on ajoute l achat courrant a la liste
                add_LastSelldic(Order)
                executed_qty = float(Order['executedQty'])

                # Cas 1: quantité vendu plus petite que le dernier achat
                if  executed_qty < Data.LastBuys[pair]['List'][0]['Qty'] * 0.9995:
                    Data.LastBuys[pair]['List'][0]['Qty'] -= executed_qty

                # Cas 2: quantité vendu plus grande que le dernier achat
                elif executed_qty > Data.LastBuys[pair]['List'][0]['Qty']*1.0005:
                    # tant que la quantité vendue est plus grande que les achats
                    while((executed_qty - Data.LastBuys[pair]['List'][0]['Qty']) > 0.00005 and len(Data.LastBuys[pair]['List']) > 1):
                        executed_qty -= Data.LastBuys[pair]['List'][0]['Qty']
                        Data.LastBuys[pair]['List'].pop(0)
                    # si il reste encore un achat
                    if len(Data.LastBuys[pair]['List']) > 1:
                        #If almost the same
                        if abs(Data.LastBuys[pair]['List'][0]['Qty'] - executed_qty) < 0.00005:
                            Data.LastBuys[pair]['List'].pop(0)
                        else:
                            Data.LastBuys[pair]['List'][0]['Qty'] -= executed_qty

                # Cas 3: quantité vendu environ égal au dernier achat
                else :
                    if len(Data.LastBuys[pair]['List']) > 1:
                        Data.LastBuys[pair]['List'].pop(0)

                # gain, on compte egalement les fees (0.06% du trade)
                Data.gain[pair] += float(Order['executedQty']) * float(Order['price']) * 0.9994
                return True
        except Exception as e:
            print("Sell Order info could not be fetch:pair: {} OrderId: {}, Exception: {} ".format(pair, Data.BuyOrderId[pair]['orderId'], e))
            return False

    elif side == "Shadow":
        if Data.ShadowOrderId['orderId'] == 0:
            return False
        try:
            Order = client.get_order(symbol=pair,
                                     orderId=Data.ShadowOrderId['orderId'])
            if (Order['status'] == 'FILLED'):
                print("Shadow order is filled")
                newBuySelldic = {'Price': str(Order['price']),
                                 'Qty': 0}
                Data.LastBuys[pair]['List'].clear()
                Data.LastSells[pair]['List'].clear()
                Data.LastBuys[pair]['List'].insert(0, newBuySelldic)

                # gain, on compte egalement les fees (0.06% du trade)
                Data.gain[pair] += float(Order['executedQty']) * float(Order['price']) * 0.9994
                Data.ShadowOrderId['orderId'] = 0
                return True

        except Exception as e:
            print("Shadow Order info could not be fetch:pair: {} OrderId: {}, Exception: {} ".format(pair, Data.BuyOrderId[pair]['orderId'], e))
            return False


def set_agressivity():
    Data.Buy_multiplication_list['ETHUSDT'] = [i * Data.Agressivity for i in Data.Buy_multiplication_list['ETHUSDT']]
    Data.Last_Agressivity = Data.Agressivity

#Algo principale de vente et achat
def calculate_trigger_prices(pair):

    vente_possible = Data.LastBuys[pair]['Nb'] - Data.LastSells[pair]['Nb']   #nb d'achat qui est passible d'une vente

    lenLastBuys = len(Data.LastBuys[pair]['List'])
    lenLastSells = len(Data.LastSells[pair]['List'])                       #nb de vente consécutive
    #Best price to compare to (offset to point on the good last buy)
    offset = lenLastBuys - 1 - vente_possible
    Last_Buy = float(Data.LastBuys[pair]['List'][offset]['Price'])  # le Last_Buy est celui qui n'est pas des miettes
    if lenLastSells > 0:
        Last_Sell = float(Data.LastSells[pair]['List'][0]['Price'])
    #to display on the GUI
    Data.NbVentePossible[pair] = vente_possible

    #Si aucun achat de realise (condition initiale + pas de vente permise)
    if ((vente_possible == 0) and (lenLastSells == 0)):
        Data.BuyPrice[pair] = Last_Buy - (Data.Buy_multiplication_list[pair][vente_possible] ** 1.3) * 0.0025 * Last_Buy
        Data.SellPrice[pair] = 999999
    #Si aucun achat restant et ventes réalisés dans le passé (on se base sur la derniere vente + Pas de vente permise)
    elif ((vente_possible == 0) and (lenLastSells > 0)):
        Data.LastSells[pair]['List'].clear()
        Data.BuyPrice[pair] = Last_Sell - (Data.Buy_multiplication_list[pair][vente_possible] ** 1.3) * 0.0025 * Last_Sell #cas speciale,
        Data.SellPrice[pair] = 999999
    #Si achats dans lasBuys (on se base sur les derniers achats)
    else:
        Data.BuyPrice[pair] = Last_Buy - (Data.Buy_multiplication_list[pair][vente_possible] ** 1.3) * 0.0025 * Last_Buy
        Data.SellPrice[pair] = Last_Buy + (Data.Sell_multiplication_list[pair][lenLastSells] ** 1.2) * 0.00255 * Last_Buy


def LastBuys_price_average():
    for pair in Data.LastBuys.keys():
        Sum = 0
        Qty = 0
        for Buydict in Data.LastBuys[pair]['List']:
            Sum += float(Buydict['Price'])*Buydict['Qty']
            Qty += float(Buydict['Qty'])
        if Qty == 0:
            Data.LastBuys[pair]['Price_Average'] = 0
            Data.LastBuys[pair]['Sum'] = 0
            Data.LastBuys[pair]['Qty'] = 0
        else:
            Data.LastBuys[pair]['Price_Average'] = Sum/Qty
            Data.LastBuys[pair]['Sum'] = Sum
            Data.LastBuys[pair]['Qty'] = Qty

def get_Prix():
    #get the bid Ask and Now price of each pair trading
    for pair in Data.LastBuys.keys():
        price = client.get_symbol_ticker(symbol=pair)
        Book = client.get_order_book(symbol=pair)
        Data.BidPrice[pair] = float(Book['bids'][0][0])
        Data.AskPrice[pair] = float(Book['asks'][0][0])
        Data.NowPrice[pair] = float(price['price'])

def Verif_Achat(pair):
    # Verifie l'achat et ajoute celle-ci aux lasbuys
    if (order_filled("Buy", pair) == True):
        # Un achat de plus
        Data.LastBuys[pair]['Nb'] += 1
        LastBuys_price_average()
        #RefreshLastBuysSells()
        #Nouveau prix de vente et d achat
        calculate_trigger_prices(pair)
        # Combien de vente possible
        nb_vente_possible = Data.LastBuys[pair]['Nb'] - Data.LastSells[pair]['Nb']
        #Refer to list in Data.py to for buy Qty
        nb_achat = Data.Buys_Qty[pair][nb_vente_possible]
        # Nouvelle achat
        Acheter(prix=Data.BuyPrice[pair], nb_achat=nb_achat, pair= pair)
        # si plus d'une vente possible
        if (nb_vente_possible > 1):
            # il y avait une vente
            cancel_order("Sell", pair)
        # nouvelle vente (Quantité acheté
        ####################################################################################
        #ALGO AGRESSIF
        nb_vente = Data.LastBuys[pair]['Qty']/(nb_vente_possible)
        ####################################################################################
        #nb_vente = Data.LastBuys[pair]['List'][0]['Qty']
        Vendre(prix=Data.SellPrice[pair], nb_vente=nb_vente, pair=pair)

def Verif_Vente(pair):
    if (len(Data.LastBuys[pair]['List']) > 1):
        # Verifie la vente et ajoute celle-ci aux lasBuys
        if (order_filled("Sell", pair) == True):
            # Une vente de plus
            Data.LastSells[pair]['Nb'] += 1
            LastBuys_price_average()
            #RefreshLastBuysSells()
            #Calculer prochain les prix d'achat et de vente
            calculate_trigger_prices(pair)
            # On cancele lordre dachat pour la mettre a jour avec la derniere vente
            cancel_order("Buy", pair)
            # combien de vente possible maintenant ?
            nb_vente_possible = Data.LastBuys[pair]['Nb'] - Data.LastSells[pair]['Nb']
            # Refer to list in Data.py to for buy Qty
            nb_achat = Data.Buys_Qty[pair][nb_vente_possible]
            Acheter(prix=Data.BuyPrice[pair], nb_achat=nb_achat, pair=pair)

            if (nb_vente_possible > 0):
                # nouvelle vente or (Data.LastBuys[0]['Qty']
                ####################################################################################
                # ALGO AGRESSIF
                nb_vente = Data.LastBuys[pair]['Qty']/(nb_vente_possible)
                ####################################################################################
                #nb_vente = Data.LastBuys[pair]['List'][0]['Qty']
                Vendre(prix=Data.SellPrice[pair], nb_vente=nb_vente, pair=pair)

'Fonction qui achette a un prix et une quantité donnée'


def shadow_Sell(pair):
    # If there is nothing else to sell focus on the shadow sell
    if (len(Data.LastBuys[pair]['List']) == 1):
        if (order_filled('Shadow')):
            Data.LastSells[pair]['Nb'] += 1
            #RefreshLastBuysSells()
            calculate_trigger_prices()
            # On cancele lordre dachat pour la mettre a jour avec la derniere vente
            cancel_order("Buy", pair)
            # Refer to list in Data.py to for buy Qty
            nb_achat = Data.Buys_Qty[pair][0]
            Acheter(prix=Data.BuyPrice[pair], nb_achat=nb_achat, pair=pair)


def Acheter(prix, nb_achat, pair):
    try:
        Data.BuyOrderId[pair] = client.order_limit_buy(symbol=pair,
                                                 quantity=round(nb_achat, Data.quantity_contraints[pair]),  #Chiffre apres la virgule pour la quantité
                                                 price=str(round(prix, Data.price_contraints[pair])))       #Chiffre apres la virgule du prix
        print('Buy Order Sent => QTY: {} ETH, PRICE: {} USDT/ETH'.format(nb_achat, prix))
    except Exception as e:
        print('Buy Order could not be send! Exception: {}'.format(e))
        exit()


'Fonction qui vend a un prix et une quantité donnée'


def Vendre(prix, nb_vente, pair):
    try:
        Data.SellOrderId[pair] = client.order_limit_sell(symbol=pair,
                                                   quantity=round(nb_vente, Data.quantity_contraints[pair]), #Chiffre apres la virgule pour la quantité
                                                   price=str(round(prix, Data.price_contraints[pair])))      #Chiffre apres la virgule du prix
        print('Sell Order Sent => QTY: {} ETH, PRICE: {} USDT/ETH'.format(nb_vente, prix))
    except Exception as e:
        print('Sell Order could not be send! Exception: {}'.format(e))
        exit()


def SellAll(prix):
    while (Data.NbVentePossible['ETHUSDT'] > 0):
        Vendre(prix=prix, nb_vente=Data.LastBuys['ETHUSDT']['Qty'])


def SellOne():
    Vendre(prix=Buy)


def BuyOne():
    Acheter(1)


'Fonction TirtyMin qui historise le prix au 30 min et qui achete si le prix a changer brusquemment***Cas de blockage achat'


def TirtyMin():
    if (Data.TimeNow - Data.TimeTirty > timedelta(minutes=15)):
        Data.TimeTirty = Data.TimeNow
        Data.TirtyMinLast = Data.TirtyMinNew
        Data.TirtyMinNew = Data.NowPrice['ETHUSDT']
        print('Tirty Min')
        if (len(Data.LastBuys['ETHUSDT']['List']) == 1 and Data.TirtyMinNew < 0.99 * Data.TirtyMinLast):
            Data.nb_VIP += 1
            Acheter(1)


get_NbCryp()
get_Prix()

'-------------------------------------------------------------------------------------------------------------------------------------------'
'-----------------------------APPLICATION'
'-------------------------------------------------------------------------------------------------------------------------------------------'

def add_Agressivity():
    Data.Agressivity +=1

def minus_Agressivity():
    if Data.Agressivity > 1:
        Data.Agressivity -=1

def onReturn(event):
    # Fonction qui initialise le GUI apres avoir envoyer un prix dans le text box (ENTER)
    Data.premier_prix = float(e1.get())
    newBuySelldic = {'Price': str(round(Data.premier_prix,2)),
                     'Qty': 0}
    Data.TirtyMinNew = Data.premier_prix
    Data.LastBuys['ETHUSDT']['List'].clear()
    Data.LastSells['ETHUSDT']['List'].clear()
    Data.LastBuys['ETHUSDT']['List'].insert(0, newBuySelldic)

    b = tk.Label(root, text='Price: ', bg='gold')
    b.grid(row=5, column=3)
    b = tk.Label(root, text='Qty:', bg='gold')
    b.grid(row=6, column=3)
    b = tk.Label(root, text='Price: ', bg='gold')
    b.grid(row=7, column=3)
    b = tk.Label(root, text='Qty:', bg='gold')
    b.grid(row=8, column=3)
    i = 0
    #Refresh the LastBuys and LastSells dict
    RefreshLastBuysSells()
    Data.BuyPrice['ETHUSDT'] = float(Data.LastBuys['ETHUSDT']['List'][0]['Price']) - (Data.Buy_multiplication_list['ETHUSDT'][0] ** 1.3) * 0.0025 * float(Data.LastBuys['ETHUSDT']['List'][0]['Price'])
    Data.SellPrice['ETHUSDT'] = 99999
    labelSellPrice.config(text='Prix de vente: ' + str(Data.SellPrice['ETHUSDT']))
    labelBuyPrice.config(text='Prix de d achat: ' + str(Data.BuyPrice['ETHUSDT']))
    labelLastBuys.config(text='Derniers achats: ')
    labelLastSells.config(text='Dernieres ventes: ')
    #Premiere ordre d'achat
    Acheter(prix=Data.BuyPrice['ETHUSDT'], nb_achat=Data.Buys_Qty['ETHUSDT'][0], pair='ETHUSDT')
    #Shadow 4% higher than start price
    Data.ShadowPrice = 1.025*Data.BuyPrice['ETHUSDT']
    #Data.ShadowOrderId = client.order_limit_sell(symbol='ETHUSDT',
    #                                             quantity=round(0.1, 5),
    #                                             price=str(round(Data.ShadowPrice, 2)))
    e1.delete(0, 'end')

def RefreshLastBuysSells():
    global label_2x7Buys, label_2x7Sells
    #Working on a clean way to display the list of dict
    if(len(Data.LastBuys['ETHUSDT']['List']) > 0):
        i = 0
        for Buy in Data.LastBuys['ETHUSDT']['List']:
            j = 0
            for Keys in Buy.keys():
                text = str(Buy[Keys])
                print('{} {}'.format(j,i))

                label_2x7Buys[j][i].config(text=text)
                label_2x7Buys[j][i].grid(row=j + 5, column=i + 4)
                j += 1
            i += 1
        #Clean the rest of the 7x7 table
        for i in range(i,7):
            for j in range(0,1):
                text = ''
                label_2x7Buys[j][i].config(text=text)
                label_2x7Buys[j][i].grid(row=j + 5, column=i + 4)
                j += 1
    if (len(Data.LastSells['ETHUSDT']['List']) > 0):
        i = 0
        for Sell in Data.LastSells['ETHUSDT']['List']:
            j = 0
            for Keys in Buy.keys():
                text = str(Sell[Keys])
                label_2x7Sells[j][i].config(text=text)
                label_2x7Sells[j][i].grid(row=j + 7, column=i + 4)
                j += 1
            i += 1
        #Clean the rest of the 7 column table
        for i in range(i,7):
            for j in range(0,1):
                text = ''
                label_2x7Sells[j][i].config(text=text)
                label_2x7Sells[j][i].grid(row=j + 7, column=i + 4)
                j += 1


'Fonction de rafraichissement de l interface graphique'
def RefreshApp():
    labelNowPrice.config(text='Prix (ETHUSDT): ' + str(Data.NowPrice['ETHUSDT']) + '  (USDT/ETH)')
    labelBidPrice.config(text='Bid Price (ETHUSDT): ' + str(Data.BidPrice['ETHUSDT']))
    labelAskPrice.config(text='Ask Price (ETHUSDT): ' + str(Data.AskPrice['ETHUSDT']))
    labelNowGain.config(text='Gain: ' + str(Data.gain['ETHUSDT']) + '  (USDT)')
    labelNbBuys.config(text='Nb dachat: ' + str(Data.LastBuys['ETHUSDT']['Nb']))
    labelNbSells.config(text='Nb de vente: ' + str(Data.LastSells['ETHUSDT']['Nb']))
    labelNbETH.config(text='Nb de ETH: ' + str(Data.LastBuys['ETHUSDT']['Qty']))
    labelNbUSDT.config(text='Qty USDT = ' + str(Data.num_USDT))
    labelSellPrice.config(text='Prix de vente: ' + str(Data.SellPrice['ETHUSDT']))
    labelBuyPrice.config(text='Prix de d achat: ' + str(Data.BuyPrice['ETHUSDT']))
    labelNbSellPossible.config(text='Nb de vente possible: ' + str(Data.NbVentePossible['ETHUSDT']))
    labelSellAllNowGain.config(text='Gain si vente total: ' + str(Data.SellAllNowGain['ETHUSDT']))


'-------------------------------------------------------------------------------------------------------------------------------------------'
'PRINCIPALE BOUCLE UTILISE POUR ROULER LE PROGRAMME'
'utilisation de after() pour boucler a tous les secondes lorsquon appuie sur RUN et '
'et arreter lors que l on appuie sur STOP'
'-------------------------------------------------------------------------------------------------------------------------------------------'

def Main():
    labelRunning.config(text='Le programme Run mon homme !')
    breakout = root.after(4500, Main)
    if (Data.start == True):

        try:
            get_Prix()
            price_mean_2min()
            get_NbCryp()
        except Timeout:
            # write event to logfile
            fichier.write('FAILLLLLLLLLLLLLLLLLLLLLLLLLLL   \n')
            Data.nb_Timeout += 1
            pass

        except ConnectionError:
            # write event to logfile
            fichier.write('FAILLLLLLLLLLLLLLLLLLLLLLLLLLL   \n')
            Data.nb_ConnectionError += 1
            pass
        for pair in Data.LastBuys.keys():
            # Regarder si la vente ou lachat a été filled
            Verif_Achat(pair)
            Verif_Vente(pair)
            #shadow_Sell()
            print(str(Data.LastBuys))
            print(str(Data.LastSells))
            print(str(Data.mean2min))
            #print("ShadowSellPrice: {}".format(Data.ShadowPrice))
            #print(Data.Buy_multiplication_list['ETHUSDT'])
            #print(Data.Sell_multiplication_list['ETHUSDT'])
            # Fonction de vérification d'achat au 30 min
            # TirtyMin()
            Data.SellAllNowGain[pair] = Data.gain[pair] + Data.LastBuys[pair]['Qty'] * Data.BidPrice[pair]
            RefreshApp()
            log_condition()
    else:
        labelRunning.config(text='Not running')
        root.after_cancel(breakout)


def Stop():
    fichier = open(Data.Fichier, 'a')
    Data.SellAllNowGain['ETHUSDT'] = Data.gain['ETHUSDT'] + Data.LastBuys['ETHUSDT']['Qty'] * Data.BidPrice['ETHUSDT']

    'Conclusion du fichier de log'
    print('STOP')
    fichier.write('Dernier PRIX:   ' + str(Data.NowPrice['ETHUSDT']) + '\n')
    fichier.write('Nb de vente:  ' + str(Data.LastSells['ETHUSDT']['Nb']) + '\n')
    fichier.write('Nb de dachat:  ' + str(Data.LastBuys['ETHUSDT']['Nb']) + '\n')
    fichier.write('Nb de ConnectionError:  ' + str(Data.nb_ConnectionError) + '\n')
    fichier.write('Nb de Timeout:  ' + str(Data.nb_Timeout) + '\n')
    fichier.write('LastBuys:  ' + str(Data.LastBuys['ETHUSDT']['List']) + '\n')
    fichier.write('LastSells:  ' + str(Data.LastSells['ETHUSDT']['List']) + '\n')
    fichier.write('SellAllNowGain:  ' + str(Data.SellAllNowGain['ETHUSDT']) + '\n')
    fichier.write('NbVIP:  ' + str(Data.nb_VIP) + '\n')

    Data.start = False
    excel.close()

def Start():
    # If no thread, Start a thread
    if Data.start == 0:
        Data.start = True
        Main()

root = tk.Tk()
root.title('Crypto_Trading app')
root.geometry('1080x720')
root.minsize(480, 480)
# root.iconbitmap('logo.ico')
root.config(background='goldenrod')

# frame = tk.Frame(root, bg='chocolate')
# frame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)

'bouton de debut'
StartButton = tk.Button(root, text='Run', command=Start, bg='green', repeatinterval=500, repeatdelay=100)
StartButton.grid(row=13, column=0, sticky='W')

'bouton d arret'
StopButton = tk.Button(root, text='Stop', bg='red', command=Stop)
StopButton.grid(row=14, column=0, sticky='W')

'bouton qui ajoute de lagressivite'
AddAgressivityButton = tk.Button(root, text='add_Agressivity', command=add_Agressivity, bg='green')
AddAgressivityButton.grid(row=13, column=1, sticky='W')

'bouton qui enleve de lagressivite'
MinusAgressivityButton = tk.Button(root, text='minus_Agressivity', command=minus_Agressivity, bg='red')
MinusAgressivityButton.grid(row=14, column=1, sticky='W')

'bouton de vente total'
SellAllButton = tk.Button(root, text='Sell All', bg='red', command=SellAll)
SellAllButton.grid(row=15, column=1, sticky='W')

'bouton de seulement une vente'
SellButton = tk.Button(root, text='Sell One', bg='limegreen', command=SellOne)
SellButton.grid(row=16, column=1, sticky='W')

'Bouton de seulement une achat'
BuyButton = tk.Button(root, text='Buy One', bg='gold', command=BuyOne)
BuyButton.grid(row=17, column=1, sticky='W')

labelNowPrice = tk.Label(root, bg='gold')
labelNowPrice.grid(row=3, column=0, sticky='W')

labelBidPrice = tk.Label(root, bg='goldenrod')
labelBidPrice.grid(row=6, column=1, sticky='W')

labelAskPrice = tk.Label(root, bg='goldenrod')
labelAskPrice.grid(row=5, column=1, sticky='W')

labelNowGain = tk.Label(root, bg='gold')
labelNowGain.grid(row=4, column=0, sticky='W')

labelLastBuys = tk.Label(root, bg='gold')
labelLastBuys.grid(row=5, column=2, sticky='W', columnspan='5')

labelLastSells = tk.Label(root, bg='gold')
labelLastSells.grid(row=7, column=2, sticky='W')

labelNbSells = tk.Label(root, bg='gold')
labelNbSells.grid(row=7, column=0, sticky='W')

labelNbBuys = tk.Label(root, bg='gold')
labelNbBuys.grid(row=8, column=0, sticky='W')

labelNbUSDT = tk.Label(root, bg='gold')
labelNbUSDT.grid(row=9, column=0, sticky='W')

labelNbETH = tk.Label(root, bg='goldenrod', padx=5, pady=5)
labelNbETH.grid(row=10, column=0, sticky='W')

labelSellPrice = tk.Label(root, bg='goldenrod', padx=5, pady=5)
labelSellPrice.grid(row=6, column=0, sticky='W')

labelBuyPrice = tk.Label(root, bg='goldenrod', padx=5, pady=5)
labelBuyPrice.grid(row=5, column=0, sticky='W')

labelNbSellPossible = tk.Label(root, bg='gold')
labelNbSellPossible.grid(row=16, column=0, sticky='W')

labelSellAllNowGain = tk.Label(root, bg='gold')
labelSellAllNowGain.grid(row=15, column=0, sticky='W')

labelRunning = tk.Label(root, bg='gold')
labelRunning.grid(row=13, column=2, sticky='W')

#Creation of the LastSells LastBuys Label
######################################################################################
label_2x7Buys = [[0 for i in range(0,7)] for j in range(0,2 )]
label_2x7Sells = [[0 for i in range(0,7)] for j in range(0,2)]
for i in range(0,7):
    for j in range(0,2):
        label_2x7Buys[j][i] = tk.Label(root, bg='gold')
        label_2x7Buys[j][i].grid(row=j + 5, column=i + 4)

for i in range(0,7):
    for j in range(0,2):
        label_2x7Sells[j][i] = tk.Label(root, bg='gold')
        label_2x7Sells[j][i].grid(row=j + 7, column=i + 4)
######################################################################################
'ENTRY'
labelStartPrice = tk.Label(root, text='StartPrice: ', bg='gold')
e1 = tk.Entry(root)
e1.bind('<Return>', onReturn)
labelStartPrice.grid(row=11, column=0, sticky='W')
e1.grid(row=12, column=0, sticky='W')

'Premier affichage'
labelNowPrice.config(text='Prix: ' + str(Data.NowPrice['ETHUSDT']) + '  (USDT/ETH)')
labelBidPrice.config(text='Bid Price: ' + str(Data.BidPrice['ETHUSDT']))
labelAskPrice.config(text='Ask Price: ' + str(Data.AskPrice['ETHUSDT']))
labelNbETH.config(text='Qty ETH = ' + str(Data.LastBuys['ETHUSDT']['Qty']))
labelNbUSDT.config(text='Qty USDT = ' + str(Data.num_USDT))

root.mainloop()

# print(float(price['price']))