'''
https://github.com/websocket-client/websocket-client
'''
import json, time
from websocket import create_connection

for i in range(3):
	try:
		ws = create_connection("wss://ws-sandbox.kraken.com")
	except Exception as error:
		print('Caught this error: ' + repr(error))
		time.sleep(3)
	else:
		break

ws.send(json.dumps({
	"event": "subscribe",
	#"event": "ping",
	"pair": ["XBT/USD", "XBT/EUR"],
	#"subscription": {"name": "ticker"}
	#"subscription": {"name": "spread"}
	"subscription": {"name": "trade"}
	#"subscription": {"name": "book", "depth": 10}
	#"subscription": {"name": "ohlc", "interval": 5}
}))

while True:
	try:
		result = ws.recv()
		result = json.loads(result)
		print ("Received '%s'" % result, time.time())
	except Exception as error:
		print('Caught this error: ' + repr(error))
		time.sleep(3)

ws.close()

# Import Built-Ins
import logging
import json
import time
import ssl
import hashlib
import hmac
from multiprocessing import Queue
from threading import Thread, Event, Timer
from collections import OrderedDict

# Import Third-Party
import websocket

# Import Homebrew

# Init Logging Facilities
log = logging.getLogger(__name__)


class WebSocketConnection(Thread):
    """Websocket Connection Thread
    Inspired heavily by ekulyk's PythonPusherClient Connection Class
    https://github.com/ekulyk/PythonPusherClient/blob/master/pusherclient/connection.py
    It handles all low-level system messages, such a reconnects, pausing of
    activity and continuing of activity.
    """
    def __init__(self, *args, url=None, timeout=None, sslopt=None,
                 http_proxy_host=None, http_proxy_port=None, http_proxy_auth=None, http_no_proxy=None,
                 reconnect_interval=None, log_level=None, **kwargs):
        """Initialize a WebSocketConnection Instance.
        :param data_q: Queue(), connection to the Client Class
        :param args: args for Thread.__init__()
        :param url: websocket address, defaults to v2 websocket.
        :param http_proxy_host: proxy host name.
        :param http_proxy_port: http proxy port. If not set, set to 80.
        :param http_proxy_auth: http proxy auth information.
                                tuple of username and password.
        :param http_no_proxy: host names, which doesn't use proxy. 
        :param timeout: timeout for connection; defaults to 10s
        :param reconnect_interval: interval at which to try reconnecting;
                                   defaults to 10s.
        :param log_level: logging level for the connection Logger. Defaults to
                          logging.INFO.
        :param kwargs: kwargs for Thread.__ini__()
        """
        # Queue used to pass data up to BTFX client
        self.q = Queue()

        # Connection Settings
        self.socket = None
        self.url = url if url else 'wss://api.bitfinex.com/ws/2'
        self.sslopt = sslopt if sslopt else {}

        # Proxy Settings
        self.http_proxy_host = http_proxy_host
        self.http_proxy_port = http_proxy_port
        self.http_proxy_auth = http_proxy_auth
        self.http_no_proxy = http_no_proxy

        # Dict to store all subscribe commands for reconnects
        self.channel_configs = OrderedDict()

        # Connection Handling Attributes
        self.connected = Event()
        self.disconnect_called = Event()
        self.reconnect_required = Event()
        self.reconnect_interval = reconnect_interval if reconnect_interval else 10
        self.paused = Event()

        # Setup Timer attributes
        # Tracks API Connection & Responses
        self.ping_timer = None
        self.ping_interval = 120

        # Tracks Websocket Connection
        self.connection_timer = None
        self.connection_timeout = timeout if timeout else 10

        # Tracks responses from send_ping()
        self.pong_timer = None
        self.pong_received = False
        self.pong_timeout = 30

        self.log = logging.getLogger(self.__module__)
        if log_level == logging.DEBUG:
            websocket.enableTrace(True)
        self.log.setLevel(level=log_level if log_level else logging.INFO)

        # Call init of Thread and pass remaining args and kwargs
        Thread.__init__(self)
        self.daemon = True
        # Use default Bitfinex websocket configuration parameters
        self.bitfinex_config = None

    def disconnect(self):
        """Disconnects from the websocket connection and joins the Thread.
        :return:
        """
        self.log.debug("disconnect(): Disconnecting from API..")
        self.reconnect_required.clear()
        self.disconnect_called.set()
        if self.socket:
            self.socket.close()
        self.join(timeout=1)

    def reconnect(self):
        """Issues a reconnection by setting the reconnect_required event.
        :return:
        """
        # Reconnect attempt at self.reconnect_interval
        self.log.debug("reconnect(): Initialzion reconnect sequence..")
        self.connected.clear()
        self.reconnect_required.set()
        if self.socket:
            self.socket.close()

    def _connect(self):
        """Creates a websocket connection.
        :return:
        """
        self.log.debug("_connect(): Initializing Connection..")
        self.socket = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )

        if 'ca_certs' not in self.sslopt.keys():
            ssl_defaults = ssl.get_default_verify_paths()
            self.sslopt['ca_certs'] = ssl_defaults.cafile

        self.log.debug("_connect(): Starting Connection..")
        self.socket.run_forever(sslopt=self.sslopt,
                        http_proxy_host=self.http_proxy_host,
                        http_proxy_port=self.http_proxy_port,
                        http_proxy_auth=self.http_proxy_auth,
                        http_no_proxy=self.http_no_proxy)

        # stop outstanding ping/pong timers
        self._stop_timers()
        while self.reconnect_required.is_set():
            if not self.disconnect_called.is_set():
                self.log.info("Attempting to connect again in %s seconds."
                              % self.reconnect_interval)
                self.state = "unavailable"
                time.sleep(self.reconnect_interval)

                # We need to set this flag since closing the socket will
                # set it to False
                self.socket.keep_running = True
                self.socket.sock = None
                self.socket.run_forever(sslopt=self.sslopt,
                                http_proxy_host=self.http_proxy_host,
                                http_proxy_port=self.http_proxy_port,
                                http_proxy_auth=self.http_proxy_auth,
                                http_no_proxy=self.http_no_proxy)
            else:
                break

    def run(self):
        """Main method of Thread.
        :return:
        """
        self.log.debug("run(): Starting up..")
        self._connect()

    def _on_message(self, ws, message):
        """Handles and passes received data to the appropriate handlers.
        :return:
        """
        self._stop_timers()

        raw, received_at = message, time.time()
        self.log.debug("_on_message(): Received new message %s at %s",
                       raw, received_at)
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Something wrong with this data, log and discard
            return

        # Handle data
        if isinstance(data, dict):
            # This is a system message
            self._system_handler(data, received_at)
        else:
            # This is a list of data
            if data[1] == 'hb':
                self._heartbeat_handler()
            else:
                self._data_handler(data, received_at)

        # We've received data, reset timers
        self._start_timers()

    def _on_close(self, ws, *args):

        self.connected.clear()
        self._stop_timers()

        if not self.disconnect_called.is_set():
            self.log.info("Connection is closed by Bitfinex.")
            for arg in args:
                self.log.info("Closing reason: %s" % arg)
            self.reconnect_required.set()
        else:
            self.log.info("Connection is closed normally.")

    def _on_open(self, ws):
        self.log.info("Connection opened")
        self.connected.set()
        self.send_ping()
        self._start_timers()
        if self.reconnect_required.is_set():
            self.log.info("_on_open(): Connection reconnected, re-subscribing..")
            self._resubscribe(soft=False)

    def _on_error(self, ws, error):
        self.log.info("Connection Error - %s", error)
        self.reconnect_required.set()
        self.connected.clear()

    def _stop_timers(self):
        """Stops ping, pong and connection timers.
        :return:
        """
        if self.ping_timer:
            self.ping_timer.cancel()

        if self.connection_timer:
            self.connection_timer.cancel()

        if self.pong_timer:
            self.pong_timer.cancel()
        self.log.debug("_stop_timers(): Timers stopped.")

    def _start_timers(self):
        """Resets and starts timers for API data and connection.
        :return:
        """
        self.log.debug("_start_timers(): Resetting timers..")
        self._stop_timers()

        # Sends a ping at ping_interval to see if API still responding
        self.ping_timer = Timer(self.ping_interval, self.send_ping)
        self.ping_timer.start()

        # Automatically reconnect if we didnt receive data
        self.connection_timer = Timer(self.connection_timeout,
                                      self._connection_timed_out)
        self.connection_timer.start()

    def send_ping(self):
        """Sends a ping message to the API and starts pong timers.
        :return:
        """
        self.log.debug("send_ping(): Sending ping to API..")
        self.socket.send(json.dumps({'event': 'ping'}))
        self.pong_timer = Timer(self.pong_timeout, self._check_pong)
        self.pong_timer.start()

    def _check_pong(self):
        """Checks if a Pong message was received.
        :return:
        """
        self.pong_timer.cancel()
        if self.pong_received:
            self.log.debug("_check_pong(): Pong received in time.")
            self.pong_received = False
        else:
            # reconnect
            self.log.debug("_check_pong(): Pong not received in time."
                           "Issuing reconnect..")
            self.reconnect()

    def send(self, api_key=None, secret=None, list_data=None, auth=False, **kwargs):
        """Sends the given Payload to the API via the websocket connection.
        :param kwargs: payload paarameters as key=value pairs
        :return:
        """
        if auth:
            nonce = str(int(time.time() * 10000000))
            auth_string = 'AUTH' + nonce
            auth_sig = hmac.new(secret.encode(), auth_string.encode(),
                                hashlib.sha384).hexdigest()

            payload = {'event': 'auth', 'apiKey': api_key, 'authSig': auth_sig,
                       'authPayload': auth_string, 'authNonce': nonce}
            payload = json.dumps(payload)
        elif list_data:
            payload = json.dumps(list_data)
        else:
            payload = json.dumps(kwargs)
        self.log.debug("send(): Sending payload to API: %s", payload)
        try:
            self.socket.send(payload)
        except websocket.WebSocketConnectionClosedException:
            self.log.error("send(): Did not send out payload %s - client not connected. ", kwargs)

    def pass_to_client(self, event, data, *args):
        """Passes data up to the client via a Queue().
        :param event:
        :param data:
        :param args:
        :return:
        """
        self.q.put((event, data, *args))

    def _connection_timed_out(self):
        """Issues a reconnection if the connection timed out.
        :return:
        """
        self.log.debug("_connection_timed_out(): Fired! Issuing reconnect..")
        self.reconnect()

    def _pause(self):
        """Pauses the connection.
        :return:
        """
        self.log.debug("_pause(): Setting paused() Flag!")
        self.paused.set()

    def _unpause(self):
        """Unpauses the connection.
        Send a message up to client that he should re-subscribe to all
        channels.
        :return:
        """
        self.log.debug("_unpause(): Clearing paused() Flag!")
        self.paused.clear()
        self.log.debug("_unpause(): Re-subscribing softly..")
        self._resubscribe(soft=True)

    def _heartbeat_handler(self):
        """Handles heartbeat messages.
        :return:
        """
        # Restart our timers since we received some data
        self.log.debug("_heartbeat_handler(): Received a heart beat "
                       "from connection!")
        self._start_timers()

    def _pong_handler(self):
        """Handle a pong response.
        :return:
        """
        # We received a Pong response to our Ping!
        self.log.debug("_pong_handler(): Received a Pong message!")
        self.pong_received = True

    def _system_handler(self, data, ts):
        """Distributes system messages to the appropriate handler.
        System messages include everything that arrives as a dict,
        or a list containing a heartbeat.
        :param data:
        :param ts:
        :return:
        """
        self.log.debug("_system_handler(): Received a system message: %s", data)
        # Unpack the data
        event = data.pop('event')
        if event == 'pong':
            self.log.debug("_system_handler(): Distributing %s to _pong_handler..",
                      data)
            self._pong_handler()
        elif event == 'info':
            self.log.debug("_system_handler(): Distributing %s to _info_handler..",
                      data)
            self._info_handler(data)
        elif event == 'error':
            self.log.debug("_system_handler(): Distributing %s to _error_handler..",
                      data)
            self._error_handler(data)
        elif event in ('subscribed', 'unsubscribed', 'conf', 'auth', 'unauth'):
            self.log.debug("_system_handler(): Distributing %s to "
                           "_response_handler..", data)
            self._response_handler(event, data, ts)
        else:
            self.log.error("Unhandled event: %s, data: %s", event, data)

    def _response_handler(self, event, data, ts):
        """Handles responses to (un)subscribe and conf commands.
        Passes data up to client.
        :param data:
        :param ts:
        :return:
        """
        self.log.debug("_response_handler(): Passing %s to client..", data)
        self.pass_to_client(event, data, ts)

    def _info_handler(self, data):
        """
        Handle INFO messages from the API and issues relevant actions.
        :param data:
        :param ts:
        """

        def raise_exception():
            """Log info code as error and raise a ValueError."""
            self.log.error("%s: %s", data['code'], info_message[data['code']])
            raise ValueError("%s: %s" % (data['code'], info_message[data['code']]))

        if 'code' not in data and 'version' in data:
            self.log.info('Initialized Client on API Version %s', data['version'])
            return

        info_message = {20000: 'Invalid User given! Please make sure the given ID is correct!',
                        20051: 'Stop/Restart websocket server '
                                 '(please try to reconnect)',
                        20060: 'Refreshing data from the trading engine; '
                                 'please pause any acivity.',
                        20061: 'Done refreshing data from the trading engine.'
                                 ' Re-subscription advised.'}

        codes = {20051: self.reconnect, 20060: self._pause,
                 20061: self._unpause}

        if 'version' in data:
            self.log.info("API version: %i", data['version'])
            return

        try:
            self.log.info(info_message[data['code']])
            codes[data['code']]()
        except KeyError as e:
            self.log.exception(e)
            self.log.error("Unknown Info code %s!", data['code'])
            raise

    def _error_handler(self, data):
        """
        Handle Error messages and log them accordingly.
        :param data:
        :param ts:
        """
        errors = {10000: 'Unknown event',
                  10001: 'Generic error',
                  10008: 'Concurrency error',
                  10020: 'Request parameters error',
                  10050: 'Configuration setup failed',
                  10100: 'Failed authentication',
                  10111: 'Error in authentication request payload',
                  10112: 'Error in authentication request signature',
                  10113: 'Error in authentication request encryption',
                  10114: 'Error in authentication request nonce',
                  10200: 'Error in un-authentication request',
                  10300: 'Subscription Failed (generic)',
                  10301: 'Already Subscribed',
                  10302: 'Unknown channel',
                  10400: 'Subscription Failed (generic)',
                  10401: 'Not subscribed',
                  11000: 'Not ready, try again later',
                  20000: 'User is invalid!',
                  20051: 'Websocket server stopping',
                  20060: 'Websocket server resyncing',
                  20061: 'Websocket server resync complete'
                  }
        try:
            self.log.error(errors[data['code']])
        except KeyError:
            self.log.error("Received unknown error Code in message %s! "
                           "Reconnecting..", data)

    def _data_handler(self, data, ts):
        """Handles data messages by passing them up to the client.
        :param data:
        :param ts:
        :return:
        """
        # Pass the data up to the Client
        self.log.debug("_data_handler(): Passing %s to client..",
                  data)
        self.pass_to_client('data', data, ts)

    def _resubscribe(self, soft=False):
        """Resubscribes to all channels found in self.channel_configs.
        :param soft: if True, unsubscribes first.
        :return: None
        """
        # Restore non-default Bitfinex websocket configuration
        if self.bitfinex_config:
            self.send(**self.bitfinex_config)
        q_list = []
        while True:
            try:
                identifier, q = self.channel_configs.popitem(last=True if soft else False)
            except KeyError:
                break
            q_list.append((identifier, q.copy()))
            if identifier == 'auth':
                self.send(**q, auth=True)
                continue
            if soft:
                q['event'] = 'unsubscribe'
            self.send(**q)

        # Resubscribe for soft start.
        if soft:
            for identifier, q in reversed(q_list):
                self.channel_configs[identifier] = q
                self.send(**q)
        else:
            for identifier, q in q_list:
                self.channel_configs[identifier] = q


##btfxwss/btfxwss/client.py /
# Import Built-Ins
import logging
import time

# Import Homebrew
from btfxwss.connection import WebSocketConnection
from btfxwss.queue_processor import QueueProcessor


# Init Logging Facilities
log = logging.getLogger(__name__)


def is_connected(func):
    def wrapped(self, *args, **kwargs):
        if self.conn and self.conn.connected.is_set():
            return func(self, *args, **kwargs)
        else:
            log.error("Cannot call %s() on unestablished connection!",
                      func.__name__)
            return None
    return wrapped


class BtfxWss:
    """Websocket Client Interface to Bitfinex WSS API
    It features separate threads for the connection and data handling.
    Data can be accessed using the provided methods.
    """

    def __init__(self, key=None, secret=None, log_level=None, **wss_kwargs):
        """
        Initializes BtfxWss Instance.
        :param key: Api Key as string
        :param secret: Api secret as string
        :param addr: Websocket API Address
        """
        self.key = key if key else ''
        self.secret = secret if secret else ''

        self.conn = WebSocketConnection(log_level=log_level,
                                        **wss_kwargs)
        self.queue_processor = QueueProcessor(self.conn.q,
                                              log_level=log_level)

    ##############
    # Properties #
    ##############
    @property
    def channel_configs(self):
        return self.conn.channel_configs

    @property
    def account(self):
        return self.queue_processor.account

    ##############################################
    # Client Initialization and Shutdown Methods #
    ##############################################

    def start(self):
        """Start the client.
        :return:
        """
        self.conn.start()
        self.queue_processor.start()

    def stop(self):
        """Stop the client.
        :return:
        """
        self.conn.disconnect()
        self.queue_processor.join()

    def reset(self):
        """Reset the client.
        :return:
        """
        self.conn.reconnect()
        while not self.conn.connected.is_set():
            log.info("reset(): Waiting for connection to be set up..")
            time.sleep(1)

        for key in self.channel_configs:
            self.conn.send(**self.channel_configs[key])

    ##########################
    # Data Retrieval Methods #
    ##########################

    def tickers(self, pair):
        """Return a queue containing all received ticker data.
        :param pair:
        :return: Queue()
        """
        key = ('ticker', pair)
        return self.queue_processor.tickers[key]

    def books(self, pair):
        """Return a queue containing all received book data.
        :param pair:
        :return: Queue()
        """
        key = ('book', pair)
        return self.queue_processor.books[key]

    def raw_books(self, pair):
        """Return a queue containing all received raw book data.
        :param pair:
        :return: Queue()
        """
        key = ('raw_book', pair)
        return self.queue_processor.raw_books[key]

    def trades(self, pair):
        """Return a queue containing all received trades data.
        :param pair:
        :return: Queue()
        """
        key = ('trades', pair)
        return self.queue_processor.trades[key]

    def candles(self, pair, timeframe=None):
        """Return a queue containing all received candles data.
        :param pair: str, Symbol pair to request data for
        :param timeframe: str
        :return: Queue()
        """
        timeframe = '1m' if not timeframe else timeframe
        key = ('candles', pair, timeframe)
        return self.queue_processor.candles[key]

    ##########################################
    # Subscription and Configuration Methods #
    ##########################################

    def _subscribe(self, channel_name, identifier, **kwargs):
        q = {'event': 'subscribe', 'channel': channel_name}
        q.update(**kwargs)
        log.debug("_subscribe: %s", q)
        self.conn.send(**q)
        self.channel_configs[identifier] = q

    def _unsubscribe(self, channel_name, identifier, **kwargs):

        channel_id = self.channel_configs[identifier]
        q = {'event': 'unsubscribe', 'chanId': channel_id}
        q.update(kwargs)
        self.conn.send(**q)
        self.channel_configs.pop(identifier)

    def config(self, decimals_as_strings=True, ts_as_dates=False,
               sequencing=False, ts=False, **kwargs):
        """Send configuration to websocket server
        :param decimals_as_strings: bool, turn on/off decimals as strings
        :param ts_as_dates: bool, decide to request timestamps as dates instead
        :param sequencing: bool, turn on sequencing
	:param ts: bool, request the timestamp to be appended to every array
               sent by the server
        :param kwargs:
        :return:
        """
        flags = 0
        if decimals_as_strings:
            flags += 8
        if ts_as_dates:
            flags += 32
        if ts:
            flags += 32768
        if sequencing:
            flags += 65536
        q = {'event': 'conf', 'flags': flags}
        q.update(kwargs)
        self.conn.bitfinex_config = q
        self.conn.send(**q)

    @is_connected
    def subscribe_to_ticker(self, pair, **kwargs):
        """Subscribe to the passed pair's ticker channel.
        :param pair: str, Symbol pair to request data for
        :param kwargs:
        :return:
        """
        identifier = ('ticker', pair)
        self._subscribe('ticker', identifier, symbol=pair, **kwargs)

    @is_connected
    def unsubscribe_from_ticker(self, pair, **kwargs):
        """Unsubscribe to the passed pair's ticker channel.
        :param pair: str, Symbol pair to request data for
        :param kwargs:
        :return:
        """
        identifier = ('ticker', pair)
        self._unsubscribe('ticker', identifier, symbol=pair, **kwargs)

    @is_connected
    def subscribe_to_order_book(self, pair, **kwargs):
        """Subscribe to the passed pair's order book channel.
        :param pair: str, Symbol pair to request data for
        :param kwargs:
        :return:
        """
        identifier = ('book', pair)
        self._subscribe('book', identifier, symbol=pair, **kwargs)

    @is_connected
    def unsubscribe_from_order_book(self, pair, **kwargs):
        """Unsubscribe to the passed pair's order book channel.
        :param pair: str, Symbol pair to request data for
        :param kwargs:
        :return:
        """
        identifier = ('book', pair)
        self._unsubscribe('book', identifier, symbol=pair, **kwargs)

    @is_connected
    def subscribe_to_raw_order_book(self, pair, prec=None, **kwargs):
        """Subscribe to the passed pair's raw order book channel.
        :param pair: str, Symbol pair to request data for
        :param prec:
        :param kwargs:
        :return:
        """
        identifier = ('raw_book', pair)
        prec = 'R0' if prec is None else prec
        self._subscribe('book', identifier, pair=pair, prec=prec, **kwargs)

    @is_connected
    def unsubscribe_from_raw_order_book(self, pair, prec=None, **kwargs):
        """Unsubscribe to the passed pair's raw order book channel.
        :param pair: str, Symbol pair to request data for
        :param prec:
        :param kwargs:
        :return:
        """
        identifier = ('raw_book', pair)
        prec = 'R0' if prec is None else prec
        self._unsubscribe('book', identifier, pair=pair, prec=prec, **kwargs)

    @is_connected
    def subscribe_to_trades(self, pair, **kwargs):
        """Subscribe to the passed pair's trades channel.
        :param pair: str, Symbol pair to request data for
        :param kwargs:
        :return:
        """
        identifier = ('trades', pair)
        self._subscribe('trades', identifier, symbol=pair, **kwargs)

    @is_connected
    def unsubscribe_from_trades(self, pair, **kwargs):
        """Unsubscribe to the passed pair's trades channel.
        :param pair: str, Symbol pair to request data for
        :param kwargs:
        :return:
        """
        identifier = ('trades', pair)
        self._unsubscribe('trades', identifier, symbol=pair, **kwargs)

    @is_connected
    def subscribe_to_candles(self, pair, timeframe=None, **kwargs):
        """Subscribe to the passed pair's OHLC data channel.
        :param pair: str, Symbol pair to request data for
        :param timeframe: str, {1m, 5m, 15m, 30m, 1h, 3h, 6h, 12h,
                                1D, 7D, 14D, 1M}
        :param kwargs:
        :return:
        """

        valid_tfs = ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D',
                     '7D', '14D', '1M']
        if timeframe:
            if timeframe not in valid_tfs:
                raise ValueError("timeframe must be any of %s" % valid_tfs)
        else:
            timeframe = '1m'
        identifier = ('candles', pair, timeframe)
        pair = 't' + pair if not pair.startswith('t') else pair
        key = 'trade:' + timeframe + ':' + pair
        self._subscribe('candles', identifier, key=key, **kwargs)

    @is_connected
    def unsubscribe_from_candles(self, pair, timeframe=None, **kwargs):
        """Unsubscribe to the passed pair's OHLC data channel.
        :param timeframe: str, {1m, 5m, 15m, 30m, 1h, 3h, 6h, 12h,
                                1D, 7D, 14D, 1M}
        :param kwargs:
        :return:
        """

        valid_tfs = ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D',
                     '7D', '14D', '1M']
        if timeframe:
            if timeframe not in valid_tfs:
                raise ValueError("timeframe must be any of %s" % valid_tfs)
        else:
            timeframe = '1m'
        identifier = ('candles', pair, timeframe)
        pair = 't' + pair if not pair.startswith('t') else pair
        key = 'trade:' + timeframe + ':' + pair

        self._unsubscribe('candles', identifier, key=key, **kwargs)

    @is_connected
    def authenticate(self):
        """Authenticate with the Bitfinex API.
        :return:
        """
        if not self.key and not self.secret:
            raise ValueError("Must supply both key and secret key for API!")
        self.channel_configs['auth'] = {'api_key': self.key, 'secret': self.secret}
        self.conn.send(api_key=self.key, secret=self.secret, auth=True)

    @is_connected
    def new_order(self, **order_settings):
        """Post a new Order via Websocket.
        :param kwargs:
        :return:
        """
        self._send_auth_command('on', order_settings)

    @is_connected
    def cancel_order(self, multi=False, **order_identifiers):
        """Cancel one or multiple orders via Websocket.
        :param multi: bool, whether order_settings contains settings for one, or
                      multiples orders
        :param order_identifiers: Identifiers for the order(s) you with to cancel
        :return:
        """
        if multi:
            self._send_auth_command('oc_multi', order_identifiers)
        else:
            self._send_auth_command('oc', order_identifiers)

    @is_connected
    def order_multi_op(self, *operations):
        """Execute multiple, order-related operations via Websocket.
        :param operations: operations to send to the websocket
        :return:
        """
        self._send_auth_command('ox_multi', operations)

    @is_connected
    def calc(self, *calculations):
        """Request one or several operations via Websocket.
        :param calculations: calculations as strings to send to the websocket
        :return:
        """
        self._send_auth_command('calc', calculations)

    def _send_auth_command(self, channel_name, data):
        payload = [0, channel_name, None, data]
        self.conn.send(list_data=payload)				
				
