class AbstractParameter(object):
	def __init__(self, id, name, parsablePhrases, requiresPro=False):
		self.id = id
		self.name = name
		self.parsablePhrases = parsablePhrases
		self.requiresPro = requiresPro
		self.parsed = {}
		self.dynamic = {}

	def supports(self, platform):
		return self.parsed[platform] is not None

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"parsablePhrases": self.parsablePhrases,
			"requiresPro": self.requiresPro,
			"parsed": self.parsed,
			"dynamic": self.dynamic
		}

	@staticmethod
	def from_dict(d):
		parameter = AbstractParameter(d.get("id"), d.get("name"), d.get("parsablePhrases", []), d.get("requiresPro", False))
		parameter.parsed = d.get("parsed", {})
		parameter.dynamic = d.get("dynamic", {})
		return parameter

class ChartParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, tradinglite=None, tradingview=None, bookmap=None, gocharting=None, finviz=None, alternativeme=None, alphaflow=None, requiresPro=False, dynamic=None):
		super().__init__(id, name, parsablePhrases, requiresPro)
		self.parsed = {
			"Alternative.me": alternativeme,
			"TradingLite": tradinglite,
			"TradingView": tradingview,
			"Bookmap": bookmap,
			"GoCharting": gocharting,
			"Finviz": finviz,
			"Alpha Flow": alphaflow
		}
		self.dynamic = dynamic

class HeatmapParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, finviz=None, bitgur=None, requiresPro=False):
		super().__init__(id, name, parsablePhrases, requiresPro)
		self.parsed = {
			"Bitgur": bitgur,
			"Finviz": finviz
		}

class PriceParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, coingecko=None, ccxt=None, iexc=None, serum=None, alternativeme=None, lld=None, requiresPro=False):
		super().__init__(id, name, parsablePhrases, requiresPro)
		self.parsed = {
			"Alternative.me": alternativeme,
			"CoinGecko": coingecko,
			"CCXT": ccxt,
			"IEXC": iexc,
			"Serum": serum,
			"LLD": lld
		}

class DetailParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, coingecko=None, iexc=None, requiresPro=False):
		super().__init__(id, name, parsablePhrases, requiresPro)
		self.parsed = {
			"CoinGecko": coingecko,
			"IEXC": iexc
		}

class TradeParameter(AbstractParameter):
	def __init__(self, id, name, parsablePhrases, ichibot=None, requiresPro=False):
		super().__init__(id, name, parsablePhrases, requiresPro)
		self.parsed = {
			"Ichibot": ichibot
		}