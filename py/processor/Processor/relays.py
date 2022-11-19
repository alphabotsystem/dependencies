from time import time
from zmq.asyncio import Context
from zmq import DEALER, LINGER

from .core import process_task
from .commands import process_quote_arguments

context = Context.instance()


async def process_conversion(commandRequest, fromBase, toBase, amount, platforms):
	if amount <= 0 or amount >= 1000000000000000: return None, "Sir?"

	if fromBase == toBase: return None, "Converting into the same asset is trivial."

	payload1 = {"raw": {"quotePrice": [1]}}
	payload2 = {"raw": {"quotePrice": [1]}}
	fromQuote, toQuote = "USD", "USD"
	adjustment = 1

	if "|" not in fromBase and "|" not in toBase:
		# Check if a direct pair exists
		responseMessage, request = await process_quote_arguments([], platforms, tickerId=fromBase + toBase)
		if responseMessage is None:
			payload, _ = await process_task(request, "quote")
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
	if fromBase != "USD":
		responseMessage, request = await process_quote_arguments([], platforms, tickerId=fromBase)
		if responseMessage is not None: return None, responseMessage

		payload1, responseMessage = await process_task(request, "quote")
		if payload1 is None: return None, responseMessage
		fromBase = request.get(payload1.get("platform")).get("ticker").get("base")
		fromQuote = request.get(payload1.get("platform")).get("ticker").get("quote")

	if toBase != "USD":
		responseMessage, request = await process_quote_arguments([], platforms, tickerId=toBase)
		if responseMessage is not None: return None, responseMessage

		payload2, responseMessage = await process_task(request, "quote")
		if payload2 is None: return None, responseMessage
		toBase = request.get(payload2.get("platform")).get("ticker").get("base")
		toQuote = request.get(payload2.get("platform")).get("ticker").get("quote")

	if fromQuote != toQuote:
		relaySymbol = toQuote + fromQuote if fromQuote == "USD" else fromQuote + toQuote
		responseMessage, request = await process_quote_arguments([], platforms, tickerId=relaySymbol)
		if responseMessage is not None: return None, responseMessage

		payload, responseMessage = await process_task(request, "quote")
		if payload is None: return None, responseMessage
		adjustment = 1 / payload["raw"]["quotePrice"][0] if fromQuote == "USD" else payload["raw"]["quotePrice"][0]

	convertedValue = payload1["raw"]["quotePrice"][0] * amount / payload2["raw"]["quotePrice"][0] * adjustment
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

def get_direct_ichibot_socket(identity):
	socket = context.socket(DEALER)
	socket.identity = identity.encode("ascii")
	socket.connect("tcp://ichibot-server:6900")
	socket.setsockopt(LINGER, 0)
	return socket