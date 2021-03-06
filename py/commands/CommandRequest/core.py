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
				return ["CNN Business", "IEXC", "CoinGecko", "CCXT", "Serum", "LLD", "Alternative.me"]
			else:
				return ["Alternative.me", "CoinGecko", "CCXT", "Serum", "IEXC", "LLD", "CNN Business"]
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
				return ["IEXC", "CoinGecko", "CCXT", "Serum"]
			else:
				return ["CoinGecko", "CCXT", "IEXC", "Serum"]
		else:
			raise ValueError(f"incorrect commant type: {commandType}")


	# -------------------------
	# User properties
	# -------------------------

	def is_registered(self):
		return "customer" in self.accountProperties


	def personal_price_alerts_available(self):
		return False
		# return self.is_registered() and bool(self.accountProperties["customer"]["addons"].get("marketAlerts", 0))

	def personal_flow_available(self):
		return False
		# return self.is_registered() and bool(self.accountProperties["customer"]["addons"].get("flow", 0))


	# -------------------------
	# Server properties
	# -------------------------

	def serverwide_price_alerts_available(self):
		return self.guildProperties.get("connection", {}).get("customer", {}).get("slots", {}).get("priceAlerts", {}).get(self.guildId, 0) == 1

	def serverwide_flow_available(self):
		return self.guildProperties.get("connection", {}).get("customer", {}).get("slots", {}).get("flow", {}).get(self.guildId, 0) == 1


	# -------------------------
	# Global properties
	# -------------------------

	def price_alerts_available(self):
		return self.is_serverwide_price_alerts_available() or self.is_personal_price_alerts_available()

	def flow_available(self):
		return self.is_serverwide_flow_available() or self.is_personal_flow_available()


	# -------------------------
	# Helpers
	# -------------------------

	@staticmethod
	def create_guild_settings(settings):
		settingsTemplate = {
			"addons": {
				"satellites": {}
			},
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