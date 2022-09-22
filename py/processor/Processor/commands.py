from .core import process_task


async def process_chart_arguments(commandRequest, arguments, platforms, tickerId=None):
	payload = await process_task(
		{
			"bias": commandRequest.marketBias,
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": tickerId
		},
		"parser",
		endpoint="/chart"
	)
	return payload.get("message"), payload.get("response")

async def process_heatmap_arguments(commandRequest, arguments, platforms):
	payload = await process_task(
		{
			"bias": commandRequest.marketBias,
			"arguments": arguments,
			"platforms": platforms
		},
		"parser",
		endpoint="/heatmap"
	)
	return payload.get("message"), payload.get("response")

async def process_quote_arguments(commandRequest, arguments, platforms, tickerId=None):
	payload = await process_task(
		{
			"bias": commandRequest.marketBias,
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": tickerId
		},
		"parser",
		endpoint="/quote"
	)
	return payload.get("message"), payload.get("response")

async def process_detail_arguments(commandRequest, arguments, platforms, tickerId=None):
	payload = await process_task(
		{
			"bias": commandRequest.marketBias,
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": tickerId
		},
		"parser",
		endpoint="/detail"
	)
	return payload.get("message"), payload.get("response")

async def process_trade_arguments(commandRequest, arguments, platforms, tickerId=None):
	payload = await process_task(
		{
			"bias": commandRequest.marketBias,
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": tickerId
		},
		"parser",
		endpoint="/trade"
	)
	return payload.get("message"), payload.get("response")