from os import environ
from time import time
from base64 import decodebytes
from aiohttp import ClientSession
from zmq.asyncio import Context, Poller
from zmq import DEALER, LINGER
from io import BytesIO

import google.auth.transport.requests
import google.oauth2.id_token

from DataRequest import ChartRequestHandler
from DataRequest import HeatmapRequestHandler
from DataRequest import PriceRequestHandler
from DataRequest import DetailRequestHandler
from DataRequest import TradeRequestHandler


class Processor(object):
	zmqContext = Context.instance()
	endpoints = {
		"candle": "http://candle-server:6900/" if environ['PRODUCTION'] else "http://candle-server:6900/",
		"chart": "https://image-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://image-server:6900/",
		"depth": "https://quote-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://quote-server:6900/",
		"detail": "https://quote-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://quote-server:6900/",
		"heatmap": "https://image-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://image-server:6900/",
		"quote": "https://quote-server-yzrdox65bq-uc.a.run.app/" if environ['PRODUCTION'] else "http://quote-server:6900/",
	}

	async def process_task(service, authorId, request, retries=3):
		url = Processor.endpoints[service]
		authReq = google.auth.transport.requests.Request()
		token = google.oauth2.id_token.fetch_id_token(authReq, url)
		headers = {
			"Authorization": "Bearer " + token,
			"content-type": "application/json",
			"accept": "application/json"
		}

		request["timestamp"] = time()
		request["authorId"] = authorId
		async with ClientSession(headers=headers) as session:
			async with session.post(url + service, json=request) as response:
				if response.status == 200:
					data = await response.json()
					payload, message = data.get("response"), data.get("message")
					if service in ["chart", "heatmap", "depth"] and payload is not None and payload["data"] is not None:
						payload["data"] = BytesIO(decodebytes(payload["data"].encode()))
					return payload, message

		if retries == 1: raise Exception("time out")
		else: return await Processor.process_task(service, authorId, request, retries=retries-1)

	@staticmethod
	async def process_chart_arguments(commandRequest, arguments, platforms, tickerId=None):
		requestHandler = ChartRequestHandler(tickerId, platforms.copy(), bias=commandRequest.marketBias)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		responseMessage = requestHandler.get_preferred_platform()

		return responseMessage, requestHandler.to_dict()

	@staticmethod
	async def process_heatmap_arguments(commandRequest, arguments, platforms):
		requestHandler = HeatmapRequestHandler(platforms.copy(), bias=commandRequest.marketBias)
		for argument in arguments:
			await requestHandler.parse_argument(argument)

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		responseMessage = requestHandler.get_preferred_platform()

		return responseMessage, requestHandler.to_dict()
	
	@staticmethod
	async def process_quote_arguments(commandRequest, arguments, platforms, tickerId=None):
		requestHandler = PriceRequestHandler(tickerId, platforms.copy(), bias=commandRequest.marketBias)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		responseMessage = requestHandler.get_preferred_platform()

		return responseMessage, requestHandler.to_dict()

	@staticmethod
	async def process_detail_arguments(commandRequest, arguments, platforms, tickerId=None):
		requestHandler = DetailRequestHandler(tickerId, platforms.copy(), bias=commandRequest.marketBias)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		responseMessage = requestHandler.get_preferred_platform()

		return responseMessage, requestHandler.to_dict()

	@staticmethod
	async def process_trade_arguments(commandRequest, arguments, platforms, tickerId=None):
		requestHandler = TradeRequestHandler(tickerId, platforms.copy(), bias=commandRequest.marketBias)
		for argument in arguments:
			await requestHandler.parse_argument(argument)
		if tickerId is not None:
			await requestHandler.process_ticker()

		requestHandler.set_defaults()
		await requestHandler.find_caveats()
		responseMessage = requestHandler.get_preferred_platform()

		return responseMessage, requestHandler.to_dict()

	@staticmethod
	async def process_conversion(commandRequest, fromBase, toBase, amount, platforms):
		if amount <= 0 or amount >= 1000000000000000: return None, "Sir?"

		if fromBase == toBase: return None, "Converting into the same asset is trivial."

		payload1 = {"raw": {"quotePrice": [1]}}
		payload2 = {"raw": {"quotePrice": [1]}}

		# Check if a direct pair exists
		responseMessage, request = await Processor.process_quote_arguments(commandRequest, [], platforms, tickerId=fromBase + toBase)
		if responseMessage is None:
			payload, _ = await Processor.process_task("quote", commandRequest.authorId, request)
			if payload is not None: return {
				"quotePrice": "{:,.8f}".format(amount).rstrip('0').rstrip('.') + " " + fromBase,
				"quoteConvertedPrice": "{:,.8f}".format(payload["raw"]["quotePrice"][0] * amount).rstrip('0').rstrip('.') + " " + toBase,
				"messageColor":"deep purple",
				"sourceText": "Alpha Currency Conversions",
				"platform": "Alpha Currency Conversions",
				"raw": {
					"quotePrice": [payload["raw"]["quotePrice"][0] * amount],
					"ticker": toBase,
					"timestamp": time()
				}
			}, None

		# Indirect calculation
		responseMessage, request = await Processor.process_quote_arguments(commandRequest, [], platforms, tickerId=fromBase)
		if responseMessage is not None: return None, responseMessage
		payload1, responseMessage = await Processor.process_task("quote", commandRequest.authorId, request)
		if payload1 is None: return None, responseMessage
		fromBase = request.get(payload1.get("platform")).get("ticker").get("base")

		responseMessage, request = await Processor.process_quote_arguments(commandRequest, [], platforms, tickerId=toBase)
		if responseMessage is not None: return None, responseMessage
		payload2, responseMessage = await Processor.process_task("quote", commandRequest.authorId, request)
		if payload2 is None: return None, responseMessage
		toBase = request.get(payload2.get("platform")).get("ticker").get("base")

		convertedValue = payload1["raw"]["quotePrice"][0] * amount / payload2["raw"]["quotePrice"][0]
		if convertedValue > 1000000000000000: return None, "Sir?"

		return {
			"quotePrice": "{:,.8f}".format(amount).rstrip('0').rstrip('.') + " " + fromBase,
			"quoteConvertedPrice": "{:,.8f}".format(convertedValue).rstrip('0').rstrip('.') + " " + toBase,
			"messageColor":"deep purple",
			"sourceText": "Alpha Currency Conversions",
			"platform": "Alpha Currency Conversions",
			"raw": {
				"quotePrice": [convertedValue],
				"ticker": toBase,
				"timestamp": time()
			}
		}, None

	@staticmethod
	def get_direct_ichibot_socket(identity):
		socket = Processor.zmqContext.socket(DEALER)
		socket.identity = identity.encode("ascii")
		socket.connect("tcp://ichibot-server:6900")
		socket.setsockopt(LINGER, 0)
		return socket