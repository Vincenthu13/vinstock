import yfinance as yf
import pandas as pd


stockNoy = "1234.TW"
stocky = yf.Ticker(stockNoy)




stock_df_5d = pd.DataFrame(stocky.history(period="5d"))
stock_df_1m = pd.DataFrame(stocky.history(period="1m"))
stock_df_6m = pd.DataFrame(stocky.history(period="6m"))
stock_df_1y = pd.DataFrame(stocky.history(period="1y"))



stock_df_5d = stock_df_5d[::-1]
stock_df_1m = stock_df_1m[::-1]
stock_df_6m = stock_df_6m[::-1]
stock_df_1y = stock_df_1y[::-1]
dividends = pd.DataFrame(stocky.dividends)
dividends = dividends[::-1]
dividends = dividends.reset_index()

msg = "\n【"+stockNoy+"】\n"
msg += "開:"+str(stock_df_5d.iloc[0]["Open"])+"\n"
msg += "高:"+str(stock_df_5d.iloc[0]["High"])+"\n"
msg += "低:"+str(stock_df_5d.iloc[0]["Low"])+"\n"
msg += "收:"+str(stock_df_5d.iloc[0]["Close"])+"\n"
msg += "月均價:"+str(stock_df_1m["Close"].mean())[:6]+"\n"
msg += "半年均價:"+str(stock_df_6m["Close"].mean())[:6]+"\n"
msg += "年均價:"+str(stock_df_1y["Close"].mean())[:6]+"\n"
msg += "--------近期股利--------\n"
for i in range(len(dividends)):
    msg += str(dividends.iloc[i]["Date"])[:11]+" "+str(dividends.iloc[i]["Dividends"])+"\n"
print(msg)