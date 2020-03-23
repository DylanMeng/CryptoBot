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

'fonction ecrire vente qui documente les donnees de la vente courrante  dans le fichier txt de log'
# def ecrire_vente_fichier():
#    global TimeNow, gain, excel, LasBuys, nb_sell, nb_buy

#    fichier = open(Data.Fichier, 'a')
#    fichier.write('Prix de vente: ' + str(Data.NowPrice)+ '  Balance_ETH:  ' + str(Data.gain))
#    fichier.write('  Date:  ' + str(datetime.today()))
#    fichier.write('   Temps: ' + str(TimeNow) + '  \n \t LastBuy: ' + str(Data.LastBuys) + '  \n \t LastSells:' + str(Data.LastSells)+ '   \nNbETH: ' + str(Data.num_ETH) +'\n' )
#    print('   SELL!!!!!')
#    fichier.close()


'fonction ecrire achat qui documente les donnees de l achat courrante  dans le fichier txt de log'


# def ecrire_achat_fichier():
#    global  TimeNow, gain, excel, nb_sell, nb_buy

#    fichier = open(Data.Fichier, 'a')
#    fichier.write('Prix de dachat: ' + str(Data.NowPrice) + '  Balance_ETH:  ' + str(Data.gain))
#    fichier.write('  Date:  ' + str(datetime.today()))
#    fichier.write('   Temps: ' + str(TimeNow) + '  \n \t LastBuys: ' + str(Data.LastBuys) + '  \n \t LastSell:' + str(Data.LastSells)+ '   \nNbETH:  ' + str(Data.num_ETH) + '\n' )
#    print('   BUY!!!!!')
#    fichier.close()

def log_condition():
    # Ouvrir le fichier en write mode clear son contenu
    fichier = open(Data.Fichier, "w")

    fichier.write('TimeNow: {}\n'.format(Data.TimeNow))
    fichier.write('NowPrice: {}\n'.format(Data.NowPrice))
    fichier.write('num_ETH: {}\n'.format(Data.num_ETH))
    fichier.write('num_USDT: {}\n'.format(Data.num_USDT))
    fichier.write('gain: {}\n'.format(Data.gain))
    fichier.write('BidPrice: {}\n'.format(Data.BidPrice))
    fichier.write('AskPrice: {}\n'.format(Data.AskPrice))
    fichier.write('NbVentePossible: {}\n'.format(Data.NbVentePossible))
    fichier.write('SellAllNowGain: {}\n'.format(Data.SellAllNowGain))
    fichier.write('BuyPrice: {}\n'.format(Data.BuyPrice))
    fichier.write('SellPrice: {}\n'.format(Data.SellPrice))
    fichier.write('LastBuys: {}\n'.format(Data.LastBuys['ETHUSDT']))
    fichier.write('LastSells: {}\n'.format(Data.LastSells['ETHUSDT']))
    fichier.write('nb_sell: {}\n'.format(Data.nb_sell))
    fichier.write('nb_buy: {}\n'.format(Data.nb_buy))
    # fichier.write('nb_Timeout: {}'.format(Data.nb_Timeout))
    # fichier.write('nb_ConnectionError: {}'.format(Data.nb_ConnectionError))
    # fichier.write('nb_VIP: {}'.format(Data.nb_VIP))

    fichier.close()


def ecrire_vente_excel():
    row = Data.nb_sell + Data.nb_buy
    worksheet1.write(row, 0, 'VENTE')
    worksheet1.write(row, 1, Data.NowPrice)
    worksheet1.write(row, 2, Data.gain)
    worksheet1.write(row, 3, str(Data.TimeNow))
    worksheet1.write(row, 4, Data.num_ETH)
    worksheet1.write(row, 5, 'LastBuys: ')
    for i in range(len(Data.LastBuys['ETHUSDT'])):
        worksheet1.write(row, i + 6, Data.LastBuys['ETHUSDT'][i]['Price'])
    worksheet1.write(row, 7 + len(Data.LastBuys['ETHUSDT']), 'LastSells')
    for i in range(len(Data.LastSells['ETHUSDT'])):
        worksheet1.write(row, i + 8 + len(Data.LastBuys['ETHUSDT']), Data.LastSells['ETHUSDT'][i]['Price'])
    print('   SELL!')

def ecrire_achat_excel():
    row = Data.nb_sell + Data.nb_buy
    worksheet1.write(row, 0, 'ACHAT')
    worksheet1.write(row, 1, Data.NowPrice)
    worksheet1.write(row, 2, Data.gain)
    worksheet1.write(row, 3, str(Data.TimeNow))
    worksheet1.write(row, 4, Data.num_ETH)
    worksheet1.write(row, 5, 'LastBuys')
    for i in range(len(Data.LastBuys['ETHUSDT'])):
        worksheet1.write(row, i + 6, Data.LastBuys['ETHUSDT'][i]['Price'])
    worksheet1.write(row, 7 + len(Data.LastBuys['ETHUSDT']), 'LastSells')
    for i in range(len(Data.LastSells['ETHUSDT'])):
        worksheet1.write(row, i + 8 + len(Data.LastBuys['ETHUSDT']), Data.LastSells['ETHUSDT'][i]['Price'])
    print('   BUY!')


def get_NbCryp():
    info = client.get_account()
    for assets in info['balances']:
        # if(assets['asset'] == 'ETH'):
        #    Data.num_ETH = float(assets['free'])
        if (assets['asset'] == 'USDT'):
            Data.num_USDT = float(assets['free'])


def cancel_order(side):
    if side == "Sell":
        try:
            client.cancel_order(symbol='ETHUSDT', orderId=Data.SellOrderId['orderId'])
            print('Sell Order canceled')
        except Exception as e:
            print("Sell Order Cancel has not worked: Id: {}, Exception: {} ".format(Data.SellOrderId['orderId'], e))
            exit()
    elif side == "Buy":
        try:
            client.cancel_order(symbol='ETHUSDT', orderId=Data.BuyOrderId['orderId'])
            print('Buy Order canceled')
        except Exception as e:
            print("Buy Order Cancel has not worked: Id: {}, Exception: {} ".format(Data.BuyOrderId['orderId'], e))
            exit()

def add_LastBuydic(Order):
    # function that add the new Buy to a dic (Should only be used in order_filled function)
    newBuydic = {'Price': Order['price'],
                 'Qty':   float(Order['executedQty'])}

    Data.LastBuys[Order['symbol']].insert(0,newBuydic)
    #trie du plus cher aux moinx cher
    Data.LastBuys[Order['symbol']] = sorted(Data.LastBuys[Order['symbol']], key= lambda i: i['Price'])

def add_LastSelldic(Order):
    # function that add the new Buy to a dic (Should only be used in order_filled function)
    newSelldic = {'Price': Order['price'],
                 'Qty':   float(Order['executedQty'])}

    Data.LastSells[Order['symbol']].insert(0,newSelldic)
    #trie du plus cher aux moinx cher
    Data.LastSells[Order['symbol']] = sorted(Data.LastSells[Order['symbol']], key= lambda i: i['Price'],reverse=True)


def order_filled(side):
    if side == "Buy":
        try:
            Order = client.get_order(symbol='ETHUSDT',
                                     orderId=Data.BuyOrderId['orderId'])
            if (Order['status'] == 'FILLED'):
                print("Buy order is filled")
                # Gain de ETH (Should not be like that)
                Data.num_ETH += float(Order['executedQty'])
                # on ajoute l achat courrant a la liste
                add_LastBuydic(Order)
                #LastBuys_price_average()
                # Si possible, on enleve la vente qui a ete utilise pour lachat
                if (len(Data.LastSells['ETHUSDT']) > 0):
                    Data.LastSells['ETHUSDT'].pop(0)
                # gain, on compte egalement les fees (0.06% du trade)
                Data.gain -= float(Order['executedQty']) * float(Order['price']) * 1.0006
                return True
        except Exception as e:
            print("Buy Order info could not be fetch: Id: {}, Exception: {} ".format(Data.BuyOrderId['orderId'], e))
            return False

    elif side == "Sell":
        try:
            Order = client.get_order(symbol='ETHUSDT',
                                     orderId=Data.SellOrderId['orderId'])
            if (Order['status'] == 'FILLED'):
                print("Sell order is filled")
                # Perte de ETH (Should not be like that)
                Data.num_ETH -= float(Order['executedQty'])
                # on ajoute l achat courrant a la liste
                add_LastSelldic(Order)
                # LastBuys_price_average()
                # Si possible, on enleve la vente qui a ete utilise pour lachat
                if (len(Data.LastBuys['ETHUSDT']) > 1):
                    Data.LastBuys['ETHUSDT'].pop(0)
                #LastBuys_price_average()
                # gain, on compte egalement les fees (0.06% du trade)
                Data.gain += float(Order['executedQty']) * float(Order['price']) * 0.9994
                return True
        except Exception as e:
            print("Sell Order info could not be fetch: Id: {}, Exception: {} ".format(Data.SellOrderId['orderId'], e))
            return False

    elif side == "Shadow":
        if Data.ShadowOrderId['orderId'] == 0:
            return False
        try:
            Order = client.get_order(symbol='ETHUSDT',
                                     orderId=Data.ShadowOrderId['orderId'])
            if (Order['status'] == 'FILLED'):
                print("Shadow order is filled")
                # Perte de ETH
                # Perte de ETH
                Data.num_ETH -= float(Order['executedQty'])
                newBuySelldic = {'Price': str(Order['price']),
                                 'Qty': 0}
                Data.LastBuys['ETHUSDT'].clear()
                Data.LastSells['ETHUSDT'].clear()
                Data.LastBuys['ETHUSDT'].insert(0, newBuySelldic)
                Data.num_ETH -= float(Order['executedQty'])
                # Si possible, on enleve l'achat qui a ete utilise pour la vente
                if (len(Data.LastBuys['ETHUSDT']) > 1):
                    Data.LastBuys['ETHUSDT'].pop(0)
                    #LastBuys_price_average()
                # gain, on compte egalement les fees (0.06% du trade)
                Data.gain += float(Order['executedQty']) * float(Order['price']) * 0.9994
                Data.ShadowOrderId['orderId'] = 0
                return True

        except Exception as e:
            print("Shadow Order info could not be fetch: Id: {}, Exception: {} ".format(Data.ShadowOrderId['orderId'], e))
            return False


def set_agressivity():
    Data.Buy_multiplication_list = [i * Data.Agressivity for i in Data.Buy_multiplication_list]
    Data.Last_Agressivity = Data.Agressivity

#Algo principale de vente et achat
def calculate_trigger_prices():

    if Data.Agressivity != Data.Last_Agressivity:
        set_agressivity()

    #lengh of the 2 lists
    lenLastBuys = len(Data.LastBuys['ETHUSDT'])
    lenLastSells = len(Data.LastSells['ETHUSDT'])
    #Best price to compare to
    Last_Buy = float(Data.LastBuys['ETHUSDT'][0]['Price'])
    if lenLastSells > 0:
        Last_Sell = float(Data.LastSells['ETHUSDT'][0]['Price'])
    #to display on the GUI
    Data.NbVentePossible = (lenLastBuys - 1)

    #Si aucun achat de realise (condition initiale + pas de vente permise)
    if ((lenLastBuys == 1) and (lenLastSells == 0)):
        Data.BuyPrice = Last_Buy - (Data.Buy_multiplication_list[lenLastBuys-1] ** 1.3) * 0.0025 * Last_Buy
        Data.SellPrice = 999999
    #Si aucun achat restant et ventes réalisés dans le passé (on se base sur la derniere vente + Pas de vente permise)
    elif ((lenLastBuys == 1) and (lenLastSells > 0)):
        Data.LastSells['ETHUSDT'].clear()
        Data.BuyPrice = Last_Sell - (Data.Buy_multiplication_list[lenLastBuys-1] ** 1.3) * 0.0025 * Last_Sell
        Data.SellPrice = 999999
    #Si achats dans lasBuys (on se base sur les derniers achats)
    else:
        Data.BuyPrice = Last_Buy - (Data.Buy_multiplication_list[lenLastBuys-1] ** 1.3) * 0.0025 * Last_Buy
        Data.SellPrice = Last_Buy + (Data.Sell_multiplication_list[lenLastSells] ** 1.2) * 0.00255 * Last_Buy


def LastBuys_price_average():
    for pair in Data.LastBuys.keys():
        Sum = 0
        Qty = 0
        for Buydict in Data.LastBuys[pair]:
            Sum += float(Buydict['Price'])*Buydict['Qty']
            Qty += Buydict['Qty']
        Data.LastBuys[pair.keys()]['Price_Average'] = Sum/Qty
        Data.LastBuys[pair.keys()]['Sum'] = Sum
        Data.LastBuys[pair.keys()]['Qty'] = Qty

def get_Prix():
    price = client.get_symbol_ticker(symbol='ETHUSDT')
    Book = client.get_order_book(symbol='ETHUSDT')
    Data.BidPrice = float(Book['bids'][0][0])
    Data.AskPrice = float(Book['asks'][0][0])
    Data.NowPrice = float(price['price'])



def Verif_Achat():
    # Verifie l'achat et ajoute celle-ci aux lasbuys
    if (order_filled("Buy") == True):
        # Un achat de plus
        Data.nb_buy += 1
        #RefreshLastBuysSells()
        'Nouveau prix de vente et d achat'
        calculate_trigger_prices()
        #Refer to list in Data.py to for buy Qty
        nb_achat = Data.Buys_Qty[len(Data.LastBuys['ETHUSDT']) - 1]
        # Nouvelle achat
        Acheter(prix=Data.BuyPrice, nb_achat=nb_achat)

        # Si vente possible
        if (len(Data.LastBuys['ETHUSDT']) > 1):
            if (len(Data.LastBuys['ETHUSDT']) > 2):
                # On cancele la vente pour une nouvelle a jour avec lachat
                cancel_order("Sell")
            # nouvelle vente or (Data.LastBuys['ETHUSDT'][0]['Qty']
            nb_vente = (1 / (len(Data.LastBuys['ETHUSDT']) - 1)) * Data.num_ETH
            Vendre(prix=Data.SellPrice, nb_vente=nb_vente)


def Verif_Vente():
    if (len(Data.LastBuys['ETHUSDT']) > 1):
        # Verifie la vente et ajoute celle-ci aux lasBuys
        if (order_filled("Sell") == True):
            # Une vente de plus
            Data.nb_sell += 1
            #RefreshLastBuysSells()
            #Calculer prochain les prix d'achat et de vente
            calculate_trigger_prices()
            # On cancele lordre dachat pour la mettre a jour avec la derniere vente
            cancel_order("Buy")
            # Refer to list in Data.py to for buy Qty
            nb_achat = Data.Buys_Qty[len(Data.LastBuys['ETHUSDT']) - 1]
            Acheter(prix=Data.BuyPrice, nb_achat=nb_achat)
            # nouvelle Vente (si possible)
            if (len(Data.LastBuys['ETHUSDT']) > 1):
                # nouvelle vente or (Data.LastBuys[0]['Qty']
                nb_vente = (1 / (len(Data.LastBuys['ETHUSDT']) - 1)) * Data.num_ETH
                Vendre(prix=Data.SellPrice, nb_vente=nb_vente)


'Fonction qui achette a un prix et une quantité donnée'


def shadow_Sell():
    # If there is nothing else to sell focus on the shadow sell
    if (len(Data.LastBuys['ETHUSDT']) == 1):
        if (order_filled('Shadow')):
            Data.nb_sell += 1
            #RefreshLastBuysSells()
            calculate_trigger_prices()
            # On cancele lordre dachat pour la mettre a jour avec la derniere vente
            cancel_order("Buy")
            # Refer to list in Data.py to for buy Qty
            nb_achat = Data.Buys_Qty[len(Data.LastBuys['ETHUSDT']) - 1]
            Acheter(prix=Data.BuyPrice, nb_achat=nb_achat)


def Acheter(prix, nb_achat):
    try:
        Data.BuyOrderId = client.order_limit_buy(symbol='ETHUSDT',
                                                 quantity=round(nb_achat, 5),
                                                 price=str(round(prix, 2)))
        print('Buy Order Sent => QTY: {} ETH, PRICE: {} USDT/ETH'.format(nb_achat, prix))
    except Exception as e:
        print('Buy Order could not be send! Exception: {}'.format(e))
        exit()


'Fonction qui vend a un prix et une quantité donnée'


def Vendre(prix, nb_vente):
    try:
        Data.SellOrderId = client.order_limit_sell(symbol='ETHUSDT',
                                                   quantity=round(nb_vente, 5),
                                                   price=str(round(prix, 2)))
        print('Sell Order Sent => QTY: {} ETH, PRICE: {} USDT/ETH'.format(nb_vente, prix))
    except Exception as e:
        print('Sell Order could not be send! Exception: {}'.format(e))
        exit()


def SellAll(prix):
    while (Data.NbVentePossible > 0):
        Vendre(prix=prix, nb_vente=Data.num_ETH)


def SellOne():
    Vendre(prix=Buy)


def BuyOne():
    Acheter(1)


'Fonction TirtyMin qui historise le prix au 30 min et qui achete si le prix a changer brusquemment***Cas de blockage achat'


def TirtyMin():
    if (Data.TimeNow - Data.TimeTirty > timedelta(minutes=15)):
        Data.TimeTirty = Data.TimeNow
        Data.TirtyMinLast = Data.TirtyMinNew
        Data.TirtyMinNew = Data.NowPrice
        print('Tirty Min')
        if (len(Data.LastBuys['ETHUSDT']) == 1 and Data.TirtyMinNew < 0.99 * Data.TirtyMinLast):
            Data.nb_VIP += 1
            Acheter(1)


get_NbCryp()
get_Prix()

'-------------------------------------------------------------------------------------------------------------------------------------------'
'APPLICATION'
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
    Data.LastBuys['ETHUSDT'].clear()
    Data.LastSells['ETHUSDT'].clear()
    Data.LastBuys['ETHUSDT'].insert(0, newBuySelldic)

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
    Data.BuyPrice = float(Data.LastBuys['ETHUSDT'][0]['Price']) - (Data.Buy_multiplication_list[0] ** 1.3) * 0.0025 * float(Data.LastBuys['ETHUSDT'][0]['Price'])
    Data.SellPrice = 99999
    labelSellPrice.config(text='Prix de vente: ' + str(Data.SellPrice))
    labelBuyPrice.config(text='Prix de d achat: ' + str(Data.BuyPrice))
    labelLastBuys.config(text='Derniers achats: ')
    labelLastSells.config(text='Dernieres ventes: ')
    #Premiere ordre d'achat
    Acheter(prix=Data.BuyPrice, nb_achat=Data.Buys_Qty[len(Data.LastBuys['ETHUSDT'])-1])
    #Shadow 4% higher than start price
    Data.ShadowPrice = 1.025*Data.BuyPrice
    #Data.ShadowOrderId = client.order_limit_sell(symbol='ETHUSDT',
    #                                             quantity=round(0.1, 5),
    #                                             price=str(round(Data.ShadowPrice, 2)))
    e1.delete(0, 'end')

def RefreshLastBuysSells():
    global label_2x7Buys, label_2x7Sells
    #Working on a clean way to display the list of dict
    if(len(Data.LastBuys['ETHUSDT']) > 0):
        i = 0
        for Buy in Data.LastBuys['ETHUSDT']:
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
    if (len(Data.LastSells['ETHUSDT']) > 0):
        i = 0
        for Sell in Data.LastSells['ETHUSDT']:
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
    labelNowPrice.config(text='Prix: ' + str(Data.NowPrice) + '  (USDT/ETH)')
    labelBidPrice.config(text='Bid Price: ' + str(Data.BidPrice))
    labelAskPrice.config(text='Ask Price: ' + str(Data.AskPrice))
    labelNowGain.config(text='Gain: ' + str(Data.gain) + '  (USDT)')
    labelNbBuys.config(text='Nb dachat: ' + str(Data.nb_buy))
    labelNbSells.config(text='Nb de vente: ' + str(Data.nb_sell))
    labelNbETH.config(text='Nb de ETH: ' + str(Data.num_ETH))
    labelNbUSDT.config(text='Qty USDT = ' + str(Data.num_USDT))
    labelSellPrice.config(text='Prix de vente: ' + str(Data.SellPrice))
    labelBuyPrice.config(text='Prix de d achat: ' + str(Data.BuyPrice))
    labelNbSellPossible.config(text='Nb de vente possible: ' + str(Data.NbVentePossible))
    labelSellAllNowGain.config(text='Gain si vente total: ' + str(Data.SellAllNowGain))


'-------------------------------------------------------------------------------------------------------------------------------------------'
'PRINCIPALE BOUCLE UTILISE POUR ROULER LE PROGRAMME'
'utilisation de after() pour boucler a tous les secondes lorsquon appuie sur RUN et '
'et arreter lors que l on appuie sur STOP'
'-------------------------------------------------------------------------------------------------------------------------------------------'


def Start():
    labelRunning.config(text='Le programme Run mon homme !')
    breakout = root.after(2500, Start)
    if (Data.stop == False):
        try:
            get_Prix()
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
        # Regarder si la vente ou lachat a été filled
        Verif_Achat()
        Verif_Vente()
        #shadow_Sell()
        print(str(Data.LastBuys))
        print(str(Data.LastSells))
        print("ShadowSellPrice: {}".format(Data.ShadowPrice))
        print(Data.Buy_multiplication_list)
        print(Data.Sell_multiplication_list)
        # Fonction de vérification d'achat au 30 min
        # TirtyMin()
        Data.SellAllNowGain = Data.gain + Data.num_ETH * Data.BidPrice
        RefreshApp()
        log_condition()
    else:
        Data.stop = False
        labelRunning.config(text='Not running')
        root.after_cancel(breakout)


def Stop():
    fichier = open(Data.Fichier, 'a')
    ETH_fin = Data.gain + Data.num_ETH * Data.BidPrice

    'Conclusion du fichier de log'
    print('STOP')
    fichier.write('Dernier PRIX:   ' + str(Data.NowPrice) + '\n')
    fichier.write('Nb de USDT a la fin(si on vend tout nos ETH la) en comptant les fees:  ' + str(ETH_fin) + '\n')
    fichier.write('Nb de vente:  ' + str(Data.nb_sell) + '\n')
    fichier.write('Nb de dachat:  ' + str(Data.nb_buy) + '\n')
    fichier.write('Nb de ConnectionError:  ' + str(Data.nb_ConnectionError) + '\n')
    fichier.write('Nb de Timeout:  ' + str(Data.nb_Timeout) + '\n')
    fichier.write('LastBuys:  ' + str(Data.LastBuys['ETHUSDT']) + '\n')
    fichier.write('LastSells:  ' + str(Data.LastSells['ETHUSDT']) + '\n')
    fichier.write('SellAllNowGain:  ' + str(Data.SellAllNowGain) + '\n')
    fichier.write('NbVIP:  ' + str(Data.nb_VIP) + '\n')

    Data.stop = True
    excel.close()


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
labelNowPrice.config(text='Prix: ' + str(Data.NowPrice) + '  (USDT/ETH)')
labelBidPrice.config(text='Bid Price: ' + str(Data.BidPrice))
labelAskPrice.config(text='Ask Price: ' + str(Data.AskPrice))
labelNbETH.config(text='Qty ETH = ' + str(Data.num_ETH))
labelNbUSDT.config(text='Qty USDT = ' + str(Data.num_USDT))

root.mainloop()

# print(float(price['price']))