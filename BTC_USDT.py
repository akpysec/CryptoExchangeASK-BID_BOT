import sys
import requests
from multiprocessing import Queue
import sqlite3
from time import time, sleep
from datetime import datetime
from multiprocessing import Process
import simplejson
import random
import socket
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import traceback


class API:

    def __init__(self, market_name: str, url: str, bid_unpack: str, ask_unpack: str, rate_limit: float):
        self.market_name = market_name
        self.url = url
        self.bid_unpack = bid_unpack
        self.ask_unpack = ask_unpack
        self.rate_limit = rate_limit
        self.HTTPResponse = None

    def get(self):

        """This method is responsible for checking connection errors only"""

        try:

            sleep(self.rate_limit)

            self.HTTPResponse = requests.get(self.url, timeout=5)

            return self.HTTPResponse.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as ConError:  # If no internet

            self.error_log(market=str(self.market_name), exception=str(ConError))

            try:
                print('No connection on {0}, checking if blocked...'.format(self.market_name))

                requests.get("https://google.com")

                print('{0} API is blocking you, sleeping for 10 seconds'.format(self.market_name))

                sleep(15)

                print('{0} has finished waiting'.format(self.market_name))

            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as NoInternet:

                self.error_log(market=str(self.market_name), exception=str(NoInternet))
                print('No Internet connection, waiting for 5 seconds')
                sleep(5)

        except simplejson.errors.JSONDecodeError as StrangeAnswer:
            print('{0} API response is strange, pleases see logs, maybe blocked? waiting for 15 seconds'.format(
                self.market_name))
            sleep(15)
            self.error_log(market=str(self.market_name), exception=str(StrangeAnswer), unique=True,
                           response=self.HTTPResponse.text)
            print('{0} has finished waiting'.format(self.market_name))
            self.HTTPResponse = None

    def unpack(self):

        try:
            bid = eval('{0}'.format(self.bid_unpack))
            ask = eval('{0}'.format(self.ask_unpack))
            query = (time(), self.market_name, bid, ask)
            return query

        except (ValueError, KeyError, IndexError) as BadUnpack:  # Passed all exceptions but is malformes
            self.error_log(market=str(self.market_name), exception=str(BadUnpack), unique=True,
                           response=self.HTTPResponse.text)

            return False

    def to_mem_to_db(self, memo: Queue):
        try:
            if self.unpack():
                memo.put(self.unpack())

        except (TypeError, KeyError, IndexError) as Type:
            self.error_log(market=str(self.market_name), exception=str(Type), response=self.HTTPResponse.text)
            print("Got bad response, waiting 10 seconds")
            sleep(15)

    def error_log(self, market: str, exception: str, response='None', unique=False) -> None:
        try:
            db_logs = sqlite3.connect("script_error_logs.sqlite")
            db_logs.execute(
                "CREATE TABLE IF NOT EXISTS logs (time FLOAT, market TEXT not null, exception TEXT not null, "
                "HTTPResponse TEXT, state BOOLEAN NOT NULL CHECK (state IN (0,1)))")
            db_input = "INSERT INTO logs(time, market, exception, HTTPResponse, state) VALUES(?, ?, ?, ?, ?)"
            update_db_input = db_logs.cursor()
            update_db_input.execute(db_input, (datetime.now(), market, exception, response, unique))

            db_logs.commit()
            db_logs.close()

        except sqlite3.OperationalError:  # Got DBBlocked so we wait until its up
            print('Captain we got blocked by the DB on {0}, no worries!'.format(market))
            sleep(random.uniform(0.001, 0.02))
            self.error_log(market=market, exception=exception, response=response, unique=unique)


class BinanceBTC(API):
    def __init__(self):
        super().__init__(market_name='Binance',
                         url='https://api.binance.com/api/v1/ticker/24hr?symbol=BTCUSDT',
                         bid_unpack="float(dict(self.HTTPResponse.json())['bidPrice'])",
                         ask_unpack="float(dict(self.HTTPResponse.json())['askPrice'])",
                         rate_limit=1.0)


class BitfinexBTC(API):
    def __init__(self):
        super().__init__(market_name='Bitfinex',
                         url='https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUST',
                         bid_unpack="float(list(self.HTTPResponse.json()[0])[1])",
                         ask_unpack="float(list(self.HTTPResponse.json()[0])[3])",
                         rate_limit=1.0)


class BitmaxBTC(API):
    def __init__(self):
        super().__init__(market_name='Bitmax',
                         url='https://bitmax.io/api/v1/quote?symbol=BTC-USDT',
                         bid_unpack="float(dict(self.HTTPResponse.json())['bidPrice'])",
                         ask_unpack="float(dict(self.HTTPResponse.json())['askPrice'])",
                         rate_limit=1.0
                         )


class BittrexBTC(API):
    def __init__(self):
        super().__init__(market_name='Bittrex',
                         url='https://api.bittrex.com/api/v1.1/public/getticker?market=USDT-BTC',
                         bid_unpack="float(dict(self.HTTPResponse.json()['result'])['Bid'])",
                         ask_unpack="float(dict(self.HTTPResponse.json()['result'])['Ask'])",
                         rate_limit=1.0)


class HitbtcBTC(API):
    def __init__(self):
        super().__init__(market_name='Hitbtc',
                         url='https://api.hitbtc.com/api/2/public/ticker/BTCUSD',
                         bid_unpack="float(self.HTTPResponse.json()['bid'])",
                         ask_unpack="float(self.HTTPResponse.json()['ask'])",
                         rate_limit=1.0)


class HuobiBTC(API):
    def __init__(self):
        super().__init__(market_name='Huobi',
                         url='https://api.huobi.pro/market/detail/merged?symbol=btcusdt',
                         bid_unpack="float(list(dict(self.HTTPResponse.json()['tick'])['bid'])[0])",
                         ask_unpack="float(list(dict(self.HTTPResponse.json()['tick'])['ask'])[0])",
                         rate_limit=1.0)


class KrakenBTC(API):
    def __init__(self):
        super().__init__(market_name='Kraken',
                         url='https://api.kraken.com/0/public/Ticker?pair=XBTUSD',
                         bid_unpack="float(self.HTTPResponse.json()['result']['XXBTZUSD']['b'][0])",
                         ask_unpack="float(self.HTTPResponse.json()['result']['XXBTZUSD']['a'][0])",
                         rate_limit=1.0)


class KucoinBTC(API):
    def __init__(self):
        super().__init__(market_name='Kucoin',
                         url='https://openapi-v2.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT',
                         bid_unpack="float(dict(self.HTTPResponse.json()['data'])['bestBid'])",
                         ask_unpack="float(dict(self.HTTPResponse.json()['data'])['bestAsk'])",
                         rate_limit=1.0)



class OkcoinBTC(API):
    def __init__(self):
        super().__init__(market_name='Okcoin',
                         url='https://www.okcoin.com/api/spot/v3/instruments/BTC-USDT/ticker',
                         bid_unpack="float(dict(self.HTTPResponse.json())['bid'])",
                         ask_unpack="float(dict(self.HTTPResponse.json())['ask'])",
                         rate_limit=1.0)



db_name = list()
if sys.platform.startswith('win'):
    db_name.append('btc_usdt_db.sqlite')
elif sys.platform == 'linux':
    db_name.append('btc_usdt_db.sqlite')


def start():
    procs = []
    proc = [BinanceBTC, BitfinexBTC, BitmaxBTC, BittrexBTC, HitbtcBTC, HuobiBTC, KrakenBTC, KucoinBTC, OkcoinBTC]
    master_memory = Queue()  # I am the common memory space for everyone!

    for pr in proc:
        def run_exchange(memo: Queue):
            try:
                while True:

                    exchange = pr()
                    response = exchange.get()

                    if response is not None:  # There was no http response - no connection?
                        exchange.to_mem_to_db(memo=memo)

            except Exception:
                send_mail(body=f'Error:\n{proc.name} CRASHED ({pr.__name__})\n')

        proc = Process(target=run_exchange, args=(master_memory,))
        procs.append(proc)
        proc.start()

    db = sqlite3.connect(*db_name)
    db.execute("CREATE TABLE IF NOT EXISTS 'cage' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
               "'time' FLOAT, 'name' TEXT not null, USDBid FLOAT, "
               "USDAsk FLOAT)")
    db_input = "INSERT OR IGNORE INTO cage('id', 'time', 'name', 'USDBid', 'USDAsk') VALUES(NULL, ?, ?, ?, ?)"

    while True:
        data = master_memory.get()
        update_db_input = db.cursor()
        update_db_input.execute(db_input, (data[0], data[1], data[2], data[3],))
        db.commit()


def send_mail(body: str):
    host = socket.gethostname()
    sender_email = "ENTER YOUR E-MAIL HERE"
    receiver_email = "WHERE TO SEND NOTIFICATION"   # , mail@mail.com, mail@mail.com
    password = 'PASSWORD FOR SENDING E-MAIL'

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Error Occurred at {host} Server"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"\n{body}\n{traceback.format_exc()}\nFor more information, Connect to the server"
    part = MIMEText(text, "plain")
    message.attach(part)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email.split(','), message.as_string())
            print('Email sent to Admins!')
    except Exception as B:
        print(f"Email was not Sent, Something went wrong...\n{B}")


if __name__ == "__main__":
    try:
        start()
    except Exception:
        send_mail(body=f'Error:\n')
