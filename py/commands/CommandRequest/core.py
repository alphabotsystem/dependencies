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
				order = ["CNN Business", "TradingView", "TradingLite", "Alternative.me"]
				if self.advanced_charting_available():
					order.insert(order.index("TradingView"), "TradingView Premium")
				return order
			else:
				order = ["Alternative.me", "TradingView", "TradingLite", "CNN Business"]
				if self.advanced_charting_available():
					order.insert(order.index("TradingView"), "TradingView Premium")
				return order
		elif commandType == "hmap":
			if self.marketBias == "traditional":
				return ["TradingView Stock Heatmap", "TradingView ETF Heatmap", "TradingView Crypto Heatmap"]
			else:
				return ["TradingView Crypto Heatmap", "TradingView Stock Heatmap", "TradingView ETF Heatmap"]
		elif commandType == "flow":
			return ["Alpha Flow"]
		elif commandType == "p":
			if self.marketBias == "traditional":
				return ["CNN Business", "Twelvedata", "CCXT", "CoinGecko", "Alternative.me", "Blockchair"]
			else:
				return ["Alternative.me", "CCXT", "CoinGecko", "Twelvedata", "CNN Business", "Blockchair"]
		elif commandType == "v":
			if self.marketBias == "traditional":
				return ["Twelvedata", "CoinGecko", "CCXT"]
			else:
				return ["CoinGecko", "CCXT", "Twelvedata"]
		elif commandType == "d":
			if self.marketBias == "traditional":
				return ["Twelvedata", "CCXT"]
			else:
				return ["CCXT", "Twelvedata"]
		elif commandType == "info":
			if self.marketBias == "traditional":
				return ["Twelvedata", "CoinGecko"]
			else:
				return ["CoinGecko", "Twelvedata"]
		elif commandType == "lookup":
			if self.marketBias == "traditional":
				return ["Twelvedata", "CCXT", "CoinGecko", "TradingView", "TradingLite"]
			else:
				return ["CCXT", "CoinGecko", "Twelvedata", "TradingView", "TradingLite"]
		elif commandType == "alert" or commandType == "paper":
			if self.marketBias == "traditional":
				return ["Twelvedata", "CCXT"]
			else:
				return ["CCXT", "Twelvedata"]
		elif commandType == "convert":
			if self.marketBias == "traditional":
				return ["Twelvedata", "CCXT", "CoinGecko"]
			else:
				return ["CCXT", "CoinGecko", "Twelvedata"]
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

	def advanced_charting_available(self):
		return self.is_feature_available("advancedCharting")

	def scheduled_posting_available(self):
		return self.is_feature_available("scheduledPosting")

	def tradingview_layouts_available(self):
		return self.is_feature_available("tradingviewLayouts")

	def price_satellites_available(self):
		return self.is_feature_available("satellites")

	def price_alerts_available(self):
		return self.is_feature_available("priceAlerts")

	def bot_license_available(self):
		return self.is_feature_available("botLicense")

	def flow_available(self):
		return self.is_feature_available("flow")

	def is_paid_user(self):
		return self.advanced_charting_available() or self.scheduled_posting_available() or self.tradingview_layouts_available() or self.price_satellites_available() or self.price_alerts_available() or self.bot_license_available() or self.flow_available()


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