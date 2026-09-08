import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

BOT_TOKEN = "8973913461:AAHEaH-Etk4z1PHout59FRFjD3x0ezc5DmA"
CHAT_ID = "1398969681"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram Send Error:", e)

send_telegram("✅ *BTC 30M Bot Updated!*\n24/7 Keep-Alive system active ho gaya hai.")

last_alert_bar_time = None

def check_setup():
    global last_alert_bar_time
    
    url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=1800&limit=3"
    res = requests.get(url, timeout=10).json()
    candles = res['data']['ohlc']
    
    prev = candles[-2]
    curr = candles[-1]
    
    p_time = prev['timestamp']
    p_open = float(prev['open'])
    p_high = float(prev['high'])
    p_low = float(prev['low'])
    p_close = float(prev['close'])
    
    c_high = float(curr['high'])
    c_low = float(curr['low'])
    
    prev_range = p_high - p_low
    
    is_ol = (p_open == p_low) and (p_close > p_open) and (prev_range >= 150.0)
    is_oh = (p_open == p_high) and (p_close < p_open) and (prev_range >= 150.0)
    
    if is_ol and (c_high > p_high) and (last_alert_bar_time != p_time):
        msg = (
            f"🚀 *BTC 30M BUY BREAKOUT (Bitstamp)*\n\n"
            f"🟢 *Previous Bar:* Exact Open=Low\n"
            f"📊 *Candle Range:* {prev_range:.2f} pts\n"
            f"🎯 *Breakout Price:* {c_high}\n"
            f"📈 High tod kar breakout trigger ho gaya!"
        )
        send_telegram(msg)
        last_alert_bar_time = p_time

    elif is_oh and (c_low < p_low) and (last_alert_bar_time != p_time):
        msg = (
            f"🔻 *BTC 30M SELL BREAKOUT (Bitstamp)*\n\n"
            f"🔴 *Previous Bar:* Exact Open=High\n"
            f"📊 *Candle Range:* {prev_range:.2f} pts\n"
            f"🎯 *Breakout Price:* {c_low}\n"
            f"📉 Low tod kar breakdown trigger ho gaya!"
        )
        send_telegram(msg)
        last_alert_bar_time = p_time

while True:
    try:
        check_setup()
    except Exception as e:
        print("Fetch Error:", e)
    time.sleep(5)
