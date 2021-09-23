from os import environ
from sys import maxsize as MAXSIZE
from time import time
from asyncio import wait
from traceback import format_exc

from TickerParserPy import TickerParser, Exchange
from .parameter import TradeParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"preferences": [
		Parameter("autoDeleteOverride", "autodelete", ["del", "delete", "autodelete"], ichibot="autodelete"),
		Parameter("hideRequest", "hide request", ["hide"], ichibot="hide"),
	]
}
DEFAULTS = {
	"Ichibot": {
		"preferences": []
	}
}

class TradeRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional", **kwargs):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = TradeRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

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
			elif finalOutput.startswith("`Force Trade"):
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

			if platform == "Ichibot":
				if not bool(request.exchange):
					try: _, request.exchange = await TickerParser.find_exchange("ftx", platform, request.parserBias)
					except: pass
				if request.exchange.get("id") == "binanceusdm":
					request.exchange["id"] = "binancefutures"


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		for platform in self.platforms:
			d[platform] = self.requests[platform].to_dict()

		return d


class TradeRequest(AbstractRequest):
	def __init__(self, tickerId, platform, bias):
		super().__init__(platform, bias)
		self.tickerId = tickerId
		self.ticker = {}
		self.exchange = {}

		self.preferences = []
		self.numericalParameters = []

		self.hasExchange = False

	async def process_ticker(self):
		for i in range(len(self.ticker.parts)):
			tickerPart = self.ticker.parts[i]
			if type(tickerPart) is str: continue

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
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences],
			"numericalParameters": self.numericalParameters
		}
		return d