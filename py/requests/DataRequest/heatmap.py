from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from TickerParser import TickerParser
from .parameter import HeatmapParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1, "1m", ["1", "1m", "1min", "1mins", "1minute", "1minutes", "min"]),
		Parameter(2, "2m", ["2", "2m", "2min", "2mins", "2minute", "2minutes"]),
		Parameter(3, "3m", ["3", "3m", "3min", "3mins", "3minute", "3minutes"]),
		Parameter(5, "5m", ["5", "5m", "5min", "5mins", "5minute", "5minutes"]),
		Parameter(10, "10m", ["10", "10m", "10min", "10mins", "10minute", "10minutes"]),
		Parameter(15, "15m", ["15", "15m", "15min", "15mins", "15minute", "15minutes"], bitgur="last_minute15/"),
		Parameter(20, "20m", ["20", "20m", "20min", "20mins", "20minute", "20minutes"]),
		Parameter(30, "30m", ["30", "30m", "30min", "30mins", "30minute", "30minutes"]),
		Parameter(45, "45m", ["45", "45m", "45min", "45mins", "45minute", "45minutes"]),
		Parameter(60, "1H", ["60", "60m", "60min", "60mins", "60minute", "60minutes", "1", "1h", "1hr", "1hour", "1hours", "hourly", "hour", "hr", "h"], bitgur="last_hour/"),
		Parameter(120, "2H", ["120", "120m", "120min", "120mins", "120minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2hours"]),
		Parameter(180, "3H", ["180", "180m", "180min", "180mins", "180minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3hours"]),
		Parameter(240, "4H", ["240", "240m", "240min", "240mins", "240minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4hours"]),
		Parameter(360, "6H", ["360", "360m", "360min", "360mins", "360minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6hours"]),
		Parameter(480, "8H", ["480", "480m", "480min", "480mins", "480minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8hours"]),
		Parameter(720, "12H", ["720", "720m", "720min", "720mins", "720minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12hours"]),
		Parameter(1440, "1D", ["24", "24h", "24hr", "24hrs", "24hour", "24hours", "d", "day", "1", "1d", "1day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440minutes"], finviz="", bitgur="last_day/"),
		Parameter(2880, "2D", ["48", "48h", "48hr", "48hrs", "48hour", "48hours", "2", "2d", "2day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880minutes"]),
		Parameter(3420, "3D", ["72", "72h", "72hr", "72hrs", "72hour", "72hours", "3", "3d", "3day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420minutes"]),
		Parameter(10080, "1W", ["7", "7d", "7day", "7days", "w", "week", "1w", "1week", "weekly"], finviz="&st=w1", bitgur="last_week/"),
		Parameter(20160, "2W", ["14", "14d", "14day", "14days", "2w", "2week"]),
		Parameter(43829, "1M", ["30d", "30day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "monthly"], finviz="&st=w4", bitgur="last_month/"),
		Parameter(87658, "2M", ["2", "2m", "2m", "2mo", "2month", "2months"]),
		Parameter(131487, "3M", ["3", "3m", "3m", "3mo", "3month", "3months"], finviz="&st=w13", bitgur="last_month3/"),
		Parameter(175316, "4M", ["4", "4m", "4m", "4mo", "4month", "4months"]),
		Parameter(262974, "6M", ["6", "6m", "5m", "6mo", "6month", "6months"], finviz="&st=w26", bitgur="last_month6/"),
		Parameter(525949, "1Y", ["12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1y", "y", "annual", "annually"], finviz="&st=w52", bitgur="last_year/"),
		Parameter(1051898, "2Y", ["24", "24m", "24mo", "24month", "24months", "2year", "2y"]),
		Parameter(1577847, "3Y", ["36", "36m", "36mo", "36month", "36months", "3year", "3y"]),
		Parameter(2103796, "4Y", ["48", "48m", "48mo", "48month", "48months", "4year", "4y"])
	],
	"types": [
		Parameter("lookback", "year to date performance", ["ytd"], finviz="&st=ytd"),
		Parameter("lookback", "relative volume", ["relative", "volume", "relvol", "rvol"], finviz="&st=relvol"),
		Parameter("lookback", "P/E", ["pe"], finviz="&st=pe"),
		Parameter("lookback", "forward P/E", ["fpe"], finviz="&st=fpe"),
		Parameter("lookback", "PEG", ["peg"], finviz="&st=peg"),
		Parameter("lookback", "P/S", ["ps"], finviz="&st=ps"),
		Parameter("lookback", "P/B", ["pb"], finviz="&st=pb"),
		Parameter("lookback", "dividend yield", ["div", "dividend", "yield"], finviz="&st=div"),
		Parameter("lookback", "EPS growth past 5 years", ["eps", "growth" "eps5y"], finviz="&st=eps5y"),
		Parameter("lookback", "float short", ["float", "short", "fs"], finviz="&st=short"),
		Parameter("lookback", "analysts recomendation", ["analysts", "recomendation", "recom", "rec", "ar"], finviz="&st=rec"),
		Parameter("lookback", "earnings day performance", ["earnings", "day", "performance", "edp", "earnperf", "edperf"], finviz="&st=earnperf"),
		Parameter("lookback", "earnings date", ["earnings", "earn", "date", "performance", "ep", "earndate", "edate", "eperf"], finviz="&st=earndate"),
		Parameter("type", "top100", ["top100", "100top", "100"], bitgur="top100/"),
		Parameter("type", "top10", ["top10", "10top", "10"], bitgur="top10/"),
		Parameter("type", "coins", ["coins", "coin"], bitgur="crypto/"),
		Parameter("type", "token", ["token", "tokens"], bitgur="token/"),
		Parameter("type", "all", ["full", "all", "every", "everything"], finviz="&t=sec_all", bitgur="all/"),
		Parameter("type", "s&p500", ["sp500", "s&p500", "sp", "spx"], finviz="&t=sec"),
		Parameter("type", "full", ["map", "geo", "world"], finviz="&t=geo"),
		Parameter("type", "exchange traded funds", ["etfs", "etf"], finviz="&t=etf"),
	],
	"style": [],
	"preferences": [
		Parameter("heatmap", "change", ["change"], bitgur="coins/", finviz=""),
		Parameter("heatmap", "volatility", ["volatility", "vol", "v"], bitgur="volatility/"),
		Parameter("heatmap", "exchanges", ["exchanges", "exchange", "exc", "e"], bitgur="exchanges/"),
		Parameter("heatmap", "trend", ["trend", "tre", "t"], bitgur="trend/"),
		Parameter("heatmap", "category", ["category", "cat", "c"], bitgur="category/"),
		Parameter("heatmap", "unusual", ["unusual", "volume", "unu", "unv", "uvol", "u"], bitgur="unusual_volume/"),
		Parameter("side", "gainers", ["gainers", "gainer", "gain", "g"], bitgur="gainers/"),
		Parameter("side", "losers", ["loosers", "looser", "losers", "loser", "loss", "l"], bitgur="loosers/"),
		Parameter("category", "mcap", [], bitgur="cap"),
		Parameter("category", "cryptocurrency", ["cryptocurrency", "crypto"], bitgur="cryptocurrency"),
		Parameter("category", "blockchain platforms", ["blockchain", "platforms"], bitgur="blockchain_platforms"),
		Parameter("category", "commerce and advertising", ["commerce", "advertising"], bitgur="commerce_and_advertising"),
		Parameter("category", "commodities", ["commodities"], bitgur="commodities"),
		Parameter("category", "content management", ["content", "management"], bitgur="content_management"),
		Parameter("category", "data storage and AI", ["data", "storage", "analytics", "ai"], bitgur="data_storage_analytics_and_ai"),
		Parameter("category", "drugs and healthcare", ["drugs", "healthcare"], bitgur="drugs_and_healthcare"),
		Parameter("category", "energy and utilities", ["energy", "utilities"], bitgur="energy_and_utilities"),
		Parameter("category", "events and entertainment", ["events", "entertainment"], bitgur="events_and_entertainment"),
		Parameter("category", "financial services", ["financial", "services"], bitgur="financial_services"),
		Parameter("category", "gambling and betting", ["gambling", "betting"], bitgur="gambling_and_betting"),
		Parameter("category", "gaming and VR", ["gaming", "vr"], bitgur="gaming_and_vr"),
		Parameter("category", "identy and reputation", ["identy", "reputation"], bitgur="identy_and_reputation"),
		Parameter("category", "legal", ["legal"], bitgur="legal"),
		Parameter("category", "real estate", ["real", "estate"], bitgur="real_estate"),
		Parameter("category", "social network", ["social", "network"], bitgur="social_network"),
		Parameter("category", "software", ["software"], bitgur="software"),
		Parameter("category", "supply and logistics", ["supply", "logistics"], bitgur="supply_and_logistics"),
		Parameter("category", "trading and investing", ["trading", "investing"], bitgur="trading_and_investing"),
		Parameter("autoDeleteOverride", "autodelete", ["del", "delete", "autodelete"], finviz="autodelete", bitgur="autodelete"),
		Parameter("hideRequest", "hide request", ["hide"], finviz="hide", bitgur="hide"),
		Parameter("forcePlatform", "force heat map on Finviz", ["fv", "finviz"], finviz=True),
		Parameter("forcePlatform", "force heat map on Bitgur", ["bg", "bitgur"], bitgur=True),
		Parameter("force", "force", ["--force"], finviz="force", bitgur="force"),
		Parameter("upload", "upload", ["--upload"], finviz="upload", bitgur="upload")
	]
}
DEFAULTS = {
	"Finviz": {
		"timeframes": [],
		"types": [AbstractRequest.find_parameter_with_id("type", name="s&p500", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Bitgur": {
		"timeframes": [],
		"types": [],
		"style": [],
		"preferences": []
	}
}


class HeatmapRequestHandler(AbstractRequestHandler):
	def __init__(self, platforms, bias="traditional", **kwargs):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = HeatmapRequest(platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			outputMessage, success = await request.add_timeframe(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_type(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_style(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_preferences(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			if finalOutput is None:
				request.set_error("`{}` is not a valid argument.".format(argument), isFatal=True)
			elif finalOutput.startswith("`Force Heat Map"):
				request.set_error(None, isFatal=True)
			else:
				request.set_error(finalOutput)

	async def process_ticker(self): raise NotImplementedError

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for type in PARAMETERS:
				request.set_default_for(type)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			types = "".join([e.parsed[platform] for e in request.types])
			styles = [e.parsed[platform] for e in request.styles]
			preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]

			if platform == "Finviz":
				isEtf = [e.get("value") for e in preferences if e.get("id") == "type"] == ["t=etf"]
				if len(request.timeframes) == 0:
					if "&st=" not in types:
						request.timeframes = [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)]
					elif isEtf and any([e in types for e in ["&st=ytd", "&st=relvol"]]):
						request.set_error("Heat map of `exchange traded funds` with select parameters is not available.")
					else:
						request.timeframes = [Parameter(None, None, None, finviz="")]
				elif "&st=" not in types:
					request.set_error("Timeframe cannot be used with selected heat map type.")
			
			elif platform == "Bitgur":
				for _ in range(8):
					preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]
					heatmap = [e.get("value") for e in preferences if e.get("id") == "heatmap"]
					side = [e.get("value") for e in preferences if e.get("id") == "side"]
					category = [e.get("value") for e in preferences if e.get("id") == "category"]

					# Add default heat map style
					if len(heatmap) == 0:
						if len(side) != 0: request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="trend", type="preferences", params=PARAMETERS)); continue
						elif len(category) != 0: request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="category", type="preferences", params=PARAMETERS)); continue
						else: request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="change", type="preferences", params=PARAMETERS)); continue

					# Timeframes are not supported on some heat map types
					[heatmap] = heatmap
					if heatmap in ["exchanges/", "volatility/", "unusual_volume/"]:
						if len(request.timeframes) != 0:
							if request.timeframes[0].id is not None: request.set_error("Timeframes are not supported on the {} heat map.".format(heatmap[:-1])); break
						else:
							request.timeframes = [Parameter(None, None, None, bitgur="")]; continue
					elif len(request.timeframes) == 0:
						request.timeframes = [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)]; continue

					# Category heat map checks
					if heatmap in ["category/"]:
						if len(category) == 0: request.set_error("Missing category."); break

					if heatmap in ["coins/", "trend/"]:
						if len(category) == 0 and types != "": request.preferences.append(AbstractRequest.find_parameter_with_id("category", name="mcap", type="preferences", params=PARAMETERS)); continue

					if heatmap in ["exchanges/", "category/"]:
						if types != "": request.set_error("Types are not supported on the {} heat map.".format(heatmap[:-1])); break
					elif types == "":
						request.preferences.append(AbstractRequest.find_parameter_with_id("type", name="all", type="types", params=PARAMETERS)); continue

					if heatmap in ["coins/", "exchanges/", "category/", "volatility/", "unusual_volume/"]:
						if len(side) != 0: request.set_error("Top gainers/losers are not supported on the {} heat map.".format(heatmap[:-1])); break
					elif len(side) == 0:
						request.preferences.append(AbstractRequest.find_parameter_with_id("side", name="gainers", type="preferences", params=PARAMETERS)); continue

					break


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		timeframes = []

		for platform in self.platforms:
			request = self.requests[platform].to_dict()
			timeframes.append(request.get("timeframes"))
			d[platform] = request

		d["timeframes"] = {p: t for p, t in zip(self.platforms, timeframes)}
		d["requestCount"] = len(d["timeframes"][d.get("currentPlatform")])

		return d


class HeatmapRequest(AbstractRequest):
	def __init__(self, platform, bias):
		super().__init__(platform, bias)

		self.timeframes = []
		self.types = []
		self.styles = []
		self.preferences = []

		self.currentTimeframe = None

	def add_parameter(self, argument, type):
		isSupported = None
		parsedParameter = None
		for param in PARAMETERS[type]:
			if argument in param.parsablePhrases:
				parsedParameter = param
				isSupported = param.supports(self.platform)
				if isSupported: break
		return isSupported, parsedParameter

	# async def add_timeframe(self, argument) -- inherited

	async def add_exchange(self, argument): raise NotImplementedError

	async def add_type(self, argument):
		heatmapStyleSupported, parsedHeatmapStyle = self.add_parameter(argument, "types")
		if parsedHeatmapStyle is not None and not self.has_parameter(parsedHeatmapStyle.id, self.types):
			if not heatmapStyleSupported:
				outputMessage = "`{}` heat map style is not supported on {}.".format(parsedHeatmapStyle.name.title(), self.platform)
				return outputMessage, False
			self.types.append(parsedHeatmapStyle)
			return None, True
		return None, None

	# async def add_style(self, argument) -- inherited

	# async def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "timeframes" and len(self.timeframes) == 0:
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.timeframes): self.timeframes.append(parameter)
		elif t == "types":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.types): self.types.append(parameter)
		elif t == "style":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.styles): self.styles.append(parameter)
		elif t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"parserBias": self.parserBias,
			"timeframes": [e.parsed[self.platform] for e in self.timeframes],
			"types": "".join([e.parsed[self.platform] for e in self.types]),
			"styles": [e.parsed[self.platform] for e in self.styles],
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences],
			"currentTimeframe": self.currentTimeframe
		}
		return d