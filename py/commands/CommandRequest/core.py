from datetime import datetime
from pytz import utc

class CommandRequest(object):
	def __init__(self, raw=None, content=None, accountId=None, authorId=None, channelId=None, guildId=None, accountProperties={}, guildProperties={}, autodelete=None, deferment=None):
		self.raw = raw
		self.content = content
		self.deferment = deferment

		_timestamp = datetime.now().astimezone(utc)
		self.snapshot = "{}-{:02d}".format(_timestamp.year, _timestamp.month)

		self.accountId = accountId
		self.authorId = authorId
		self.channelId = channelId
		self.guildId = guildId

		self.accountProperties = accountProperties
		self.guildProperties = CommandRequest.create_guild_settings(guildProperties)
		self.overrides = self.guildProperties.get("overrides", {}).get(str(channelId), {})

		defaultSettings = self.guildProperties["settings"]["messageProcessing"]

		self.autodelete = autodelete
		if autodelete is not None and autodelete < 0:
			self.autodelete = None
		elif autodelete is None and self.overrides.get("messageProcessing", {}).get("autodelete", defaultSettings["autodelete"]):
			self.autodelete = 1

		self.marketBias = self.overrides.get("messageProcessing", {}).get("bias", defaultSettings["bias"])


	# -------------------------
	# Charting platforms
	# -------------------------

	def get_platform_order_for(self, commandType, assetType=None):
		if assetType is not None and assetType != "":
			if assetType == "crypto": self.marketBias == "crypto"
			else: self.marketBias == "traditional"

		if commandType == "c":
			chartSettings = self.accountProperties.get("settings", {}).get("charts", {})
			if self.marketBias == "traditional":
				return ["CNN Business"] + chartSettings.get("preferredOrder", ["TradingView", "GoCharting", "Finviz", "TradingLite", "Bookmap"]) + ["Alternative.me"]
			else:
				return ["Alternative.me"] + chartSettings.get("preferredOrder", ["TradingView", "GoCharting", "Finviz", "TradingLite", "Bookmap"]) + ["CNN Business"]
		elif commandType == "hmap":
			if self.marketBias == "traditional":
				return ["TradingView Stock Heatmap", "TradingView Crypto Heatmap"]
			else:
				return ["TradingView Crypto Heatmap", "TradingView Stock Heatmap"]
		elif commandType == "flow":
			return ["Alpha Flow"]
		elif commandType == "p":
			if self.marketBias == "traditional":
				return ["CNN Business", "IEXC", "CCXT", "CoinGecko", "Serum", "LLD", "Alternative.me"]
			else:
				return ["Alternative.me", "CCXT", "CoinGecko", "IEXC", "Serum", "LLD", "CNN Business"]
		elif commandType == "v":
			if self.marketBias == "traditional":
				return ["IEXC", "CoinGecko", "CCXT"]
			else:
				return ["CoinGecko", "CCXT", "IEXC"]
		elif commandType == "d":
			if self.marketBias == "traditional":
				return ["IEXC", "CCXT"]
			else:
				return ["CCXT", "IEXC"]
		elif commandType == "info":
			if self.marketBias == "traditional":
				return ["IEXC", "CoinGecko"]
			else:
				return ["CoinGecko", "IEXC"]
		elif commandType == "alert" or commandType == "paper":
			if self.marketBias == "traditional":
				return ["IEXC", "CCXT"]
			else:
				return ["CCXT", "IEXC"]
		elif commandType == "convert":
			if self.marketBias == "traditional":
				return ["IEXC", "CCXT", "CoinGecko", "Serum"]
			else:
				return ["CCXT", "CoinGecko", "IEXC", "Serum"]
		else:
			raise ValueError(f"incorrect commant type: {commandType}")


	# -------------------------
	# Global properties
	# -------------------------

	def is_registered(self):
		return "customer" in self.accountProperties

	def price_alerts_available(self):
		slots = self.guildProperties.get("connection", {}).get("customer", {}).get("slots", {}).get("priceAlerts", {})
		subscription = self.guildProperties.get("connection", {}).get("customer", {}).get("subscriptions", {}).get("priceAlerts", 0)
		filled = sorted(slots.keys())[:subscription]
		return self.guildId in filled or "personal" in filled

	def flow_available(self):
		slots = self.guildProperties.get("connection", {}).get("customer", {}).get("slots", {}).get("flow", {})
		subscription = self.guildProperties.get("connection", {}).get("customer", {}).get("subscriptions", {}).get("flow", 0)
		filled = sorted(slots.keys())[:subscription]
		return self.guildId in filled or "personal" in filled


	# -------------------------
	# Helpers
	# -------------------------

	@staticmethod
	def create_guild_settings(settings):
		settingsTemplate = {
			"settings": {
				"assistant": {
					"enabled": True
				},
				"messageProcessing": {
					"bias": "traditional",
					"autodelete": False
				},
				"setup": {
					"completed": False,
					"connection": None,
					"tos": 1.0
				}
			}
		}

		if settings is None: settings = {}
		CommandRequest.__recursive_fill(settings, settingsTemplate)

		return settings

	@staticmethod
	def __recursive_fill(settings, template):
		for e in template:
			if type(template[e]) is dict:
				if e not in settings:
					settings[e] = template[e].copy()
				else:
					CommandRequest.__recursive_fill(settings[e], template[e])
			elif e not in settings:
				settings[e] = template[e]