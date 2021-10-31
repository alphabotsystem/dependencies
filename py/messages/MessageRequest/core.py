class MessageRequest(object):
	def __init__(self, raw=None, content=None, accountId=None, authorId=None, channelId=None, guildId=None, presetUsed=False, accountProperties={}, guildProperties={}):
		self.raw = raw
		self.content = content

		self.accountId = accountId
		self.authorId = authorId
		self.channelId = channelId
		self.guildId = guildId

		self.accountProperties = accountProperties
		self.guildProperties = MessageRequest.create_guild_settings(guildProperties)
		self.overrides = self.guildProperties.get("overrides", {})

		self.presetUsed = False

		self.autodelete = self.guildProperties["settings"]["messageProcessing"]["autodelete"]
		self.marketBias = self.guildProperties["settings"]["messageProcessing"]["bias"]

		if str(channelId) in self.overrides:
			self.autodelete = self.overrides[str(channelId)].get("messageProcessing", {}).get("autodelete", self.autodelete)
			self.marketBias = self.overrides[str(channelId)].get("messageProcessing", {}).get("bias", self.marketBias)
	
	# -------------------------
	# Properties
	# -------------------------

	def is_muted(self):
		return False

	def get_limit(self):
		return 30 if self.is_registered() else 10

	
	# -------------------------
	# Charting platforms
	# -------------------------

	def get_platform_order_for(self, commandType):
		if commandType == "charts":
			return (self.accountProperties["settings"]["charts"]["preferredOrder"] if "settings" in self.accountProperties else ["TradingView", "GoCharting", "Finviz", "TradingLite", "Bookmap"]) + ["Alternative.me"]
		elif commandType == "heatmaps":
			if self.marketBias == "traditional":
				return ["Finviz", "Bitgur"]
			else:
				return ["Bitgur", "Finviz"]
		elif commandType == "quotes":
			if self.marketBias == "traditional":
				return ["IEXC", "Alternative.me", "CoinGecko", "CCXT", "Serum", "LLD"]
			else:
				return ["Alternative.me", "CoinGecko", "CCXT", "Serum", "IEXC", "LLD"]
		elif commandType == "details":
			if self.marketBias == "traditional":
				return ["IEXC", "CoinGecko"]
			else:
				return ["CoinGecko", "IEXC"]
		elif commandType == "trades":
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

	def personal_command_presets_available(self):
		return self.is_registered() and (self.is_trialing() or bool(self.accountProperties["customer"]["addons"].get("commandPresets", 0)))

	def personal_flow_available(self):
		return self.is_registered() and (self.is_trialing() or bool(self.accountProperties["customer"]["addons"].get("flow", 0)))

	def personal_statistics_available(self):
		return self.is_registered() and (self.is_trialing() or bool(self.accountProperties["customer"]["addons"].get("statistics", 0)))


	# -------------------------
	# Server properties
	# -------------------------

	def is_serverwide_pro_used(self):
		return self.serverwide_price_alerts_available() or self.serverwide_command_presets_available() or self.serverwide_flow_available() or self.serverwide_statistics_available()

	def serverwide_price_alerts_available(self):
		return self.guildProperties["addons"]["marketAlerts"]["enabled"]

	def serverwide_command_presets_available(self):
		return self.guildProperties["addons"]["commandPresets"]["enabled"]

	def serverwide_flow_available(self):
		return self.guildProperties["addons"]["flow"]["enabled"]

	def serverwide_statistics_available(self):
		return self.guildProperties["addons"]["statistics"]["enabled"]


	# -------------------------
	# Global properties
	# -------------------------

	def price_alerts_available(self):
		return self.serverwide_price_alerts_available() or self.personal_price_alerts_available()
	
	def command_presets_available(self):
		return self.serverwide_command_presets_available() or self.personal_command_presets_available()
	
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
				"commandPresets": {
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
		MessageRequest.__recursive_fill(settings, settingsTemplate)

		return settings

	@staticmethod
	def __recursive_fill(settings, template):
		for e in template:
			if type(template[e]) is dict:
				if e not in settings:
					settings[e] = template[e].copy()
				else:
					MessageRequest.__recursive_fill(settings[e], template[e])
			elif e not in settings:
				settings[e] = template[e]