from .core import process_task


async def process_chart_arguments(arguments, platforms, tickerId=None, defaults={}):
	payload = await process_task(
		{
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": tickerId,
			"defaults": defaults
		},
		"parser",
		endpoint="/chart"
	)
	return payload.get("message"), payload.get("response")

async def process_heatmap_arguments(arguments, platforms):
	payload = await process_task(
		{
			"arguments": arguments,
			"platforms": platforms
		},
		"parser",
		endpoint="/heatmap"
	)
	return payload.get("message"), payload.get("response")

async def process_quote_arguments(arguments, platforms, tickerId=None):
	payload = await process_task(
		{
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": tickerId
		},
		"parser",
		endpoint="/quote"
	)
	return payload.get("message"), payload.get("response")

async def process_detail_arguments(arguments, platforms, tickerId=None):
	payload = await process_task(
		{
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": tickerId
		},
		"parser",
		endpoint="/detail"
	)
	return payload.get("message"), payload.get("response")