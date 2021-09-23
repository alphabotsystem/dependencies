from os import environ
from zmq import Context, Poller, REQ, LINGER, POLLIN
from orjson import loads
from io import BytesIO


class TickerParser(object):
	zmqContext = Context.instance()

	@staticmethod
	def execute_parser_request(endpoint, parameters, timeout=5):
		socket = TickerParser.zmqContext.socket(REQ)
		payload, responseText = None, None
		socket.connect("tcp://parser:6900")
		socket.setsockopt(LINGER, 0)
		poller = Poller()
		poller.register(socket, POLLIN)

		socket.send_multipart([endpoint] + parameters)
		responses = poller.poll(timeout * 1000)

		if len(responses) != 0:
			response = socket.recv_multipart()
			socket.close()
			return response
		else:
			socket.close()
			raise Exception("time out")
		return None

	@staticmethod
	def find_exchange(raw, platform, bias):
		[success, exchange] = TickerParser.execute_parser_request(b"find_exchange", [raw.encode(), platform.encode(), bias.encode()])
		exchange = None if exchange == b"" else loads(exchange)
		return bool(int(success)), exchange

	@staticmethod
	def match_ticker(tickerId, exchange, platform, bias):
		exchangeId = exchange.get("id").lower() if bool(exchange) else ""
		[ticker, error] = TickerParser.execute_parser_request(b"match_ticker", [tickerId.encode(), exchangeId.encode(), platform.encode(), bias.encode()])
		ticker = None if ticker == b"" else loads(ticker)
		error = None if error == b"" else error.decode()
		return ticker, error

	@staticmethod
	def check_if_fiat(tickerId):
		[success, fiat] = TickerParser.execute_parser_request(b"check_if_fiat", [tickerId.encode()])
		return bool(int(success)), fiat

	@staticmethod
	def get_listings(tickerBase, tickerQuote):
		[listings, total] = TickerParser.execute_parser_request(b"get_listings", [tickerBase.encode(), tickerQuote.encode()])
		return loads(listings), int(total)

	@staticmethod
	def get_formatted_price_ccxt(exchangeId, symbol, price):
		[response] = TickerParser.execute_parser_request(b"get_formatted_price_ccxt", [exchangeId.encode(), symbol.encode(), str(price).encode()])
		return response.decode()

	@staticmethod
	def get_formatted_amount_ccxt(exchangeId, symbol, amount):
		[response] = TickerParser.execute_parser_request(b"get_formatted_amount_ccxt", [exchangeId.encode(), symbol.encode(), str(amount).encode()])
		return response.decode()
