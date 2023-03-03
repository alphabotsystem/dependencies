from time import time
from datetime import datetime

class CommandRequest(object):
	def __init__(self, raw=None, content=None, accountId=None, authorId=None, channelId=None, guildId=None, accountProperties={}, guildProperties={}, autodelete=None, origin="default"):
		self.raw = raw
		self.content = content
		self.origin = str(origin)

		self.start = time()
		_timestamp = datetime.utcfromtimestamp(self.start)
		self.snapshot = "{}-{:02d}".format(_timestamp.year, _timestamp.month)
		self.telemetry = {
			"database": None,
			"prelight": None,
			"parser": None,
			"request": None,
			"response": None
		}

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
				order = ["CNN Business", "TradingView", "TradingLite", "Bookmap", "Alternative.me"]
				if self.advanced_charting_available():
					order.insert(order.index("TradingView"), "TradingView Premium")
				return order
			else:
				order = ["Alternative.me", "TradingView", "TradingLite", "Bookmap", "CNN Business"]
				if self.advanced_charting_available():
					order.insert(order.index("TradingView"), "TradingView Premium")
				return order
		elif commandType == "hmap":
			if self.marketBias == "traditional":
				return ["TradingView Stock Heatmap", "TradingView Crypto Heatmap"]
			else:
				return ["TradingView Crypto Heatmap", "TradingView Stock Heatmap"]
		elif commandType == "flow":
			return ["Alpha Flow"]
		elif commandType == "p":
			if self.marketBias == "traditional":
				return ["CNN Business", "IEXC", "CCXT", "CoinGecko", "Alternative.me"]
			else:
				return ["Alternative.me", "CCXT", "CoinGecko", "IEXC", "CNN Business"]
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
		elif commandType == "lookup":
			if self.marketBias == "traditional":
				return ["IEXC", "CCXT", "CoinGecko", "TradingView", "TradingLite", "Bookmap"]
			else:
				return ["CCXT", "CoinGecko", "IEXC", "TradingView", "TradingLite", "Bookmap"]
		elif commandType == "alert" or commandType == "paper":
			if self.marketBias == "traditional":
				return ["IEXC", "CCXT"]
			else:
				return ["CCXT", "IEXC"]
		elif commandType == "convert":
			if self.marketBias == "traditional":
				return ["IEXC", "CCXT", "CoinGecko"]
			else:
				return ["CCXT", "CoinGecko", "IEXC"]
		else:
			raise ValueError(f"incorrect commant type: {commandType}")


	# -------------------------
	# Telemetry
	# -------------------------

	def set_delay(self, at, delay):
		if at not in self.telemetry:
			raise Exception(f"{at} is not a valid telemetry checkpoint")
		self.telemetry[at] = delay

	def get_delay(self, at):
		if at not in self.telemetry:
			raise Exception(f"{at} is not a valid telemetry checkpoint")
		return self.telemetry[at]


	# -------------------------
	# Global properties
	# -------------------------

	def is_registered(self):
		return "customer" in self.accountProperties

	def is_feature_available(self, feature):
		ownerSlots = self.guildProperties.get("connection", {}).get("customer", {}).get("slots", {}).get(feature, {})
		ownerSubscription = self.guildProperties.get("connection", {}).get("customer", {}).get("subscriptions", {}).get(feature, 0)
		ownerFilledSlots = sorted(ownerSlots.keys())[:ownerSubscription]
		userSlots = self.accountProperties.get("customer", {}).get("slots", {}).get(feature, {})
		userSubscription = self.accountProperties.get("customer", {}).get("subscriptions", {}).get(feature, 0)
		userFilledSlots = sorted(userSlots.keys())[:userSubscription]
		return str(self.guildId) in ownerFilledSlots or "personal" in userFilledSlots

	def price_alerts_available(self):
		return self.is_feature_available("priceAlerts")

	def advanced_charting_available(self):
		return self.is_feature_available("advancedCharting")

	def scheduled_posting_available(self):
		return self.is_feature_available("scheduledPosting")

	def flow_available(self):
		return self.is_feature_available("flow")


	# -------------------------
	# Helpers
	# -------------------------

	@staticmethod
	def create_guild_settings(settings):
		settingsTemplate = {
			"charting": {
				"theme": "dark",
				"timeframe": "1-hour",
				"indicators": [],
				"chartType": "candles"
			},
			"settings": {
				"assistant": {
					"enabled": True
				},
				"messageProcessing": {
					"bias": "traditional",
					"autodelete": None
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