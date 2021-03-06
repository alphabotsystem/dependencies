from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from TickerParser import TickerParser, Exchange
from .parameter import PriceParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"preferences": [
		Parameter("lld", "funding", ["fun", "fund", "funding"], lld="funding"),
		Parameter("lld", "open interest", ["oi", "openinterest", "ov", "openvalue"], lld="oi"),
		Parameter("lld", "longs/shorts ratio", ["ls", "l/s", "longs/shorts", "long/short"], lld="ls"),
		Parameter("lld", "shorts/longs ratio", ["sl", "s/l", "shorts/longs", "short/long"], lld="sl"),
		Parameter("lld", "dominance", ["dom", "dominance"], lld="dom"),
		Parameter("forcePlatform", "force quote on CoinGecko", ["cg", "coingecko"], coingecko=True),
		Parameter("forcePlatform", "force quote on a crypto exchange", ["cx", "ccxt", "crypto", "exchange"], ccxt=True),
		Parameter("forcePlatform", "force quote on a stock exchange", ["ix", "iexc", "stock", "stocks"], iexc=True),
		Parameter("forcePlatform", "force quote on Serum", ["serum", "srm"], serum=True),
		Parameter("forcePlatform", "force quote on Alternative.me", ["am", "alternativeme"], alternativeme=True),
		Parameter("forcePlatform", "force quote on CNN Business", ["cnn", "cnnbusiness"], cnnbusiness=True),
		Parameter("force", "force", ["--force"], ccxt="force", iexc="force")
	]
}
DEFAULTS = {
	"Alternative.me": {
		"preferences": []
	},
	"CNN Business": {
		"preferences": []
	},
	"CoinGecko": {
		"preferences": []
	},
	"CCXT": {
		"preferences": []
	},
	"IEXC": {
		"preferences": []
	},
	"Serum": {
		"preferences": []
	},
	"LLD": {
		"preferences": []
	}
}


class PriceRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional"):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = PriceRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			_argument = argument.lower().replace(" ", "")
			if request.errorIsFatal or argument == "": continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			outputMessage, success = await request.add_preferences(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_exchange(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			if finalOutput is None:
				request.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
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

			preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]

			if platform == "Alternative.me":
				if request.tickerId not in ["FGI"]: request.set_error(None, isFatal=True)

			elif platform == "CNN Business":
				if request.tickerId not in ["FGI"]: request.set_error(None, isFatal=True)

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

		self.preferences = []

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

	async def add_style(self, argument): raise NotImplementedError

	# async def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"exchange": self.exchange,
			"parserBias": self.parserBias,
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences]
		}
		return d