# Crypto_Exchange_ASK_BID_snoopy
Created in partnership with Milan Charniak (https://github.com/charnim)

Basic ASK:BID sniffer of BTC-USDT over multiple Exchanges.

BTC_USDT.py workflow:

1) Sends get request to an exchanges API's (You may want to adjust request timers)
2) Writes to memory
3) Gets from memory & writes to DB (sqlite3)
4) Also a e-mail notification function if something goes wrong (Needs input of your e-mail & password for sending e-mails & another e-mail address for recieving)

Graph.py:
Run Graph.py couple of seconds after launching the BTC_USDT.py to view the DATA(ASK:BID) in a graph.
Adjust name & password parameters or if not used comment them out.
