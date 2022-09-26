from .core import process_task

async def find_exchange(raw, platform):
	payload = await process_task(
		{
			"raw": raw,
			"platform": platform
		},
		"parser",
		endpoint="/find_exchange"
	)
	return payload.get("success"), payload.get("match")

async def match_ticker(tickerId, exchange, platform):
	exchangeId = exchange.get("id").lower() if bool(exchange) else None
	payload = await process_task(
		{
			"tickerId": tickerId,
			"exchangeId": exchangeId,
			"platform": platform
		},
		"parser",
		endpoint="/match_ticker"
	)
	return payload.get("response"), payload.get("message")

async def get_listings(ticker, currentPlatform):
	payload = await process_task(
		{
			"ticker": ticker,
			"platform": currentPlatform
		},
		"parser",
		endpoint="/get_listings"
	)
	return payload.get("response"), payload.get("total")

async def get_formatted_price_ccxt(exchangeId, symbol, price):
	payload = await process_task(
		{
			"exchangeId": exchangeId,
			"symbol": symbol,
			"price": price
		},
		"parser",
		endpoint="/get_formatted_price_ccxt"
	)
	return payload.get("response")

async def get_formatted_amount_ccxt(exchangeId, symbol, amount):
	payload = await process_task(
		{
			"exchangeId": exchangeId,
			"symbol": symbol,
			"amount": amount
		},
		"parser",
		endpoint="/get_formatted_amount_ccxt"
	)
	return payload.get("response")