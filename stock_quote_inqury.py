"""This script can inqury a stock quote and save to a csv using unofficial webull API"""
from webull import webull
import numpy as np
import pandas as pd
import sys

wb=webull()
df=pd.DataFrame()

if len(sys.argv)>3:
    if len(sys.argv)==4:
        stock,res,count=sys.argv[1:4]
        path='./'+stock.lower()+'-'+res+'-'+str(count)+'.csv'
        df=wb.get_bars(stock=stock,interval=res,count=count)
        df.to_csv(path)
        print('csv file output to: '+path)
    elif len(sys.argv)==5:
        stock,res,count,path=sys.argv[1:5]
        df=wb.get_bars(stock=stock,interval=res,count=count)
        df.to_csv(path)
    else:
        print('Too much arguments.')

else:
    if len(sys.argv)>1:
        print('Insufficient arguments.')
    inp=input('Enter stock symbol (q to quit):')
    while(inp != 'q'):
        stock=inp
        inp=input('Enter interval (m1, m5, m15, m30, h1, h2, h4, d1, w1):')
        res=inp
        inp=input('Enter count:')
        count=int(inp)
        df=wb.get_bars(stock=stock,interval=res,count=count)
        df.to_csv('./'+stock.lower+'-'+res+'-'+str(count)+'.csv')
        inp=input('Enter stock symbol (q to quit):')
