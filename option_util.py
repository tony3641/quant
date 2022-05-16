from cmath import sqrt
from pickle import FALSE
from statistics import variance
from symtable import Symbol
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm


class Option:
    __greek_keys__=['delta','gamma','theta','vega','rho','impVol']
    initialized= FALSE

    def __init__(self, stock_symbol, id):
        self.symbol=stock_symbol
        self.option_id=id

    def update_info(self, webull):
        quote=webull.get_option_quote(stock=self.symbol,optionId=self.option_id)
        data=quote['data'][0]
        self.direction=data['direction']
        self.expire=data['expireDate']
        self.strike=data['strikePrice']
        self.ask_price=float(data['askList'][0]['price'])
        self.bid_price=float(data['bidList'][0]['price'])
        self.greeks={greek_key: data[greek_key] for greek_key in self.__greek_keys__}
        self.name=data['symbol']

        self.initialized=True

    def display(self):
        if self.initialized is True:
            print(self.name+' bid='+str(self.bid_price)+', ask='+str(self.ask_price))
            print(str(self.greeks))
        else:
            raise ValueError('Warning: option info not updated yet, \
                please call Option.update_info().')

def get_option_positions(positions,webull=None):
    option_positions=[]
    for position in positions:
        if position['assetType']=='OPTION':
            ticker=position['ticker']
            symbol=ticker['symbol']
            option_id=position['tickerId']
            option=Option(symbol,option_id)
            if webull is not None:
                option.update_info(webull)
            option_positions.append(option)
    return option_positions

"""This function calculates  gain/loss of a strategy(a series of options) at the same expire date"""
def calc_gain_at_expire(close_price,strategy):
    profit=0
    for i in strategy:
        if i[0] == 'call':
            if i[2]<=close_price:
                profit+=(close_price-i[2]-i[3])*i[1]*100
            else:
                profit+=(-i[3])*i[1]*100
        if i[0] == 'put':
            if i[2]>=close_price:
                profit+=(i[2]-close_price-i[3])*i[1]*100
            else:
                profit+=(-i[3])*i[1]*100
        if i[0] == 'stock' or i[0] == 'spot':
            profit+=(close_price-i[3])*i[1]
    return profit

"""Please note: T here is in unit of year"""
def calc_delta(S, K, r, T, sigma, type):
    d1=(np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    if type=='call':
        delta=norm.cdf(d1,0,1)
    if type=='put':
        delta=-norm.cdf(-d1,0,1)
    return delta

def calc_gamma(S, K, r, T, sigma, type):
    d1=(np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    gamma=norm.pdf(d1,0,1)/(S*sigma*np.sqrt(T))
    return gamma

def calc_theta(S, K, r, T, sigma, type):
    d1=(np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    if type=='call':
        theta=-((S*norm.pdf(d1,0,1)*sigma)/(2*np.sqrt(T)))-r*K*np.exp(-r*T)*norm.cdf(d2,0,1)
    if type=='put':
        theta=-((S*norm.pdf(d1,0,1)*sigma)/(2*np.sqrt(T)))+r*K*np.exp(-r*T)*norm.cdf(-d2,0,1)
    return theta/365

def calc_vega(S, K, r, T, sigma):
    d1=(np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    vega=S*np.sqrt(T)*norm.pdf(d1,0,1)*0.01
    return vega

"""Calculate the theo value of a call/put based on Black Scholes model """
def black_scholes(S, K, r, T, sigma, direction):
    d1=(np.log(S/K)+(r+sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    if direction=='call':
        price=S*norm.cdf(d1,0,1)-K*np.exp(-r*T)*norm.cdf(d2,0,1)
    if direction=='put':
        price=K*np.exp(-r*T)*norm.cdf(-d2,0,1)-S*norm.cdf(-d1,0,1)
    return price


"""calculate the historic volatility of a stock, needed for black scholes"""
"""Input should be a list of consecutive daily close price"""
def calc_stock_volatility(period_close_price):
    r=[]
    for i in range(len(period_close_price)):
        if i>0:
            r.append(np.log(period_close_price[i]/period_close_price[i-1])) #daily log return
    r_avg=np.average(r)
    variance=0
    for i in range(len(r)):
        variance+=((r[i]-r_avg)**2)/(len(r)-1)
    std_dev=np.sqrt(252)*np.sqrt(variance) #annualized sd with 252 trading days per year
    return std_dev