from datetime import datetime
from pytz import utc

class CommandRequest(object):
	def __init__(self, raw=None, content=None, accountId=None, authorId=None, channelId=None, guildId=None, accountProperties={}, guildProperties={}, autodelete=None):
		self.raw = raw
		self.content = content

		_timestamp = datetime.now().astimezone(utc)
		self.snapshot = "{}-{:02d}".format(_timestamp.year, _timestamp.month)

		self.accountId = accountId
		self.authorId = authorId
		self.channelId = channelId
		self.guildId = guildId

		self.accountProperties = accountProperties
		self.guildProperties = CommandRequest.create_guild_settings(guildProperties)
		self.overrides = self.guildProperties.get("overrides", {}).get(str(channelId), {})

		self.autodelete = autodelete
		if autodelete is not None and autodelete < 0:
			self.autodelete = None
		elif autodelete is None and self.overrides.get("messageProcessing", {}).get("autodelete", self.guildProperties["settings"]["messageProcessing"]["autodelete"]):
			self.autodelete = 1

		self.marketBias = self.overrides.get("messageProcessing", {}).get("bias", self.guildProperties["settings"]["messageProcessing"]["bias"])


	# -------------------------
	# Charting platforms
	# -------------------------

	def get_platform_order_for(self, commandType, assetType=None):
		if assetType is not None and assetType != "":
			if assetType == "crypto": self.marketBias == "crypto"
			else: self.marketBias == "traditional"

		if commandType == "c":
			if self.marketBias == "traditional":
				return (self.accountProperties["settings"]["charts"]["preferredOrder"] if "settings" in self.accountProperties else ["TradingView", "GoCharting", "Finviz", "TradingLite", "Bookmap"]) + ["Alternative.me"]
			else:
				return ["Alternative.me"] + (self.accountProperties["settings"]["charts"]["preferredOrder"] if "settings" in self.accountProperties else ["TradingView", "GoCharting", "Finviz", "TradingLite", "Bookmap"])
		elif commandType == "hmap":
			if self.marketBias == "traditional":
				return ["Finviz", "Bitgur"]
			else:
				return ["Bitgur", "Finviz"]
		elif commandType == "p":
			if self.marketBias == "traditional":
				return ["IEXC", "Alternative.me", "CoinGecko", "CCXT", "Serum", "LLD"]
			else:
				return ["Alternative.me", "CoinGecko", "CCXT", "Serum", "IEXC", "LLD"]
		elif commandType == "info":
			if self.marketBias == "traditional":
				return ["IEXC", "CoinGecko"]
			else:
				return ["CoinGecko", "IEXC"]
		elif commandType == "x":
			return ["CCXT"]
		else:
			raise ValueError("incorrect commant type: {}".format(commandType))


	# -------------------------
	# User properties
	# -------------------------

	def is_registered(self):
		return "customer" in self.accountProperties

	def is_pro(self):
		return self.is_registered() and self.accountProperties["customer"]["personalSubscription"].get("plan", "free") == "price_HLr5Pnrj3yRWOP"

	def is_trialing(self):
		return self.is_pro() and self.accountProperties["customer"]["personalSubscription"].get("trialing", False)


	def personal_price_alerts_available(self):
		return self.is_registered() and (self.is_trialing() or bool(self.accountProperties["customer"]["addons"].get("marketAlerts", 0)))

	def personal_flow_available(self):
		return self.is_registered() and (self.is_trialing() or bool(self.accountProperties["customer"]["addons"].get("flow", 0)))

	def personal_statistics_available(self):
		return self.is_registered() and (self.is_trialing() or bool(self.accountProperties["customer"]["addons"].get("statistics", 0)))


	# -------------------------
	# Server properties
	# -------------------------

	def is_serverwide_pro_used(self):
		return self.serverwide_price_alerts_available() or self.serverwide_flow_available() or self.serverwide_statistics_available()

	def serverwide_price_alerts_available(self):
		return self.guildProperties["addons"]["marketAlerts"]["enabled"]

	def serverwide_flow_available(self):
		return self.guildProperties["addons"]["flow"]["enabled"]

	def serverwide_statistics_available(self):
		return self.guildProperties["addons"]["statistics"]["enabled"]


	# -------------------------
	# Global properties
	# -------------------------

	def price_alerts_available(self):
		return self.serverwide_price_alerts_available() or self.personal_price_alerts_available()

	def flow_available(self):
		return self.serverwide_flow_available() or self.personal_flow_available()

	def statistics_available(self):
		return self.serverwide_statistics_available() or self.personal_statistics_available()


	# -------------------------
	# Helpers
	# -------------------------

	@staticmethod
	def create_guild_settings(settings):
		settingsTemplate = {
			"addons": {
				"satellites": {
					"enabled": False
				},
				"marketAlerts": {
					"enabled": False
				},
				"flow": {
					"enabled": False
				},
				"statistics": {
					"enabled": False
				}
			},
			"settings": {
				"assistant": {
					"enabled": True
				},
				"channels": {
					"public": None,
					"private": None
				},
				"cope": {
					"holding": [],
					"voting": []
				},
				"messageProcessing": {
					"bias": "traditional",
					"autodelete": False,
					"sentiment": True
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