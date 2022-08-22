from os import environ
from orjson import loads
from aiohttp import ClientSession

import google.auth.transport.requests
import google.oauth2.id_token


class TickerParser(object):
	endpoint = "http://parser:6900/" if environ['PRODUCTION'] else "http://parser:6900/"

	async def process_task(service, data, retries=3):
		authReq = google.auth.transport.requests.Request()
		token = google.oauth2.id_token.fetch_id_token(authReq, TickerParser.endpoint)
		headers = {
			"Authorization": "Bearer " + token,
			"content-type": "application/json",
			"accept": "application/json"
		}

		async with ClientSession(headers=headers) as session:
			async with session.post(TickerParser.endpoint + service, json=data) as response:
				if response.status == 200:
					return await response.json()

		if retries == 1: raise Exception("time out")
		else: return await TickerParser.process_task(service, data, retries=retries-1)

	@staticmethod
	async def find_exchange(raw, platform, bias):
		payload = await TickerParser.process_task("parser/find_exchange", {"raw": raw, "platform": platform, "bias": bias})
		return payload.get("success"), payload.get("match")

	@staticmethod
	async def match_ticker(tickerId, exchange, platform, bias):
		exchangeId = exchange.get("id").lower() if bool(exchange) else None
		payload = await TickerParser.process_task("parser/match_ticker", {"tickerId": tickerId, "exchangeId": exchangeId, "platform": platform, "bias": bias})
		return payload.get("response"), payload.get("message")

	@staticmethod
	async def check_if_fiat(tickerId):
		payload = await TickerParser.process_task("parser/check_if_fiat", {"tickerId": tickerId})
		return payload.get("isFiat"), payload.get("asset")

	@staticmethod
	async def get_listings(tickerBase, tickerQuote):
		payload = await TickerParser.process_task("parser/get_listings", {"tickerBase": tickerBase, "tickerQuote": tickerQuote})
		return payload.get("response"), payload.get("total")

	@staticmethod
	async def get_formatted_price_ccxt(exchangeId, symbol, price):
		payload = await TickerParser.process_task("parser/get_formatted_price_ccxt", {"exchangeId": exchangeId, "symbol": symbol, "price": price})
		return payload.get("response")

	@staticmethod
	async def get_formatted_amount_ccxt(exchangeId, symbol, amount):
		payload = await TickerParser.process_task("parser/get_formatted_amount_ccxt", {"exchangeId": exchangeId, "symbol": symbol, "amount": amount})
		return payload.get("response")

	@staticmethod
	async def get_venues(platforms):
		payload = await TickerParser.process_task("parser/get_venues", {"platforms": platforms})
		return payload.get("response")