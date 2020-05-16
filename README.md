# Crypto_Exchange_ASK_BID_snoopy
Created in partnership with Milan Charniak (https://github.com/charnim)

*RUN IN LINUX, WINDOWS GAVE ME TROUBLE

Use python 3.6+
Basic ASK:BID sniffer of BTC-USDT over multiple Exchanges.

BTC_USDT.py workflow:

1) Sends get request to an exchanges API's (You may want to adjust request timers)
2) Writes to memory
3) Gets from memory & writes to DB (sqlite3)
4) Also a e-mail notification function if something goes wrong (Needs input of your e-mail & password for sending e-mails & another e-mail address for recieving)

LIVE_GRAPH.py:
Run LIVE_GRAPH.py couple of seconds after launching the BTC_USDT.py (so it would have some data put to graph) to view the DATA(ASK:BID) in a graph.
Adjust name & password parameters or if not used comment them out.

Best practice is to run in TMUX like so:

    Start a new session with the following command + debugging in case it crashes: tmux -vv new -s SESSION_NAME

    Check for running sessions: tmux ls

    Connect to specific session: tmux attach -t SESSION_NAME

    Split screen: Ctrl + b Shift + " - for horizontal split Shift + % - for vertical split

    Move between windows: Ctrl + b arrow key - up/down/left/right

    Kill session: exit

If there's a need to update version of a running script, you MUST kill all previous processes with:

pkill python3

and only after launch a new script, otherwise you will get DB locked.

