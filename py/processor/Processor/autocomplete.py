from .core import process_task


async def autocomplete_timeframe(cls, ctx):
	payload = await process_task(
		{
			"option": "timeframe",
			"timeframe": " ".join(ctx.options.get("timeframe", "").lower().split()),
			"type": " ".join(ctx.options.get("type", "").lower().split())
		},
		"parser",
		endpoint="/autocomplete"
	)
	return payload.get("response")

async def autocomplete_market(cls, ctx):
	payload = await process_task(
		{
			"option": "market",
			"market": " ".join(ctx.options.get("market", "").lower().split()),
			"type": " ".join(ctx.options.get("type", "").lower().split())
		},
		"parser",
		endpoint="/autocomplete"
	)
	return payload.get("response")

async def autocomplete_category(cls, ctx):
	payload = await process_task(
		{
			"option": "category",
			"category": " ".join(ctx.options.get("category", "").lower().split()),
			"type": " ".join(ctx.options.get("type", "").lower().split())
		},
		"parser",
		endpoint="/autocomplete"
	)
	return payload.get("response")

async def autocomplete_color(cls, ctx):
	payload = await process_task(
		{
			"option": "color",
			"color": " ".join(ctx.options.get("color", "").lower().split()),
			"type": " ".join(ctx.options.get("type", "").lower().split())
		},
		"parser",
		endpoint="/autocomplete"
	)
	return payload.get("response")

async def autocomplete_size(cls, ctx):
	payload = await process_task(
		{
			"option": "size",
			"size": " ".join(ctx.options.get("size", "").lower().split()),
			"type": " ".join(ctx.options.get("type", "").lower().split())
		},
		"parser",
		endpoint="/autocomplete"
	)
	return payload.get("response")

async def autocomplete_group(cls, ctx):
	payload = await process_task(
		{
			"option": "group",
			"group": " ".join(ctx.options.get("group", "").lower().split()),
			"type": " ".join(ctx.options.get("type", "").lower().split())
		},
		"parser",
		endpoint="/autocomplete"
	)
	return payload.get("response")