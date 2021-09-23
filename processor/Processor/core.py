from os import environ
from time import time
from base64 import decodebytes
from zmq.asyncio import Context, Poller
from zmq import REQ, DEALER, LINGER, POLLIN
from orjson import dumps, loads
from io import BytesIO

from DataRequest import ChartRequestHandler
from DataRequest import HeatmapRequestHandler
from DataRequest import PriceRequestHandler
from DataRequest import DetailRequestHandler
from DataRequest import TradeRequestHandler


class Processor(object):
	clientId = b"public"
	services = {
		"candle": "tcp://candle-server:6900",
		"chart": "tcp://image-server:6900",
		"depth": "tcp://quote-server:6900",
		"detail": "tcp://detail-server:6900",
		"heatmap": "tcp://image-server:6900",
		"quote": "tcp://quote-server:6900",
		"ichibot": "tcp://ichibot-server:6900"
	}
	zmqContext = Context.instance()

	@staticmethod
	async def process_request(service, authorId, request, timeout=60, retries=3):
		socket = Processor.zmqContext.socket(REQ)
		payload, responseText = None, None
		socket.connect(Processor.services[service])
		socket.setsockopt(LINGER, 0)
		poller = Poller()
		poller.register(socket, POLLIN)

		request["timestamp"] = time()
		request["authorId"] = authorId
		await socket.send_multipart([Processor.clientId, service.encode(), dumps(request)])
		responses = await poller.poll(timeout * 1000)

		if len(responses) != 0:
			payload, responseText = await socket.recv_multipart()
			socket.close()
			payload = loads(payload)
			payload = payload if bool(payload) else None
			responseText = None if responseText == b"" else responseText.decode()
			if service in ["chart", "heatmap", "depth"] and payload is not None:
				payload["data"] = BytesIO(decodebytes(payload["data"].encode()))
		else:
			socket.close()
			if retries == 1: raise Exception("time out")
			else: payload, responseText = await Processor.process_request(service, authorId, request, retries=retries-1)

		return payload, responseText

	@staticmethod
	async def process_chart_arguments(messageRequest, arguments, tickerId=None, platform=None, platformQueue=None, **kwargs):
		if isinstance(tickerId, str): tickerId = tickerId[:25]
		if platform is not None: platformQueue = [platform]
		elif platformQueue is None: platformQueue = messageRequest.get_platform_order_for("charts")

		for p in kwargs.get("excluded", []):
			if p in platformQueue:
				platformQueue.remove(p)

		requestHandler = ChartRequestHandler(tickerId, platformQueue, bias=messageRequest.marketBias, **kwargs)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		outputMessage = requestHandler.get_preferred_platform()

		return outputMessage, requestHandler.to_dict()

	@staticmethod
	async def process_heatmap_arguments(messageRequest, arguments, platform=None, platformQueue=None, **kwargs):
		if platform is not None: platformQueue = [platform]
		elif platformQueue is None: platformQueue = messageRequest.get_platform_order_for("heatmaps")

		for p in kwargs.get("excluded", []):
			if p in platformQueue:
				platformQueue.remove(p)

		requestHandler = HeatmapRequestHandler(platformQueue, bias=messageRequest.marketBias, **kwargs)
		for argument in arguments:
			await requestHandler.parse_argument(argument)

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		outputMessage = requestHandler.get_preferred_platform()

		return outputMessage, requestHandler.to_dict()
	
	@staticmethod
	async def process_quote_arguments(messageRequest, arguments, tickerId=None, platform=None, platformQueue=None, **kwargs):
		if isinstance(tickerId, str): tickerId = tickerId[:25]
		if platform is not None: platformQueue = [platform]
		elif platformQueue is None: platformQueue = messageRequest.get_platform_order_for("quotes")

		for p in kwargs.get("excluded", []):
			if p in platformQueue:
				platformQueue.remove(p)

		requestHandler = PriceRequestHandler(tickerId, platformQueue, bias=messageRequest.marketBias, **kwargs)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		outputMessage = requestHandler.get_preferred_platform()

		return outputMessage, requestHandler.to_dict()

	@staticmethod
	async def process_detail_arguments(messageRequest, arguments, tickerId=None, platform=None, platformQueue=None, **kwargs):
		if isinstance(tickerId, str): tickerId = tickerId[:25]
		if platform is not None: platformQueue = [platform]
		elif platformQueue is None: platformQueue = messageRequest.get_platform_order_for("details")

		for p in kwargs.get("excluded", []):
			if p in platformQueue:
				platformQueue.remove(p)

		requestHandler = DetailRequestHandler(tickerId, platformQueue, bias=messageRequest.marketBias, **kwargs)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		outputMessage = requestHandler.get_preferred_platform()

		return outputMessage, requestHandler.to_dict()

	@staticmethod
	async def process_trade_arguments(messageRequest, arguments, tickerId=None, platform=None, platformQueue=None, **kwargs):
		if isinstance(tickerId, str): tickerId = tickerId[:25]
		if platform is not None: platformQueue = [platform]
		elif platformQueue is None: platformQueue = messageRequest.get_platform_order_for("trades")

		for p in kwargs.get("excluded", []):
			if p in platformQueue:
				platformQueue.remove(p)

		requestHandler = TradeRequestHandler(tickerId, platformQueue, bias=messageRequest.marketBias, **kwargs)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		outputMessage = requestHandler.get_preferred_platform()

		return outputMessage, requestHandler.to_dict()

	@staticmethod
	async def process_conversion(messageRequest, fromBase, toBase, amount):
		try: amount = float(amount)
		except: return None, "Provided amount is not a number."
		if amount > 1000000000000000000000: return None, "Sir?"

		if fromBase == toBase: return None, "Converting into the same unit is trivial."

		payload1 = {"raw": {"quotePrice": [1]}}
		payload2 = {"raw": {"quotePrice": [1]}}

		if fromBase not in ["USD", "USDT", "USDC", "DAI", "HUSD", "TUSD", "PAX", "USDK", "USDN", "BUSD", "GUSD", "USDS"]:
			outputMessage, request = await Processor.process_quote_arguments(messageRequest, [], tickerId=fromBase + "USD", excluded=["CCXT", "Serum", "LLD"])
			if outputMessage is not None: return None, outputMessage
			payload1, quoteText = await Processor.process_request("quote", messageRequest.authorId, request)
			if payload1 is None: return None, quoteText
			fromBase = request.get(payload1.get("platform")).get("ticker").get("id")
		else:
			fromBase = "USD"
		if toBase not in ["USD", "USDT", "USDC", "DAI", "HUSD", "TUSD", "PAX", "USDK", "USDN", "BUSD", "GUSD", "USDS"]:
			outputMessage, request = await Processor.process_quote_arguments(messageRequest, [], tickerId="USD" + toBase, excluded=["CCXT", "Serum", "LLD"])
			if outputMessage is not None: return None, outputMessage
			payload2, quoteText = await Processor.process_request("quote", messageRequest.authorId, request)
			if payload2 is None: return None, quoteText
			toBase = request.get(payload2.get("platform")).get("ticker").get("id")
		else:
			toBase = "USD"

		convertedValue = payload1["raw"]["quotePrice"][0] * amount * payload2["raw"]["quotePrice"][0]
		if convertedValue > 1000000000000000000000: return None, "Sir?"

		payload = {
			"quotePrice": "{:,.3f} {}".format(amount, fromBase),
			"quoteConvertedPrice": "{:,.6f} {}".format(convertedValue, toBase),
			"messageColor":"deep purple",
			"sourceText": "Alpha Currency Conversions",
			"platform": "Alpha Currency Conversions",
			"raw": {
				"quotePrice": [convertedValue],
				"ticker": toBase,
				"timestamp": time()
			}
		}
		return payload, None

	@staticmethod
	def get_direct_ichibot_socket(identity):
		socket = Processor.zmqContext.socket(DEALER)
		socket.identity = identity.encode("ascii")
		socket.connect(Processor.services["ichibot"])
		socket.setsockopt(LINGER, 0)
		return socket