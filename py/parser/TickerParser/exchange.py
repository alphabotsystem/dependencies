from time import time
import ccxt


class Exchange(object):
	def __init__(self, id, marketType, name=None, region=None, cache=None):
		self.id = id
		self.name = None
		self.region = region
		self.properties = None
		self.type = marketType
		self.stale = False

		if self.type == "crypto":
			self.properties = getattr(ccxt, id)() if cache is None else cache
			if cache is None:
				try: self.properties.load_markets()
				except: self.stale = True
			if id == "binanceusdm": self.name = "Binance Futures" # USDⓈ-M
			elif id == "binancecoinm": self.name = "Binance Futures COIN-M"
			else: self.name = self.properties.name
		else:
			self.properties = StocksExchange(id)
			self.name = id.title() if name is None else name

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"region": self.region,
			"type": self.type
		}

	@staticmethod
	def from_dict(d, cache=None):
		if d is None or not d: return None
		return Exchange(d.get("id"), d.get("type"), d.get("name"), d.get("region"), cache=cache)

	def __hash__(self):
		return hash(self.id)

	def __str__(self):
		return f"{self.name} [id: {self.id}]"

class StocksExchange(object):
	def __init__(self, id):
		self.id = id
		self.symbols = []
		self.markets = {}
		self.timeframes = ["1m"]

	def milliseconds(self):
		return int(time() * 1000)