from webull import webull
import option_util
import numpy as np
import pandas as pd
import getpass

wb=webull()
loggedin=False
usr_id=input('Enter username:')
while(not loggedin):
    passwd=getpass.getpass('Enter password:')
    print("---Autheticating, this might take a while---")
    login_status=wb.login(username=usr_id,password=passwd)
    if 'accessToken' in login_status:
        print('Login successfully.')
        loggedin=True
    else:
        print(login_status['msg'])

trade_token=getpass.getpass('Enter 6-digit trade token:')
wb.get_trade_token(trade_token)

#wb.logout()
