from os import environ
from zmq.asyncio import Context, Poller
from zmq import REQ, LINGER, POLLIN
from orjson import loads
from io import BytesIO


class TickerParser(object):
	zmqContext = Context.instance()

	@staticmethod
	async def execute_parser_request(endpoint, parameters, timeout=5):
		socket = TickerParser.zmqContext.socket(REQ)
		socket.connect("tcp://parser:6900")
		socket.setsockopt(LINGER, 0)
		poller = Poller()
		poller.register(socket, POLLIN)

		await socket.send_multipart([endpoint] + parameters)
		responses = await poller.poll(timeout * 1000)

		if len(responses) != 0:
			response = await socket.recv_multipart()
			socket.close()
			return response
		else:
			socket.close()
			raise Exception("time out")
		return None

	@staticmethod
	async def find_exchange(raw, platform, bias):
		[success, exchange] = await TickerParser.execute_parser_request(b"find_exchange", [raw.encode(), platform.encode(), bias.encode()])
		exchange = None if exchange == b"" else loads(exchange)
		return bool(int(success)), exchange

	@staticmethod
	async def match_ticker(tickerId, exchange, platform, bias):
		exchangeId = exchange.get("id").lower() if bool(exchange) else ""
		[ticker, error] = await TickerParser.execute_parser_request(b"match_ticker", [tickerId.encode(), exchangeId.encode(), platform.encode(), bias.encode()])
		ticker = None if ticker == b"" else loads(ticker)
		error = None if error == b"" else error.decode()
		return ticker, error

	@staticmethod
	async def check_if_fiat(tickerId):
		[success, fiat] = await TickerParser.execute_parser_request(b"check_if_fiat", [tickerId.encode()])
		fiat = None if fiat == b"" else fiat.decode()
		return bool(int(success)), fiat

	@staticmethod
	async def get_listings(tickerBase, tickerQuote):
		[listings, total] = await TickerParser.execute_parser_request(b"get_listings", [tickerBase.encode(), tickerQuote.encode()])
		return loads(listings), int(total)

	@staticmethod
	async def get_formatted_price_ccxt(exchangeId, symbol, price):
		[response] = await TickerParser.execute_parser_request(b"get_formatted_price_ccxt", [exchangeId.encode(), symbol.encode(), str(price).encode()])
		return response.decode()

	@staticmethod
	async def get_formatted_amount_ccxt(exchangeId, symbol, amount):
		[response] = await TickerParser.execute_parser_request(b"get_formatted_amount_ccxt", [exchangeId.encode(), symbol.encode(), str(amount).encode()])
		return response.decode()
