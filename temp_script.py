#You need to copy paste condition in below mentioned Condition variable

Condition = "( {cash} ( 1 week ago max( 10 , 1 week ago close ) < 1 week ago min( 10 , 1 week ago close ) * 1.15 and weekly volume > 1 week ago volume and weekly close >= weekly open and weekly close > 1 week ago max( 10 , 1 week ago close ) and 1 week ago  close <= 2 week ago  max( 10 , 1 week ago close ) and net profit[quarter] >= 1 and weekly close > 50 ) )"
 

sleeptime = 900
import telebot
from time import sleep
import os
import warnings
import sys
warnings.filterwarnings("ignore")
import datetime

try:
    import xlwings as xw
except (ModuleNotFoundError, ImportError):
    print("xlwings module not found")
    os.system(f"{sys.executable} -m pip install -U xlwings")
finally:
    import xlwings as xw
    
try:
    import requests
except (ModuleNotFoundError, ImportError):
    print("requests module not found")
    os.system(f"{sys.executable} -m pip install -U requests")
finally:
    import requests

try:
    import pandas as pd
except (ModuleNotFoundError, ImportError):
    print("pandas module not found")
    os.system(f"{sys.executable} -m pip install -U pandas")
finally:
    import pandas as pd
    
try:
    from bs4 import BeautifulSoup
except (ModuleNotFoundError, ImportError):
    print("BeautifulSoup module not found")
    os.system(f"{sys.executable} -m pip install -U beautifulsoup4")
finally:
    from bs4 import BeautifulSoup
    
    
Charting_Link = "https://chartink.com/screener/"
Charting_url = 'https://chartink.com/screener/process'


def GetDataFromChartink(payload):
    payload = {'scan_clause': payload}
    
    with requests.Session() as s:
        r = s.get(Charting_Link)
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.select_one("[name='csrf-token']")['content']
        s.headers['x-csrf-token'] = csrf
        r = s.post(Charting_url, data=payload)

        df = pd.DataFrame()
        for item in r.json()['data']:
            
            if len(item) > 0:
                df = pd.concat([df, pd.DataFrame.from_dict(item,orient='index').T],ignore_index = True)
            
    return df


try:
    if not os.path.exists('Chartink_Result.xlsm'):
        wb = xw.Book()
        wb.save('Chartink_Result.xlsm')
        wb.close()

    wb = xw.Book('Chartink_Result.xlsm')
    try:
        result = wb.sheets('Chartink_Result')
    except Exception as e:
        wb.sheets.add('Chartink_Result')
        result = wb.sheets('Chartink_Result')
except Exception as e:
    pass
    
while True:
    
    
    data = GetDataFromChartink(Condition)
    screened_stocks=pd.DataFrame(data)

    if len(data) > 0:
        data = data.sort_values(by='per_chg',ascending=False)

        print(f"\n\n{data}")
        
        try:
            result.range('a:h').value = None
            result.range('a1').options(index=False).value = data
        except Exception as e:
            pass
   
    

    bot_token = '6499086834:AAHPQWd9YenVWV0sfmXrGB-doKo0LxMle90'
    chat_id = '-1001933568192'
    bot = telebot.TeleBot(bot_token)
    
    screened_stocks_list = list(screened_stocks['nsecode'])
    screened_stocks.to_csv(f'Darvas_box_{datetime.date.today()}.csv', index=False)

    message = " Darvas Box Weekly Breakout- Buy:\n"

    for stock in screened_stocks_list:
        # Assuming 'screened_stocks' contains stock data with columns like 'nsecode' and 'per_chg'
        stock_data = screened_stocks[screened_stocks['nsecode'] == stock]

        if not stock_data.empty:
            stock_name = stock
            change = stock_data.iloc[0]['per_chg']   # Convert to percentage
            current_time = datetime.datetime.now().strftime('%m-%d %H:%M') 
            close = stock_data.iloc[0]['close']

            # Create a line for each stock
            stock_line = f"- {stock_name}  {close}  {change:.2f}%   {current_time}\n"

            # Add the line to the message
            message += stock_line

    # Send the message
    bot.send_message(chat_id, text=message)

    

    sleep(sleeptime)
            