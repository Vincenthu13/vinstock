import requests
from twstock import Stock
from twstock import BestFourPoint
import twstock
import time
import pandas as pd
import yfinance as yf


def Average(lst):
    return sum(lst) / len(lst)

headers = {
    "Authorization": "Bearer " + "NE32czocHRl5Lck7ruO19egR2rghFjlMU9Ok5ibOnSB",
    "Content-Type": "application/x-www-form-urlencoded"
}

stock_list = ['2330','2884','3026','1227']
stock_name = ['台積電','玉山金','禾伸堂','佳格']



for i in range(len(stock_list)):
    time.sleep(15)
    stock = Stock(stock_list[i])
    bfp = BestFourPoint(stock)
    bfp.best_four_point()
    t_stock = twstock.realtime.get(stock_list[i])




    msg = "\n【"+t_stock['info']['name']+"】\n"
    msg +=  "開:"+t_stock['realtime']['open'][:6]+"\n"
    msg += "高:"+t_stock['realtime']['high'][:6]+"\n"
    msg += "低:"+t_stock['realtime']['low'][:6]+"\n"
    msg += "最新價格:"+t_stock['realtime']['latest_trade_price'][:6]+"\n"
    msg += "五日均價:"+str(Average(stock.moving_average(stock.price, 5)))[:6]+"\n"




    stockNoy = stock_list[i]+".TW"
    stocky = yf.Ticker(stockNoy)
    stock_df = pd.DataFrame(stocky.history(period="1y"))
    stock_df = stock_df.reset_index()
    stock_df = stock_df[::-1]
    stock_df_5 = stock_df.head(5)
    stock_df_30 = stock_df.head(30)
    stock_df_180 = stock_df.head(180)
    stock_df_365 = stock_df.head(365)
    # msg = "\n【"+stockNo+" - "+stock_name[i]+"】\n"
    # msg += "日期:"+str(stock_df.iloc[0]["Date"])+"\n"
    # msg += "開:"+str(stock_df.iloc[0]["Close"])+"\n"
    # msg += "高:"+str(stock_df.iloc[0]["High"])+"\n"
    # msg += "低:"+str(stock_df.iloc[0]["Low"])+"\n"
    msg += "月均價:"+str(stock_df_30["Close"].mean())[:6]+"\n"
    msg += "半年均價:"+str(stock_df_180["Close"].mean())[:6]+"\n"
    msg += "年均價:"+str(stock_df_365["Close"].mean())[:6]+"\n"


    msg += "四大買點:"+str(bfp.best_four_point_to_buy())+"\n"
    msg += "四大賣點:"+str(bfp.best_four_point_to_sell())+"\n"
    msg += "綜合判斷:"+str(bfp.best_four_point())

    print(msg)
    params = {"message": msg}
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)




