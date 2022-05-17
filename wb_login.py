from webull import webull
import my_quant_util
import numpy as np
import pandas as pd
import getpass

wb=webull()
loggedin=False
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
print('Trade token autherized. Ready to order now\n\n')

positions=wb.get_positions()
option_positions=my_quant_util.get_option_positions(positions,wb)
for option_position in option_positions:
    option_position.display_position()

while(input() != 'q!'):
    print('Enter next command.')


if(wb.logout()>=0):
    print('Logged out.')
