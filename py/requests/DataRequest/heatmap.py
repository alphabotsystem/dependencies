from sys import maxsize as MAXSIZE
from time import time
from traceback import format_exc

from TickerParser import TickerParser
from .parameter import HeatmapParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1, "1m", ["1", "1m", "1min", "1mins", "1minute", "1minutes", "min"]),
		Parameter(2, "2m", ["2", "2m", "2min", "2mins", "2minute", "2minutes"]),
		Parameter(3, "3m", ["3", "3m", "3min", "3mins", "3minute", "3minutes"]),
		Parameter(5, "5m", ["5", "5m", "5min", "5mins", "5minute", "5minutes"]),
		Parameter(10, "10m", ["10", "10m", "10min", "10mins", "10minute", "10minutes"]),
		Parameter(15, "15m", ["15", "15m", "15min", "15mins", "15minute", "15minutes"], bitgur="last_minute15/"),
		Parameter(20, "20m", ["20", "20m", "20min", "20mins", "20minute", "20minutes"]),
		Parameter(30, "30m", ["30", "30m", "30min", "30mins", "30minute", "30minutes"]),
		Parameter(45, "45m", ["45", "45m", "45min", "45mins", "45minute", "45minutes"]),
		Parameter(60, "1H", ["60", "60m", "60min", "60mins", "60minute", "60minutes", "1", "1h", "1hr", "1hour", "1hours", "hourly", "hour", "hr", "h"], bitgur="last_hour/", tradingViewStockHeatmap="?color=change%7C60", tradingViewCryptoHeatmap="?color=change%7C60"),
		Parameter(120, "2H", ["120", "120m", "120min", "120mins", "120minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2hours"]),
		Parameter(180, "3H", ["180", "180m", "180min", "180mins", "180minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3hours"]),
		Parameter(240, "4H", ["240", "240m", "240min", "240mins", "240minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4hours"], tradingViewStockHeatmap="?color=change%7C240", tradingViewCryptoHeatmap="?color=change%7C240"),
		Parameter(360, "6H", ["360", "360m", "360min", "360mins", "360minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6hours"]),
		Parameter(480, "8H", ["480", "480m", "480min", "480mins", "480minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8hours"]),
		Parameter(720, "12H", ["720", "720m", "720min", "720mins", "720minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12hours"]),
		Parameter(1440, "1D", ["24", "24h", "24hr", "24hrs", "24hour", "24hours", "d", "day", "1", "1d", "1day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440minutes"], bitgur="last_day/", tradingViewStockHeatmap="?color=change", tradingViewCryptoHeatmap="?color=change"),
		Parameter(2880, "2D", ["48", "48h", "48hr", "48hrs", "48hour", "48hours", "2", "2d", "2day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880minutes"]),
		Parameter(3420, "3D", ["72", "72h", "72hr", "72hrs", "72hour", "72hours", "3", "3d", "3day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420minutes"]),
		Parameter(10080, "1W", ["7", "7d", "7day", "7days", "w", "week", "1w", "1week", "weekly"], bitgur="last_week/", tradingViewStockHeatmap="?color=Perf.W", tradingViewCryptoHeatmap="?color=Perf.W"),
		Parameter(20160, "2W", ["14", "14d", "14day", "14days", "2w", "2week"]),
		Parameter(43829, "1M", ["30d", "30day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "monthly"], bitgur="last_month/", tradingViewStockHeatmap="?color=Perf.1M", tradingViewCryptoHeatmap="?color=Perf.1M"),
		Parameter(87658, "2M", ["2", "2m", "2m", "2mo", "2month", "2months"]),
		Parameter(131487, "3M", ["3", "3m", "3m", "3mo", "3month", "3months"], bitgur="last_month3/", tradingViewStockHeatmap="?color=Perf.3M", tradingViewCryptoHeatmap="?color=Perf.3M"),
		Parameter(175316, "4M", ["4", "4m", "4m", "4mo", "4month", "4months"]),
		Parameter(262974, "6M", ["6", "6m", "5m", "6mo", "6month", "6months"], bitgur="last_month6/", tradingViewStockHeatmap="?color=Perf.6M", tradingViewCryptoHeatmap="?color=Perf.6M"),
		Parameter(525949, "1Y", ["12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1y", "y", "annual", "annually"], bitgur="last_year/", tradingViewStockHeatmap="?color=Perf.Y", tradingViewCryptoHeatmap="?color=Perf.Y"),
		Parameter(1051898, "2Y", ["24", "24m", "24mo", "24month", "24months", "2year", "2y"]),
		Parameter(1577847, "3Y", ["36", "36m", "36mo", "36month", "36months", "3year", "3y"]),
		Parameter(2103796, "4Y", ["48", "48m", "48mo", "48month", "48months", "4year", "4y"]),
		Parameter("ytd", "YTD", ["ytd"], tradingViewStockHeatmap="?color=Perf.Y", tradingViewCryptoHeatmap="?color=Perf.Y"),
	],
	"types": [
		Parameter("type", "Nasdaq 100", ["nasdaq", "nasdaq100", "stocks"], tradingViewStockHeatmap="&dataset=NASDAQ100"),
		Parameter("type", "S&P 500", ["s&p500", "s&p", "sp500", "sap500", "sap", "spx", "spx500"], tradingViewStockHeatmap="&dataset=SPX500"),
		Parameter("type", "Dow Jones Composite Average", ["dji", "dowjones", "dowjonescompositeaverage", "djca"], tradingViewStockHeatmap="&dataset=DJCA"),
		Parameter("type", "All US companies", ["alluscompanies", "us", "usa" "uscompanies", "allusa"], tradingViewStockHeatmap="&dataset=AllUSA"),
		Parameter("type", "S&P/ASX 200", ["s&p/asx200", "asx200", "asx", "spasx", "sapasx", "sp200", "sap200"], tradingViewStockHeatmap="&dataset=ASX200"),
		Parameter("type", "All Australian companies", ["allaustraliancompanies", "australiancompanies", "au", "allau"], tradingViewStockHeatmap="&dataset=AllAU"),
		Parameter("type", "BEL 20", ["bel20"], tradingViewStockHeatmap="&dataset=BEL20"),
		Parameter("type", "All Belgian companies", ["allbelgiancompanies", "belgiancompanies", "be", "allbe"], tradingViewStockHeatmap="&dataset=AllBE"),
		Parameter("type", "Shenzhen Component Index", ["shenzhencomponentindex", "sci", "szse399001", "szse"], tradingViewStockHeatmap="&dataset=SZSE399001"),
		Parameter("type", "All Chinese companies", ["allchinesecompanies", "chinesecompanies", "cn", "allcn"], tradingViewStockHeatmap="&dataset=AllCN"),
		Parameter("type", "STOXX 50", ["stoxx50", "sx5e"], tradingViewStockHeatmap="&dataset=SX5E"),
		Parameter("type", "STOXX 600", ["stoxx600", "sxxp"], tradingViewStockHeatmap="&dataset=SXXP"),
		Parameter("type", "All European companies", ["alleuropeancompanies", "europeancompanies", "eu", "alleu"], tradingViewStockHeatmap="&dataset=AllEU"),
		Parameter("type", "OMX HELSINKI 25", ["omxhelsinki25", "omx", "helsinki", "helsinki25"], tradingViewStockHeatmap="&dataset=HELSINKI25"),
		Parameter("type", "All Finnish companies", ["allfinnishcompanies", "fi", "allfi", "finnishcompanies"], tradingViewStockHeatmap="&dataset=AllFI"),
		Parameter("type", "CAC 40", ["cac40", "cac"], tradingViewStockHeatmap="&dataset=CAC40"),
		Parameter("type", "All French companies", ["allfrenchcompanies", "fr", "allfr", "frenchcompanies"], tradingViewStockHeatmap="&dataset=AllFR"),
		Parameter("type", "DAX", ["dax"], tradingViewStockHeatmap="&dataset=DAX"),
		Parameter("type", "MDAX Performance", ["mdax", "mdaxperformance"], tradingViewStockHeatmap="&dataset=MDAX"),
		Parameter("type", "SDAX Performance", ["sdax", "sdaxperformance"], tradingViewStockHeatmap="&dataset=SDAX"),
		Parameter("type", "TECDAX TR", ["tecdax", "tecdaxtr"], tradingViewStockHeatmap="&dataset=TECDAX"),
		Parameter("type", "All German companies", ["allgermancompanies", "de", "allde", "germancompanies"], tradingViewStockHeatmap="&dataset=AllDE"),
		Parameter("type", "NIFTY 50", ["nifty50", "nifty"], tradingViewStockHeatmap="&dataset=NIFTY50"),
		Parameter("type", "S&P BSE SENSEX", ["s&pbsesensex", "sensex"], tradingViewStockHeatmap="&dataset=SENSEX"),
		Parameter("type", "All Indian companies", ["allindiancompanies", "in", "allin", "indiancompanies"], tradingViewStockHeatmap="&dataset=AllIN"),
		Parameter("type", "FTSE MIB INDEX", ["ftsemib", "ftsemibindex", "ftse"], tradingViewStockHeatmap="&dataset=FTSEMIB"),
		Parameter("type", "All Italian companies", ["allitaliancompanies", "it", "allit", "italiancompanies"], tradingViewStockHeatmap="&dataset=AllIT"),
		Parameter("type", "All Malaysian companies", ["allmalaysiancompanies", "my", "allmy", "malaysiancompanies"], tradingViewStockHeatmap="&dataset=AllMY"),
		Parameter("type", "MOEX RUSSIA", ["moex", "moexrussia"], tradingViewStockHeatmap="&dataset=MOEXRUSSIA"),
		Parameter("type", "MOEX BROAD MARKET (RUB)", ["moexrub", "moexbroad"], tradingViewStockHeatmap="&dataset=MOEXBROAD"),
		Parameter("type", "MOEX SMID", ["moexsmid"], tradingViewStockHeatmap="&dataset=MOEXSMID"),
		Parameter("type", "RTS", ["rts"], tradingViewStockHeatmap="&dataset=RTS"),
		Parameter("type", "RTS BROAD MARKET", ["rtsbroad"], tradingViewStockHeatmap="&dataset=RTSBROAD"),
		Parameter("type", "All Russian companies", ["allrussiancompanies", "ru", "allru", "russiancompanies"], tradingViewStockHeatmap="&dataset=AllRU"),
		Parameter("type", "All Spanish companies", ["allspanishcompanies", "es", "alles", "spanishcompanies"], tradingViewStockHeatmap="&dataset=AllES"),
		Parameter("type", "BIST 100", ["bist100"], tradingViewStockHeatmap="&dataset=BIST100"),
		Parameter("type", "BIST TUM", ["bisttum"], tradingViewStockHeatmap="&dataset=BISTTUM"),
		Parameter("type", "All Turkish companies", ["allturkishcompanies", "tr", "alltr", "turkishcompanies"], tradingViewStockHeatmap="&dataset=ALLTR"),
		Parameter("type", "UK 100 Index", ["uk100"], tradingViewStockHeatmap="&dataset=UK100"),
		Parameter("type", "All UK companies", ["allukcompanies", "uk", "alluk", "ukcompanies"], tradingViewStockHeatmap="&dataset=AllUK"),
		Parameter("type", "top100", ["top100", "100top", "100"], bitgur="top100/"),
		Parameter("type", "top10", ["top10", "10top", "10"], bitgur="top10/"),
		Parameter("type", "coins", ["coins", "coin"], bitgur="crypto/"),
		Parameter("type", "token", ["token", "tokens"], bitgur="token/"),
		Parameter("type", "crypto in USD (excluding Bitcoin)", ["cryptoinusd(excludingbitcoin)"], tradingViewCryptoHeatmap="&dataset=CryptoWithoutBTC"),
		Parameter("type", "crypto in BTC", ["cryptoinbtc"], tradingViewCryptoHeatmap="&dataset=CryptoInBTC"),
		Parameter("type", "crypto DeFi", ["cryptodefi"], tradingViewCryptoHeatmap="&dataset=CryptoDeFi"),
		Parameter("type", "crypto in USD", ["full", "all", "every", "everything", "crypto", "cryptoinusd"], bitgur="all/", tradingViewCryptoHeatmap="&dataset=Crypto"),
		Parameter("theme", "light theme", ["light", "white"], tradingViewStockHeatmap="&theme=light", tradingViewCryptoHeatmap="&theme=light"),
		Parameter("theme", "dark theme", ["dark", "black"], tradingViewStockHeatmap="&theme=dark", tradingViewCryptoHeatmap="&theme=dark"),
	],
	"style": [],
	"preferences": [
		Parameter("heatmap", "performance", ["change", "performance"], bitgur="coins/", tradingViewStockHeatmap="performance", tradingViewCryptoHeatmap="performance"),
		Parameter("heatmap", "pre-market change", ["pre-marketchange", "premarketchange", "premarketperformance"], tradingViewStockHeatmap="?color=premarket_change"),
		Parameter("heatmap", "post-market change", ["post-marketchange", "postmarketchange", "postmarketperformance"], tradingViewStockHeatmap="?color=postmarket_change"),
		Parameter("heatmap", "relative volume", ["relativevolume", "volume"], tradingViewStockHeatmap="?color=relative_volume_10d_calc"),
		Parameter("heatmap", "gap", ["gap"], tradingViewStockHeatmap="?color=gap", tradingViewCryptoHeatmap="?color=gap"),
		Parameter("heatmap", "volatility", ["volatility", "vol", "v"], bitgur="volatility/", tradingViewStockHeatmap="?color=Volatility.D", tradingViewCryptoHeatmap="?color=Volatility.D"),
		Parameter("heatmap", "exchanges", ["exchanges", "exchange", "exc", "e"], bitgur="exchanges/"),
		Parameter("heatmap", "trend", ["trend", "tre", "t"], bitgur="trend/"),
		Parameter("heatmap", "category", ["category", "cat", "c"], bitgur="category/"),
		Parameter("heatmap", "unusual", ["unusual", "volume", "unu", "unv", "uvol", "u"], bitgur="unusual_volume/"),
		Parameter("side", "gainers", ["gainers", "gainer", "gain", "g"], bitgur="gainers/"),
		Parameter("side", "losers", ["loosers", "looser", "losers", "loser", "loss", "l"], bitgur="loosers/"),
		Parameter("size", "market cap", ["marketcap", "mcap"], tradingViewStockHeatmap="&size=market_cap_basic", tradingViewCryptoHeatmap="&size=market_cap_calc"),
		Parameter("size", "traded volume", ["tradedvolume", "volume"], tradingViewCryptoHeatmap="&size=total_value_traded"),
		Parameter("size", "number of employees", ["numberofemployees", "employees"], tradingViewStockHeatmap="&size=number_of_employees"),
		Parameter("size", "dividend yield", ["dividendyield", "dividendyield"], tradingViewStockHeatmap="&size=dividend_yield_recent"),
		Parameter("size", "price to earnings ratio (TTM)", ["pricetoearningsratio(ttm)", "pricetoearningsratio", "pricetoearnings"], tradingViewStockHeatmap="&size=price_earnings_ttm"),
		Parameter("size", "price to sales (FY)", ["pricetosales(fy)", "pricetosales"], tradingViewStockHeatmap="&size=price_sales_ratio"),
		Parameter("size", "price to book (FY)", ["pricetobook(fy)", "pricetobook"], tradingViewStockHeatmap="&size=price_book_ratio"),
		Parameter("size", "price to book (MRQ)", ["pricetoboo(mrq)", "mrq"], tradingViewStockHeatmap="&size=price_book_fq"),
		Parameter("group", "no group", ["no group"], tradingViewStockHeatmap="&group=no_group", tradingViewCryptoHeatmap="&group=no_group"),
		Parameter("group", "sector", ["sector"], tradingViewStockHeatmap="&group=sector"),
		Parameter("category", "market cap", ["marketcap", "mcap"], bitgur="cap"),
		Parameter("category", "cryptocurrency", ["cryptocurrency", "crypto"], bitgur="cryptocurrency"),
		Parameter("category", "blockchain platforms", ["blockchain", "platforms"], bitgur="blockchain_platforms"),
		Parameter("category", "commerce and advertising", ["commerce", "advertising"], bitgur="commerce_and_advertising"),
		Parameter("category", "commercial services", ["commercialservices"], tradingViewStockHeatmap="&activeGroup=Commercial%20Services"),
		Parameter("category", "commodities", ["commodities"], bitgur="commodities"),
		Parameter("category", "communications", ["communications"], tradingViewStockHeatmap="&activeGroup=Communications"),
		Parameter("category", "consumer durables", ["consumerdurables"], tradingViewStockHeatmap="&activeGroup=Consumer%20Durables"),
		Parameter("category", "consumer non-durables", ["consumernon-durables"], tradingViewStockHeatmap="&activeGroup=Consumer%20Non-Durables"),
		Parameter("category", "consumer services", ["consumerservices"], tradingViewStockHeatmap="&activeGroup=Consumer%20Services"),
		Parameter("category", "content management", ["content", "management"], bitgur="content_management"),
		Parameter("category", "data storage and AI", ["data", "storage", "analytics", "ai"], bitgur="data_storage_analytics_and_ai"),
		Parameter("category", "distribution services", ["distributionservices"], tradingViewStockHeatmap="&activeGroup=Distribution%20Services"),
		Parameter("category", "drugs and healthcare", ["health", "drugs", "healthcare"], bitgur="drugs_and_healthcare"),
		Parameter("category", "energy and utilities", ["energy", "utilities"], bitgur="energy_and_utilities"),
		Parameter("category", "electronic technology", ["electronictechnology"], tradingViewStockHeatmap="&activeGroup=Electronic%20Technology"),
		Parameter("category", "events and entertainment", ["events", "entertainment"], bitgur="events_and_entertainment"),
		Parameter("category", "energy minerals", ["energyminerals"], tradingViewStockHeatmap="&activeGroup=Energy%20Minerals"),
		Parameter("category", "finance", ["finance", "financialservices"], bitgur="financial_services", tradingViewStockHeatmap="&activeGroup=Finance"),
		Parameter("category", "gambling and betting", ["gambling", "betting"], bitgur="gambling_and_betting"),
		Parameter("category", "gaming and VR", ["gaming", "vr"], bitgur="gaming_and_vr"),
		Parameter("category", "health services", ["healthservices"], tradingViewStockHeatmap="&activeGroup=Health%20Services"),
		Parameter("category", "health technology", ["health", "healthtechnology", "healthcare"], tradingViewStockHeatmap="&activeGroup=Health%20Technology"),
		Parameter("category", "identy and reputation", ["identy", "reputation"], bitgur="identy_and_reputation"),
		Parameter("category", "industrial services", ["industrialservices"], tradingViewStockHeatmap="&activeGroup=Industrial%20Services"),
		Parameter("category", "legal", ["legal"], bitgur="legal"),
		Parameter("category", "miscellaneous", ["miscellaneous"], tradingViewStockHeatmap="&activeGroup=Miscellaneous"),
		Parameter("category", "non-energy minerals", ["non-energyminerals"], tradingViewStockHeatmap="&activeGroup=Non-Energy%20Minerals"),
		Parameter("category", "process industries", ["processindustries"], tradingViewStockHeatmap="&activeGroup=Process%20Industries"),
		Parameter("category", "producer manufacturing", ["producermanufacturing"], tradingViewStockHeatmap="&activeGroup=Producer%20Manufacturing"),
		Parameter("category", "real estate", ["real", "estate"], bitgur="real_estate"),
		Parameter("category", "retail trade", ["retailtrade"], tradingViewStockHeatmap="&activeGroup=Retail%20Trade"),
		Parameter("category", "social network", ["social", "network"], bitgur="social_network"),
		Parameter("category", "software", ["software"], bitgur="software"),
		Parameter("category", "supply and logistics", ["supply", "logistics"], bitgur="supply_and_logistics"),
		Parameter("category", "technology services", ["technologyservices"], tradingViewStockHeatmap="&activeGroup=Technology%20Services"),
		Parameter("category", "trading and investing", ["trading", "investing"], bitgur="trading_and_investing"),
		Parameter("category", "transportation", ["transportation"], tradingViewStockHeatmap="&activeGroup=Transportation"),
		Parameter("category", "utilities", ["utilities"], tradingViewStockHeatmap="&activeGroup=Utilities"),
		Parameter("forcePlatform", "force heat map on Bitgur", ["bg", "bitgur"], bitgur=True),
		Parameter("force", "force", ["--force"], tradingViewStockHeatmap="force", tradingViewCryptoHeatmap="force", bitgur="force"),
		Parameter("upload", "upload", ["--upload"], tradingViewStockHeatmap="upload", tradingViewCryptoHeatmap="upload", bitgur="upload")
	]
}
DEFAULTS = {
	"TradingView Stock Heatmap": {
		"timeframes": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("type", name="S&P 500", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"TradingView Crypto Heatmap": {
		"timeframes": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("type", name="crypto in USD", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Bitgur": {
		"timeframes": [],
		"types": [],
		"style": [],
		"preferences": []
	}
}


class HeatmapRequestHandler(AbstractRequestHandler):
	def __init__(self, platforms, bias="traditional"):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = HeatmapRequest(platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			_argument = argument.lower().replace(" ", "")
			if request.errorIsFatal or argument == "": continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			outputMessage, success = await request.add_timeframe(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_type(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_style(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_preferences(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			if finalOutput is None:
				request.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
			elif finalOutput.startswith("`Force Heat Map"):
				request.set_error(None, isFatal=True)
			else:
				request.set_error(finalOutput)

	async def process_ticker(self): raise NotImplementedError

	def set_defaults(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue
			for type in PARAMETERS:
				request.set_default_for(type)

	async def find_caveats(self):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			types = [{"id": e.id, "value": e.parsed[platform]} for e in request.types]
			preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]

			if platform == "TradingView Stock Heatmap":
				heatmap = [e.get("value") for e in preferences if e.get("id") == "heatmap"]
				size = [e.get("value") for e in preferences if e.get("id") == "size"]
				group = [e.get("value") for e in preferences if e.get("id") == "group"]

				theme = [e.get("value") for e in types if e.get("id") == "theme"]
				_type = [e.get("value") for e in types if e.get("id") == "type"]

				if "performance" not in heatmap and any([e in heatmap for e in ["?color=premarket_change", "?color=postmarket_change", "?color=relative_volume_10d_calc", "?color=gap", "?color=Volatility.D"]]):
					if request.timeframes[0].id is not None: request.set_error(f"Timeframes are not supported on the {heatmap[:-1]} heat map.")
				elif len(request.timeframes) == 0:
					request.timeframes = [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)]
					if "performance" not in heatmap:
						request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="performance", type="preferences", params=PARAMETERS))

				if len(size) == 0:
					request.preferences.append(AbstractRequest.find_parameter_with_id("size", name="market cap", type="preferences", params=PARAMETERS))
				if len(group) == 0:
					request.preferences.append(AbstractRequest.find_parameter_with_id("group", name="sector", type="preferences", params=PARAMETERS))

				if len(theme) == 0:
					request.types.append(AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="types", params=PARAMETERS))
				if len(_type) == 0:
					request.types.append(AbstractRequest.find_parameter_with_id("type", name="S&P 500", type="types", params=PARAMETERS))
			elif platform == "TradingView Crypto Heatmap":
				heatmap = [e.get("value") for e in preferences if e.get("id") == "heatmap"]
				size = [e.get("value") for e in preferences if e.get("id") == "size"]
				group = [e.get("value") for e in preferences if e.get("id") == "group"]

				theme = [e.get("value") for e in types if e.get("id") == "theme"]
				_type = [e.get("value") for e in types if e.get("id") == "type"]

				if "performance" not in heatmap and any([e in heatmap for e in ["?color=gap", "?color=Volatility.D"]]):
					if request.timeframes[0].id is not None: request.set_error(f"Timeframes are not supported on the {heatmap[:-1]} heat map.")
				elif len(request.timeframes) == 0:
					request.timeframes = [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)]
					if "performance" not in heatmap:
						request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="performance", type="preferences", params=PARAMETERS))

				if len(size) == 0:
					request.preferences.append(AbstractRequest.find_parameter_with_id("size", name="market cap", type="preferences", params=PARAMETERS))
				if len(group) == 0:
					request.preferences.append(AbstractRequest.find_parameter_with_id("group", name="no group", type="preferences", params=PARAMETERS))

				if len(theme) == 0:
					request.types.append(AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="types", params=PARAMETERS))
				if len(_type) == 0:
					request.types.append(AbstractRequest.find_parameter_with_id("type", name="crypto in USD", type="types", params=PARAMETERS))
			elif platform == "Bitgur":
				for _ in range(8):
					preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]
					heatmap = [e.get("value") for e in preferences if e.get("id") == "heatmap"]
					side = [e.get("value") for e in preferences if e.get("id") == "side"]
					category = [e.get("value") for e in preferences if e.get("id") == "category"]

					# Add default heat map style
					if len(heatmap) == 0:
						if len(side) != 0: request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="trend", type="preferences", params=PARAMETERS)); continue
						elif len(category) != 0: request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="category", type="preferences", params=PARAMETERS)); continue
						else: request.preferences.append(AbstractRequest.find_parameter_with_id("heatmap", name="performance", type="preferences", params=PARAMETERS)); continue

					# Timeframes are not supported on some heat map types
					[heatmap] = heatmap
					if heatmap in ["exchanges/", "volatility/", "unusual_volume/"]:
						if len(request.timeframes) != 0:
							if request.timeframes[0].id is not None: request.set_error(f"Timeframes are not supported on the {heatmap[:-1]} heat map."); break
						else:
							request.timeframes = [Parameter(None, None, None, bitgur="")]; continue
					elif len(request.timeframes) == 0:
						request.timeframes = [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)]; continue

					# Category heat map checks
					if heatmap in ["category/"]:
						if len(category) == 0: request.set_error("Missing category."); break

					if heatmap in ["coins/", "trend/"]:
						if len(category) == 0 and len(types) != 0: request.preferences.append(AbstractRequest.find_parameter_with_id("category", name="market cap", type="preferences", params=PARAMETERS)); continue

					if heatmap in ["exchanges/", "category/"]:
						if len(types) != 0: request.set_error(f"Types are not supported on the {heatmap[:-1]} heat map."); break
					elif len(types) == 0:
						request.preferences.append(AbstractRequest.find_parameter_with_id("type", name="crypto in USD", type="types", params=PARAMETERS)); continue

					if heatmap in ["coins/", "exchanges/", "category/", "volatility/", "unusual_volume/"]:
						if len(side) != 0: request.set_error(f"Top gainers/losers are not supported on the {heatmap[:-1]} heat map."); break
					elif len(side) == 0:
						request.preferences.append(AbstractRequest.find_parameter_with_id("side", name="gainers", type="preferences", params=PARAMETERS)); continue

					break


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		timeframes = []

		for platform in self.platforms:
			request = self.requests[platform].to_dict()
			timeframes.append(request.get("timeframes"))
			d[platform] = request

		d["timeframes"] = {p: t for p, t in zip(self.platforms, timeframes)}
		d["requestCount"] = len(d["timeframes"][d.get("currentPlatform")])

		return d


class HeatmapRequest(AbstractRequest):
	def __init__(self, platform, bias):
		super().__init__(platform, bias)

		self.timeframes = []
		self.types = []
		self.styles = []
		self.preferences = []

		self.currentTimeframe = None

	def add_parameter(self, argument, type):
		isSupported = None
		parsedParameter = None
		for param in PARAMETERS[type]:
			if argument in param.parsablePhrases:
				parsedParameter = param
				isSupported = param.supports(self.platform)
				if isSupported: break
		return isSupported, parsedParameter

	# async def add_timeframe(self, argument) -- inherited

	async def add_exchange(self, argument): raise NotImplementedError

	async def add_type(self, argument):
		heatmapStyleSupported, parsedHeatmapStyle = self.add_parameter(argument, "types")
		if parsedHeatmapStyle is not None and not self.has_parameter(parsedHeatmapStyle.id, self.types):
			if not heatmapStyleSupported:
				outputMessage = f"`{parsedHeatmapStyle.name.title()}` heat map style is not supported on {self.platform}."
				return outputMessage, False
			self.types.append(parsedHeatmapStyle)
			return None, True
		return None, None

	# async def add_style(self, argument) -- inherited

	# async def add_preferences(self, argument) -- inherited

	def set_default_for(self, t):
		if t == "timeframes" and len(self.timeframes) == 0:
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.timeframes): self.timeframes.append(parameter)
		elif t == "types":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.types): self.types.append(parameter)
		elif t == "style":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.styles): self.styles.append(parameter)
		elif t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)


	def to_dict(self):
		d = {
			"parserBias": self.parserBias,
			"timeframes": [e.parsed[self.platform] for e in self.timeframes],
			"types": "".join([e.parsed[self.platform] for e in self.types]),
			"styles": [e.parsed[self.platform] for e in self.styles],
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences],
			"currentTimeframe": self.currentTimeframe
		}
		return d