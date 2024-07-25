
import websocket
import json
import pandas as pd
from datetime import datetime

symbol = 'btcusdt'
socket = f'wss://stream.binance.com:9443/ws/{symbol}@kline_1s'

columns = ['Open', 'High', 'Low', 'Close', 'Volume']
df = pd.DataFrame(columns=columns)
df.index.name = 'Event Time'

def on_message(ws, message):
    global df
    msg = json.loads(message)
    out = msg['k']

    # Event Time
    event_time = pd.to_datetime(msg['E'], unit='ms')
    # Open price
    open = float(out['o'])
    # High price
    high = float(out['h'])
    #Low price
    low = float(out['l'])
    # Close price
    close = float(out['c'])
    # Volume 
    volume = float(out['v'])
    
    # Append the new data to the DataFrame
    new_row = pd.DataFrame({'Open': open, 'High': high, 'Low': low, 
                            'Close': close, 'Volume': volume}, index=[event_time])
    
    new_row.index.name = 'Event Time'
    df = pd.concat([df, new_row])
    

    print(df)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("---------- CLOSED FINE----------")

def on_open(ws):
    print("---------- OPENED CONNECTION ----------")

ws = websocket.WebSocketApp(socket,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()