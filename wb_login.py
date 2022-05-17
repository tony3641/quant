from matplotlib.pyplot import flag
from webull import webull
import my_quant_util
import numpy as np
import pandas as pd
import getpass

wb=webull()
loggedin=False
cmd=''
local_order_id=0
order={}
usr_id=input('Enter username:')
while(not loggedin):
    passwd=getpass.getpass('Enter password:')
    print('\n---Autheticating, this might take a while---\n')
    login_status=wb.login(username=usr_id,password=passwd)
    if 'accessToken' in login_status:
        print('Login successfully.\n')
        loggedin=True
    else:
        print(login_status['msg'])

trade_token_authed=False
while(not trade_token_authed):
    trade_token=getpass.getpass('Enter 6-digit trade token:')
    trade_token_authed=wb.get_trade_token(trade_token)
print('Trade token autherized. Ready to order now\n')
positions=wb.get_positions()
print('--------------  Your stock positions  -------------')
print('\n')
option_positions=my_quant_util.get_option_positions(positions,wb)
print('-------------  Your option positions  -------------')
for option_position in option_positions:
    option_position.display_position()
print('---------------------------------------------------')
while(True):
    cmd=input('quant_sys$:') #COMMAND TICKER QUANT PRICE
    if cmd == 'q!' :
        break
    else:
        flags=cmd.split()

    if flags[0]=='BUYSTOCKLMT':
        ret=wb.place_order(stock=flags[1],quant=int(flags[2]),price=int(flags[3]))
        if(ret['success']==True):
            order.update({local_order_id:{'remoteId':ret['data']['orderId'],\
                'stock':flags[1],'quantity':flags[2],'price':flags[3],'type':'BUYLMT'}})
            print('order success, local order id='+str(local_order_id))
            local_order_id+=1
    elif flags[0]=='BUYSTOCKMKT':
        wb.place_order(stock=flags[1],quant=int(flags[2]),orderType='MKT')
        if(ret['success']==True):
            order.update({local_order_id:ret['data']['orderId']})
            print('order success, local order id='+str(local_order_id))
            local_order_id+=1
    elif flags[0]=='CANCEL':
        if flags[1]=='ALL':
            wb.cancel_all_orders()
            print('All orders canceled.')
        else:
            ret=wb.cancel_order(order_id=order[int(flags[1])]['remoteId'])
            if(ret==True):
                print(str(order[int(flags[1])]['type'])+' '+str(order[int(flags[1])]['stock'])\
                    +' '+str(order[int(flags[1])]['quantity'])+' '+str(order[int(flags[1])]['price'])\
                    +' canceled.')
    else:
        print('Error.')

if(wb.logout()>=0):
    print('Logged out.')
