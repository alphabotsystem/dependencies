from time import time
from asyncio import gather
from zmq.asyncio import Context
from zmq import DEALER, LINGER

from .core import process_task
from .commands import process_quote_arguments

context = Context.instance()


async def process_conversion(commandRequest, fromBase, toBase, amount, platforms, acceptable=["USD"]):
	if amount <= 0 or amount >= 1000000000000000: return None, "Sir?"

	if fromBase == toBase: return None, "Converting into the same asset is trivial."

	payload1 = {"raw": {"quotePrice": [1]}}
	payload2 = {"raw": {"quotePrice": [1]}}
	fromQuote, toQuote = "USD", "USD"
	fromTicker, toTicker = "US Dollar", "US Dollar"
	adjustment = 1

	tasks, results = [], None

	# Parse arguments
	if fromBase not in acceptable:
		tasks.append(process_quote_arguments([], platforms, tickerId=fromBase))
	if toBase not in acceptable:
		tasks.append(process_quote_arguments([], platforms, tickerId=toBase))

	if len(tasks) > 0:
		results = await gather(*tasks)

	tasks, requests = [], []

	# Conversion calculation
	if fromBase not in acceptable:
		responseMessage, request = results.pop(0)
		if responseMessage is not None: return None, "Value in `from` failed to parse. " + responseMessage
		tasks.append(process_task(request, "quote"))
		requests.append(request)
	if toBase not in acceptable:
		responseMessage, request = results.pop(0)
		if responseMessage is not None: return None, "Value in `to` failed to parse. " + responseMessage
		tasks.append(process_task(request, "quote"))
		requests.append(request)

	if len(tasks) > 0:
		results = await gather(*tasks)

	if fromBase not in acceptable:
		request = requests.pop(0)
		payload1, responseMessage = results.pop(0)
		if payload1 is None: return None, responseMessage
		fromBase = request.get(payload1.get("platform")).get("ticker").get("base")
		fromQuote = request.get(payload1.get("platform")).get("ticker").get("quote")
		fromTicker = request.get(payload1.get("platform")).get("ticker").get("name")
	if toBase not in acceptable:
		request = requests.pop(0)
		payload2, responseMessage = results.pop(0)
		if payload2 is None: return None, responseMessage
		toBase = request.get(payload2.get("platform")).get("ticker").get("base")
		toQuote = request.get(payload2.get("platform")).get("ticker").get("quote")
		toTicker = request.get(payload2.get("platform")).get("ticker").get("name")

	if fromQuote != toQuote and fromQuote not in acceptable and toQuote not in acceptable:
		relaySymbol = toQuote + fromQuote if fromQuote in acceptable else fromQuote + toQuote
		responseMessage, request = await process_quote_arguments([], platforms, tickerId=relaySymbol)
		if responseMessage is not None: return None, responseMessage
		payload, responseMessage = await process_task(request, "quote")
		if payload is None: return None, responseMessage
		adjustment = 1 / payload["raw"]["quotePrice"][0] if fromQuote in acceptable else payload["raw"]["quotePrice"][0]

	convertedValue = payload1["raw"]["quotePrice"][0] * amount / (payload2["raw"]["quotePrice"][0] * adjustment)
	if convertedValue > 1000000000000000: return None, "Sir?"

	return {
		"quotePrice": "{:,.8f}".format(amount).rstrip('0').rstrip('.') + " " + fromBase,
		"quoteVolume": f"Converting from {fromTicker}",
		"quoteConvertedPrice": "{:,.8f}".format(convertedValue).rstrip('0').rstrip('.') + " " + toBase,
		"quoteConvertedVolume": f"to {toTicker}",
		"messageColor":"deep purple",
		"sourceText": "Alpha.bot Conversions",
		"platform": "Alpha.bot Conversions",
		"raw": {
			"quotePrice": [convertedValue],
			"ticker": toBase,
			"timestamp": time()
		}
	}, None

def get_direct_ichibot_socket(identity):
	socket = context.socket(DEALER)
	socket.identity = identity.encode("ascii")
	socket.connect("tcp://ichibot-server:6900")
	socket.setsockopt(LINGER, 0)
	return socket