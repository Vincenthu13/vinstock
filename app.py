import os
from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests
from twstock import Stock
from twstock import BestFourPoint
import twstock
import time
import pandas as pd
import yfinance as yf


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("wMd2r0LkaNZ4eJcoeDILS+D1BvAIbghFf+zy406Dp8ktg0n4HQ6gDlKh0FrPwGqMldRn7h02DcFk1XOLz9D48fqkYSdRmbvR2lYchggjrxZ421yx4jtYuJ+4tqOKn7y+CtFPxobd64u/3x9x+5i2uwdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.environ.get("3afec071f0d41f2668fa4f688f7ddd22"))

def Average(lst):
    return sum(lst) / len(lst)

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    if str(get_message).isdigit():
        try:
            stock = Stock(str(get_message))
            bfp = BestFourPoint(stock)
            bfp.best_four_point()
            t_stock = twstock.realtime.get(str(get_message))
            

            stockNoy = str(get_message)+".TW"
            stocky = yf.Ticker(stockNoy)
            stock_df_5d = pd.DataFrame(stocky.history(period="5d"))
            stock_df_1m = pd.DataFrame(stocky.history(period="1m"))
            stock_df_1y = pd.DataFrame(stocky.history(period="1y"))
            stock_df_3y = pd.DataFrame(stocky.history(period="3y"))
            stock_df_5d = stock_df_5d[::-1]
            stock_df_1m = stock_df_1m[::-1]
            stock_df_1y = stock_df_1y[::-1]
            stock_df_3y = stock_df_3y[::-1]


            dividends = pd.DataFrame(stocky.dividends)
            dividends = dividends[::-1]
            dividends = dividends.reset_index()

            msg = "【"+str(get_message)+"-"+t_stock['info']['name']+"】\n"
 

            msg += "開:"+str(t_stock['realtime']['open'])[:6]+"\n"
            msg += "高:"+str(t_stock['realtime']['high'])[:6]+"\n"
            msg += "低:"+str(t_stock['realtime']['low'])[:6]+"\n"
            msg += "最新價格:"+t_stock['realtime']['latest_trade_price'][:6]+"\n"
            msg += "五日均價:"+str(stock_df_5d["Close"].mean())[:6]+"\n"
            msg += "月均價:"+str(stock_df_1m["Close"].mean())[:6]+"\n"
            msg += "一年均價:"+str(stock_df_1y["Close"].mean())[:6]+"\n"
            msg += "三年均價:"+str(stock_df_3y["Close"].mean())[:6]+"\n"

            msg += "四大買點:"+str(bfp.best_four_point_to_buy())+"\n"
            msg += "四大賣點:"+str(bfp.best_four_point_to_sell())+"\n"
            msg += "綜合判斷:"+str(bfp.best_four_point())+"\n"

            msg += "***--------近期股利--------***\n"
            for i in range(len(dividends)):
                msg += str(dividends.iloc[i]["Date"])[:11]+" "+str(dividends.iloc[i]["Dividends"])+"\n"

            reply = TextSendMessage(msg)
            line_bot_api.reply_message(event.reply_token, reply)

        except Exception as Argument:
            msg = get_message+"-"+str(Argument)
            reply = TextSendMessage(text=msg)
            line_bot_api.reply_message(event.reply_token, reply)

        


