# Crypto_Exchange_ASK_BID_snoopy
Created in partnership with Milan Charniak (https://github.com/charnim)

*RUN IN LINUX, WINDOWS GAVE ME TROUBLE

Basic ASK:BID sniffer of BTC-USDT over multiple Exchanges.

BTC_USDT.py workflow:

1) Sends get request to an exchanges API's (You may want to adjust request timers)
2) Writes to memory
3) Gets from memory & writes to DB (sqlite3)
4) Also a e-mail notification function if something goes wrong (Needs input of your e-mail & password for sending e-mails & another e-mail address for recieving)

LIVE_GRAPH.py:
Run LIVE_GRAPH.py couple of seconds after launching the BTC_USDT.py (so it would have some data put to graph) to view the DATA(ASK:BID) in a graph.
Adjust name & password parameters or if not used comment them out.
