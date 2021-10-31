from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from TickerParser import TickerParser, Exchange
from .parameter import PriceParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"style": [],
	"preferences": [
		Parameter("lld", "funding", ["fun", "fund", "funding"], lld="funding"),
		Parameter("lld", "open interest", ["oi", "openinterest", "ov", "openvalue"], lld="oi"),
		Parameter("lld", "longs/shorts ratio", ["ls", "l/s", "longs/shorts", "long/short"], lld="ls"),
		Parameter("lld", "shorts/longs ratio", ["sl", "s/l", "shorts/longs", "short/long"], lld="sl"),
		Parameter("lld", "dominance", ["dom", "dominance"], lld="dom"),
		Parameter("isAmountPercent", "percentage amount", ["%"], ccxt="amountPercent", iexc="amountPercent", serum="amountPercent"),
		Parameter("isPricePercent", "percentage price", ["%"], ccxt="pricePercent", iexc="pricePercent", serum="pricePercent"),
		Parameter("isLimitOrder", "limit order", ["@", "at"], ccxt="limitOrder", iexc="limitOrder", serum="limitOrder"),
		Parameter("autoDeleteOverride", "autodelete", ["del", "delete", "autodelete"], coingecko="autodelete", ccxt="autodelete", iexc="autodelete", serum="autodelete", alternativeme="autodelete", lld="autodelete"),
		Parameter("hideRequest", "hide request", ["hide"], coingecko="hide", ccxt="hide", iexc="hide", serum="hide", alternativeme="hide", lld="hide"),
		Parameter("public", "public trigger", ["pub", "publish", "public"], ccxt="public", iexc="public", serum="public"),
		Parameter("message", "alert trigger message", ["message"], ccxt="message", iexc="message", serum="message"),
		Parameter("forcePlatform", "force quote on CoinGecko", ["cg", "coingecko"], coingecko=True),
		Parameter("forcePlatform", "force quote on a crypto exchange", ["cx", "ccxt", "crypto"], ccxt=True),
		Parameter("forcePlatform", "force quote on a stock exchange", ["ix", "iexc", "stock"], iexc=True),
		Parameter("forcePlatform", "force quote on Serum", ["serum", "srm"], serum=True),
		Parameter("forcePlatform", "force quote on Alternative.me", ["am", "alternativeme"], alternativeme=True),
		Parameter("force", "force", ["--force"], ccxt="force", iexc="force"),
		Parameter("upload", "upload", ["--upload"], ccxt="upload", iexc="upload")
	]
}
DEFAULTS = {
	"Alternative.me": {
		"style": [],
		"preferences": []
	},
	"CoinGecko": {
		"style": [],
		"preferences": []
	},
	"CCXT": {
		"style": [],
		"preferences": []
	},
	"IEXC": {
		"style": [],
		"preferences": []
	},
	"Serum": {
		"style": [],
		"preferences": []
	},
	"LLD": {
		"style": [],
		"preferences": []
	}
}


class PriceRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional", **kwargs):
		super().__init__(platforms)
		self.isMarketAlert = kwargs.get("isMarketAlert", False)
		self.isPaperTrade = kwargs.get("isPaperTrade", False)
		for platform in platforms:
			self.requests[platform] = PriceRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			outputMessage, success = await request.add_style(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_preferences(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_exchange(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_numerical_parameters(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			if finalOutput is None:
				request.set_error("`{}` is not a valid argument.".format(argument), isFatal=True)
			elif finalOutput.startswith("`Force Quote"):
				request.set_error(None, isFatal=True)
			else:
				request.set_error(finalOutput)
	
	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for type in PARAMETERS:
				request.set_default_for(type)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			styles = [e.parsed[platform] for e in request.styles]
			preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]

			if self.isMarketAlert:
				if not request.ticker.get("isSimple"):
					request.set_error("Price alerts for aggregated tickers aren't available.", isFatal=True)
				if len(request.numericalParameters) > 1:
					request.set_error("Only one alert trigger level can be specified at once.")
				elif len(request.numericalParameters) == 0:
					request.set_error("Alert trigger level was not provided.")
				if {"id": "isAmountPercent", "value": "amountPercent"} in preferences:
					request.set_error("`Percentage Amount` parameter is only supported by Alpha Paper Trader.")
				if {"id": "isPricePercent", "value": "pricePercent"} in preferences:
					request.set_error("`Percentage Price` parameter is only supported by Alpha Paper Trader.")
				if {"id": "isLimitOrder", "value": "limitOrder"} in preferences:
					request.set_error("`Limit Order` parameter is only supported by Alpha Paper Trader.")
			elif self.isPaperTrade:
				if not request.ticker.get("isSimple"):
					request.set_error("Paper trading for aggregated tickers isn't available.", isFatal=True)
				if request.hasExchange:
					request.set_error("Specifying an exchange is not supported. Omit the exchange from your request to execute the trade.", isFatal=True)
				if request.ticker.get("id") is not None:
					if len(request.numericalParameters) == 0: request.set_error("Paper trade amount was not provided.")
					elif len(request.numericalParameters) > 2: request.set_error("Too many numerical arguments provided.")
				else:
					if len(request.numericalParameters) != 0: request.set_error("Numerical arguments can't be used with this command.")
				if {"id": "public", "value": "public"} in preferences:
					request.set_error("`Public Trigger` parameter is only supported by Price Alerts.")
			else:
				if len(request.numericalParameters) > 0:
					request.set_error("Only Alpha Price Alerts accept numerical parameters.".format(request.ticker.get("id")), isFatal=True)
				if {"id": "public", "value": "public"} in preferences:
					request.set_error("`Public Trigger` parameter is only supported by Price Alerts.")
				if {"id": "isAmountPercent", "value": "amountPercent"} in preferences:
					request.set_error("`Percentage Amount` parameter is only supported by Alpha Paper Trader.")
				if {"id": "isPricePercent", "value": "pricePercent"} in preferences:
					request.set_error("`Percentage Price` parameter is only supported by Alpha Paper Trader.")
				if {"id": "isLimitOrder", "value": "limitOrder"} in preferences:
					request.set_error("`Limit Order` parameter is only supported by Alpha Paper Trader.")

			if platform == "Alternative.me":
				if request.tickerId not in ["FGI"]:
					request.set_error(None, isFatal=True)

			elif platform == "CoinGecko":
				if request.couldFail: request.set_error(None, isFatal=True)
				if bool(request.exchange) or ("CCXT" in self.requests and self.requests["CCXT"].ticker.get("mcapRank", MAXSIZE) < request.ticker.get("mcapRank", MAXSIZE)):
					request.set_error(None, isFatal=True)

			elif platform == "CCXT":
				if not bool(request.exchange) or request.couldFail: request.set_error(None, isFatal=True)

			elif platform == "IEXC":
				if request.couldFail: request.set_error(None, isFatal=True)

			elif platform == "Serum":
				if request.couldFail: request.set_error(None, isFatal=True)

			elif platform == "LLD":
				if not bool(request.exchange) and request.ticker.get("id") not in ["MCAP"]:
					request.set_error(None, isFatal=True)


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		for platform in self.platforms:
			d[platform] = self.requests[platform].to_dict()

		return d


class PriceRequest(AbstractRequest):
	def __init__(self, tickerId, platform, bias):
		super().__init__(platform, bias)
		self.tickerId = tickerId
		self.ticker = {}
		self.exchange = {}

		self.styles = []
		self.preferences = []
		self.numericalParameters = []

		self.hasExchange = False

	async def process_ticker(self):
		preferences = [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences]
		if any([e.get("id") in ["funding", "oi"] for e in preferences]):
			if not self.hasExchange:
				try: _, self.exchange = await TickerParser.find_exchange("bitmex", self.platform, self.parserBias)
				except: pass
		elif any([e.get("id") in ["ls", "sl"] for e in preferences]):
			if not self.hasExchange:
				try: _, self.exchange = await TickerParser.find_exchange("bitfinex", self.platform, self.parserBias)
				except: pass

		updatedTicker, error = None, None
		try: updatedTicker, error = await TickerParser.match_ticker(self.tickerId, self.exchange, self.platform, self.parserBias)
		except: pass

		if error is not None:
			self.set_error(error, isFatal=True)
		elif not updatedTicker:
			self.couldFail = True
		else:
			self.ticker = updatedTicker
			self.tickerId = updatedTicker.get("id")
			self.exchange = updatedTicker.get("exchange")

	def add_parameter(self, argument, type):
		isSupported = None
		parsedParameter = None
		for param in PARAMETERS[type]:
			if argument in param.parsablePhrases:
				parsedParameter = param
				isSupported = param.supports(self.platform)
				if isSupported: break
		return isSupported, parsedParameter

	async def add_timeframe(self, argument): raise NotImplementedError

	# async def add_exchange(self, argument) -- inherited

	# async def add_style(self, argument) -- inherited

	# async def add_preferences(self, argument) -- inherited

	async def add_numerical_parameters(self, argument):
		try:
			numericalParameter = float(argument)
			if numericalParameter <= 0:
				outputMessage = "Only parameters greater than `0` are accepted."
				return outputMessage, False
			self.numericalParameters.append(numericalParameter)
			return None, True
		except: return None, None

	def set_default_for(self, t):
		if t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"exchange": self.exchange,
			"parserBias": self.parserBias,
			"styles": [e.parsed[self.platform] for e in self.styles],
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences],
			"numericalParameters": self.numericalParameters
		}
		return d