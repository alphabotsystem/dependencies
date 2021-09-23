from os import environ
from sys import maxsize as MAXSIZE
from time import time
from re import search
from traceback import format_exc

from TickerParserPy import TickerParser, Exchange
from .parameter import ChartParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1, "1m", ["1", "1m", "1min", "1mins", "1minute", "1minutes", "min", "m"], tradinglite="1", tradingview="1", gocharting="1m"),
		Parameter(2, "2m", ["2", "2m", "2min", "2mins", "2minute", "2minutes"]),
		Parameter(3, "3m", ["3", "3m", "3min", "3mins", "3minute", "3minutes"], tradinglite="3", tradingview="3", gocharting="3m"),
		Parameter(4, "4m", ["4", "4m", "4min", "4mins", "4minute", "4minutes"]),
		Parameter(5, "5m", ["5", "5m", "5min", "5mins", "5minute", "5minutes"], tradinglite="5", tradingview="5", gocharting="5m"),
		Parameter(6, "6m", ["6", "6m", "6min", "6mins", "6minute", "6minutes"]),
		Parameter(10, "10m", ["10", "10m", "10min", "10mins", "10minute", "10minutes"], bookmap="bm-btn-time-frame-10m"),
		Parameter(15, "15m", ["15", "15m", "15min", "15mins", "15minute", "15minutes"], tradinglite="15", tradingview="15", gocharting="15m"),
		Parameter(20, "20m", ["20", "20m", "20min", "20mins", "20minute", "20minutes"]),
		Parameter(30, "30m", ["30", "30m", "30min", "30mins", "30minute", "30minutes"], tradinglite="30", tradingview="30", gocharting="30m"),
		Parameter(45, "45m", ["45", "45m", "45min", "45mins", "45minute", "45minutes"], tradingview="45"),
		Parameter(60, "1H", ["60", "60m", "60min", "60mins", "60minute", "60minutes", "1", "1h", "1hr", "1hour", "1hours", "hourly", "hour", "hr", "h"], tradinglite="60", tradingview="60", bookmap="bm-btn-time-frame-1h", gocharting="1h"),
		Parameter(120, "2H", ["120", "120m", "120min", "120mins", "120minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2hours"], tradinglite="120", tradingview="120", gocharting="2h"),
		Parameter(180, "3H", ["180", "180m", "180min", "180mins", "180minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3hours"], tradingview="180"),
		Parameter(240, "4H", ["240", "240m", "240min", "240mins", "240minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4hours"], tradinglite="240", tradingview="240", gocharting="4h"),
		Parameter(360, "6H", ["360", "360m", "360min", "360mins", "360minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6hours"], tradinglite="360"),
		Parameter(480, "8H", ["480", "480m", "480min", "480mins", "480minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8hours"], tradinglite="480"),
		Parameter(720, "12H", ["720", "720m", "720min", "720mins", "720minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12hours"], tradinglite="720", gocharting="12h"),
		Parameter(1440, "1D", ["24", "24h", "24hr", "24hrs", "24hour", "24hours", "d", "day", "1", "1d", "1day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440minutes"], tradinglite="1440", tradingview="D", bookmap="bm-btn-time-frame-1d", gocharting="1D", finviz="d", alphaflow="yesterday"),
		Parameter(2880, "2D", ["48", "48h", "48hr", "48hrs", "48hour", "48hours", "2", "2d", "2day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880minutes"]),
		Parameter(3420, "3D", ["72", "72h", "72hr", "72hrs", "72hour", "72hours", "3", "3d", "3day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420minutes"]),
		Parameter(5760, "4D", ["96", "96h", "96hr", "96hrs", "96hour", "96hours", "4", "4d", "4day", "5760", "5760m", "5760min", "5760mins", "5760minute", "5760minutes"]),
		Parameter(7200, "5D", ["120", "120h", "120hr", "120hrs", "120hour", "120hours", "5", "5d", "5day", "7200", "7200m", "7200min", "7200mins", "7200minute", "7200minutes"]),
		Parameter(8640, "6D", ["144", "144h", "144hr", "144hrs", "144hour", "144hours", "4", "4d", "4day", "8640", "8640m", "8640min", "8640mins", "8640minute", "8640minutes"]),
		Parameter(10080, "1W", ["7", "7d", "7day", "7days", "w", "week", "1w", "1week", "weekly"], tradingview="W", bookmap="bm-btn-time-frame-1W", gocharting="1W", finviz="w", alphaflow="lastweek"),
		Parameter(20160, "2W", ["14", "14d", "14day", "14days", "2w", "2week"]),
		Parameter(30240, "3W", ["21", "21d", "21day", "21days", "3w", "3week"]),
		Parameter(43829, "1M", ["30d", "30day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "monthly"], tradingview="M", bookmap="bm-btn-time-frame-1Mo", gocharting="1M", finviz="m"),
		Parameter(87658, "2M", ["2", "2m", "2m", "2mo", "2month", "2months"]),
		Parameter(131487, "3M", ["3", "3m", "3m", "3mo", "3month", "3months"]),
		Parameter(175316, "4M", ["4", "4m", "4m", "4mo", "4month", "4months"]),
		Parameter(262974, "6M", ["6", "6m", "5m", "6mo", "6month", "6months"]),
		Parameter(525949, "1Y", ["12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1y", "y", "annual", "annually"]),
		Parameter(1051898, "2Y", ["24", "24m", "24mo", "24month", "24months", "2year", "2y"]),
		Parameter(1577847, "3Y", ["36", "36m", "36mo", "36month", "36months", "3year", "3y"]),
		Parameter(2103796, "4Y", ["48", "48m", "48mo", "48month", "48months", "4year", "4y"]),
		Parameter(2628000, "5Y", ["60", "60m", "60mo", "60month", "60months", "5year", "5y"])
	],
	"indicators": [
		Parameter("ab", "Abandoned Baby", ["ab", "abandonedbaby"], gocharting="ABANDONEDBABY"),
		Parameter("accd", "Accumulation/Distribution", ["accd", "accumulationdistribution", "ad", "acc"], tradingview="ACCD@tv-basicstudies", gocharting="ACC", dynamic={"GoCharting": [20]}),
		Parameter("accumulationswingindex", "Accumulation Swing Index", ["accumulationswingindex", "accsi", "asi"], gocharting="ACCSWINGINDEX"),
		Parameter("admi", "Average Directional Movement Index", ["admi", "adx"], gocharting="ADX", dynamic={"GoCharting": [20]}),
		Parameter("adr", "ADR", ["adr"], tradingview="studyADR@tv-basicstudies"),
		Parameter("alligator", "Alligator", ["alligator"], gocharting="ALLIGATOR"),
		Parameter("aroon", "Aroon", ["aroon"], tradingview="AROON@tv-basicstudies", gocharting="AROON", dynamic={"GoCharting": [20]}),
		Parameter("aroonoscillator", "Aroon Oscillator", ["aroonoscillator"], gocharting="AROONOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("atr", "ATR", ["atr"], tradingview="ATR@tv-basicstudies", gocharting="ATR", dynamic={"GoCharting": [20]}),
		Parameter("atrb", "ATR Bands", ["atrb"], gocharting="ATRBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("atrts", "ATR Trailing Stop", ["trailingstop", "atrts", "atrstop", "atrs"], gocharting="ATRTRAILINGSTOP", dynamic={"GoCharting": [14, 2]}),
		Parameter("awesome", "Awesome Oscillator", ["awesome", "ao"], tradingview="AwesomeOscillator@tv-basicstudies", gocharting="AWESOMEOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("balanceofpower", "Balance of Power", ["balanceofpower", "bop"], gocharting="BOP", dynamic={"GoCharting": [20]}),
		Parameter("bearish", "All Bearish Candlestick Patterns", ["bear", "bearish", "bearishpatterns", "bp"], gocharting="BEARISH"),
		Parameter("bearishengulfing", "Bearish Engulfing Pattern", ["bearishengulfing"], gocharting="BEARISHENGULFINGPATTERN"),
		Parameter("bearishhammer", "Bearish Hammer Pattern", ["bearishhammer"], gocharting="BEARISHHAMMER"),
		Parameter("bearishharami", "Bearish Harami Pattern", ["bearishharami"], gocharting="BEARISHHARAMI"),
		Parameter("bearishharamicross", "Bearish Harami Cross Pattern", ["bearishharamicross"], gocharting="BEARISHHARAMICROSS"),
		Parameter("bearishinvertedhammer", "Bearish Inverted Hammer", ["bearishinvertedhammer"], gocharting="BEARISHINVERTEDHAMMER"),
		Parameter("bearishmarubozu", "Bearish Marubozu Pattern", ["bearishmarubozu"], gocharting="BEARISHMARUBOZU"),
		Parameter("bearishspinningtop", "Bearish Spinning Top Pattern", ["bearishspinningtop"], gocharting="BEARISHSPINNINGTOP"),
		Parameter("width", "Bollinger Bands Width", ["width", "bbw"], tradingview="BollingerBandsWidth@tv-basicstudies"),
		Parameter("bullish", "All Bullish Candlestick Patterns", ["bull", "bullish", "bullishpatterns", "bp"], gocharting="BULLISH"),
		Parameter("bullishengulfing", "Bullish Engulfing Pattern", ["bullishengulfing"], gocharting="BULLISHENGULFINGPATTERN"),
		Parameter("bullishhammer", "Bullish Hammer Pattern", ["bullishhammer"], gocharting="BULLISHHAMMER"),
		Parameter("bullishharami", "Bullish Harami Pattern", ["bullishharami"], gocharting="BULLISHHARAMI"),
		Parameter("bullishharamicross", "Bullish Harami Cross Pattern", ["bullishharamicross"], gocharting="BULLISHHARAMICROSS"),
		Parameter("bullishinvertedhammer", "Bullish Inverted Hammer Pattern", ["bullishinvertedhammer"], gocharting="BULLISHINVERTEDHAMMER"),
		Parameter("bullishmarubozu", "Bullish Marubozu Pattern", ["bullishmarubozu"], gocharting="BULLISHMARUBOZU"),
		Parameter("bullishspinningtop", "Bullish Spinning Top Pattern", ["bullishspinningtop"], gocharting="BULLISHSPINNINGTOP"),
		Parameter("bollinger", "Bollinger Bands", ["bollinger", "bbands", "bb"], tradingview="BB@tv-basicstudies", gocharting="BOLLINGERBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("cmf", "Chaikin Money Flow Index", ["cmf"], tradingview="CMF@tv-basicstudies", gocharting="CHAIKINMFI", dynamic={"GoCharting": [20]}),
		Parameter("chaikin", "Chaikin Oscillator", ["chaikin", "co"], tradingview="ChaikinOscillator@tv-basicstudies"),
		Parameter("cv", "Chaikin Volatility", ["cv", "chaikinvolatility"], gocharting="CHAIKINVOLATILITY"),
		Parameter("cf", "Chande Forecast", ["cf", "chandeforecast"], gocharting="CHANDEFORECAST", dynamic={"GoCharting": [20]}),
		Parameter("chande", "Chande MO", ["chande", "cmo"], tradingview="chandeMO@tv-basicstudies", gocharting="CMO", dynamic={"GoCharting": [20]}),
		Parameter("choppiness", "Choppiness Index", ["choppiness", "ci"], tradingview="ChoppinessIndex@tv-basicstudies", gocharting="CHOPPINESS"),
		Parameter("cci", "CCI", ["cci"], tradingview="CCI@tv-basicstudies", gocharting="CCI", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("crsi", "CRSI", ["crsi"], tradingview="CRSI@tv-basicstudies"),
		Parameter("cog", "Center of Gravity", ["cog"], gocharting="COG", dynamic={"GoCharting": [20]}),
		Parameter("coppock", "Coppock", ["coppock"], gocharting="COPPOCK"),
		Parameter("cumtick", "Cumulative Tick", ["cumtick"], gocharting="CUMTICK", dynamic={"GoCharting": [20]}),
		Parameter("correlation", "Correlation Coefficient", ["correlation", "cc"], tradingview="CorrelationCoefficient@tv-basicstudies"),
		Parameter("darkcloudcoverpattern", "Dark Cloud Cover Pattern", ["darkcloudcover", "dccp"], gocharting="DARKCLOUDCOVER"),
		Parameter("detrended", "Detrended Price Oscillator", ["detrended", "dpo"], tradingview="DetrendedPriceOscillator@tv-basicstudies", gocharting="DPO", dynamic={"GoCharting": [20]}),
		Parameter("disparityoscillator", "Disparity Oscillator", ["disparityoscillator"], gocharting="DISPARITY", dynamic={"GoCharting": [20]}),
		Parameter("donchainwidth", "Donchain Width", ["donchainwidth"], gocharting="DONCHIANWIDTH", dynamic={"GoCharting": [20]}),
		Parameter("dm", "DM", ["dm", "directional"], tradingview="DM@tv-basicstudies"),
		Parameter("dojipattern", "Doji Pattern", ["doji"], gocharting="DOJI"),
		Parameter("donch", "DONCH", ["donch", "donchainchannel"], tradingview="DONCH@tv-basicstudies", gocharting="DONCHIANCHANNEL", dynamic={"GoCharting": [14, 2]}),
		Parameter("downsidetasukigappattern", "Downside Tasuki Gap Pattern", ["downsidetasukigap", "dtgp"], gocharting="DOWNSIDETASUKIGAP"),
		Parameter("dema", "Double EMA", ["dema", "2ema"], tradingview="DoubleEMA@tv-basicstudies", gocharting="DEMA", dynamic={"GoCharting": [20]}),
		Parameter("dragonflydojipattern", "Dragonfly Doji Pattern", ["dragonflydoji", "ddp"], gocharting="DRAGONFLYDOJI"),
		Parameter("efi", "EFI", ["efi"], tradingview="EFI@tv-basicstudies"),
		Parameter("ema", "EMA", ["ema"], tradingview="MAExp@tv-basicstudies", gocharting="EMA", dynamic={"GoCharting": [20]}),
		Parameter("elderray", "Elder Ray", ["elderray"], gocharting="ELDERRAY"),
		Parameter("elliott", "Elliott Wave", ["elliott", "ew"], tradingview="ElliottWave@tv-basicstudies"),
		Parameter("env", "ENV", ["env"], tradingview="ENV@tv-basicstudies"),
		Parameter("eom", "Ease of Movement", ["eom"], tradingview="EaseOfMovement@tv-basicstudies", gocharting="EOM", dynamic={"GoCharting": [20]}),
		Parameter("eveningdojistarpattern", "Evening Doji Star Pattern", ["eveningdojistar", "edsp"], gocharting="EVENINGDOJISTAR"),
		Parameter("eveningstarpattern", "Evening Star Pattern", ["eveningstar", "esp"], gocharting="EVENINGSTAR"),
		Parameter("fisher", "Fisher Transform", ["fisher", "ft"], tradingview="FisherTransform@tv-basicstudies", gocharting="EHLERFISHERTRANSFORM", dynamic={"GoCharting": [20]}),
		Parameter("forceindex", "Force Index", ["forceindex"], gocharting="FORCEINDEX"),
		Parameter("fullstochasticoscillator", "Full Stochastic Oscillator", ["fso"], gocharting="FULLSTOCHASTICOSCILLATOR"),
		Parameter("gravestonedojipattern", "Gravestone Doji Pattern", ["gravestonedoji", "gd"], gocharting="GRAVESTONEDOJI"),
		Parameter("gatoroscillator", "Gator Oscillator", ["gatoroscillator", "gatoro"], gocharting="GATOROSCILLATOR"),
		Parameter("gopalakrishnanrangeindex", "Gopalakrishnan Range Index", ["gopalakrishnanrangeindex", "gri", "gapo"], gocharting="GAPO", dynamic={"GoCharting": [20]}),
		Parameter("guppy", "Guppy Moving Average", ["guppy", "gma", "rainbow", "rma"], gocharting="GUPPY", dynamic={"GoCharting": [20]}),
		Parameter("guppyoscillator", "Guppy Oscillator", ["guppyoscillator", "guppyo", "rainbowoscillator", "rainbowo"], gocharting="GUPPYOSCILLATOR"),
		Parameter("hangmanpattern", "Hangman Pattern", ["hangman", "hangingman"], gocharting="HANGINGMAN"),
		Parameter("hhv", "High High Volume", ["highhighvolume", "hhv"], gocharting="HHV", dynamic={"GoCharting": [20]}),
		Parameter("hml", "High Minus Low", ["highminuslow", "hml"], gocharting="HIGHMINUSLOW"),
		Parameter("hv", "HV", ["historicalvolatility", "hv"], tradingview="HV@tv-basicstudies", gocharting="HISTVOLATILITY"),
		Parameter("hull", "Hull MA", ["hull", "hma"], tradingview="hullMA@tv-basicstudies", gocharting="HULL"),
		Parameter("ichimoku", "Ichimoku Cloud", ["ichimoku", "cloud", "ichi", "ic"], tradingview="IchimokuCloud@tv-basicstudies", gocharting="ICHIMOKU"),
		Parameter("imi", "Intraday Momentum Index", ["intradaymomentumindex", "imi", "intradaymi"], gocharting="INTRADAYMI", dynamic={"GoCharting": [20]}),
		Parameter("keltner", "KLTNR", ["keltner", "kltnr"], tradingview="KLTNR@tv-basicstudies", gocharting="KELTNERCHANNEL", dynamic={"GoCharting": [14, 2]}),
		Parameter("klinger", "Klinger", ["klinger"], gocharting="KLINGER"),
		Parameter("kst", "Know Sure Thing", ["knowsurething", "kst"], gocharting="KST"),
		Parameter("kst", "KST", ["kst"], tradingview="KST@tv-basicstudies"),
		Parameter("llv", "Lowest Low Volume", ["llv", "lowestlowvolume"], gocharting="LLV", dynamic={"GoCharting": [20]}),
		Parameter("regression", "Linear Regression", ["regression", "lr", "linreg"], tradingview="LinearRegression@tv-basicstudies"),
		Parameter("macd", "MACD", ["macd"], tradingview="MACD@tv-basicstudies", gocharting="MACD"),
		Parameter("massindex", "Mass Index", ["massindex", "mi"], gocharting="MASSINDEX"),
		Parameter("medianprice", "Median Price", ["medianprice", "mp"], gocharting="MP", dynamic={"GoCharting": [20]}),
		Parameter("mom", "Momentum", ["mom", "momentum"], tradingview="MOM@tv-basicstudies", gocharting="MOMENTUMINDICATOR", dynamic={"GoCharting": [20]}),
		Parameter("morningdojistarpattern", "Morning Doji Star Pattern", ["morningdojistar", "mds"], gocharting="MORNINGDOJISTAR"),
		Parameter("morningstarpattern", "Morning Star Pattern", ["morningstar", "ms"], gocharting="MORNINGSTAR"),
		Parameter("mf", "Money Flow", ["mf", "mfi"], tradingview="MF@tv-basicstudies", gocharting="MONEYFLOWINDEX", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("moon", "Moon Phases", ["moon"], tradingview="MoonPhases@tv-basicstudies", gocharting="MOONPHASE"),
		Parameter("ma", "Moving Average", ["ma", "sma"], tradingview="MASimple@tv-basicstudies", gocharting="SMA", dynamic={"GoCharting": [20]}),
		Parameter("maenvelope", "Moving Average Envelope", ["maenvelope", "mae"], gocharting="MAENVELOPE", dynamic={"GoCharting": [14, 2]}),
		Parameter("nvi", "Negative Volume Index", ["nvi", "negvolindex", "negativevolumeindex"], gocharting="NEGVOLINDEX"),
		Parameter("obv", "On Balance Volume", ["obv"], tradingview="OBV@tv-basicstudies", gocharting="ONBALANCEVOLUME", dynamic={"GoCharting": [20]}),
		Parameter("parabolic", "PSAR", ["parabolic", "sar", "psar"], tradingview="PSAR@tv-basicstudies", gocharting="SAR"),
		Parameter("performanceindex", "Performance Index", ["performanceindex", "pi"], gocharting="PERFORMANCEINDEX"),
		Parameter("pgo", "Pretty Good Oscillator", ["prettygoodoscillator", "pgo"], gocharting="PRETTYGOODOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("piercinglinepattern", "Piercing Line Pattern", ["piercingline", "pl"], gocharting="PIERCINGLINE"),
		Parameter("pmo", "Price Momentum Oscillator", ["pmo", "pricemomentum"], gocharting="PMO"),
		Parameter("po", "Price Oscillator", ["po", "price"], tradingview="PriceOsc@tv-basicstudies", gocharting="PRICEOSCILLATOR"),
		Parameter("pphl", "Pivot Points High Low", ["pphl"], tradingview="PivotPointsHighLow@tv-basicstudies"),
		Parameter("pps", "Pivot Points Standard", ["pps", "pivot"], tradingview="PivotPointsStandard@tv-basicstudies", gocharting="PIVOTPOINTS"),
		Parameter("primenumberbands", "Prime Number Bands", ["primenumberbands", "pnb"], gocharting="PRIMENUMBERBANDS", dynamic={"GoCharting": [14, 2]}),
		Parameter("primenumberoscillator", "Prime Number Oscillator", ["primenumberoscillator", "pno"], gocharting="PRIMENUMBEROSCILLATOR"),
		Parameter("psychologicalline", "Psychological Line", ["psychologicalline", "psy", "psychological"], gocharting="PSY", dynamic={"GoCharting": [20]}),
		Parameter("pvi", "Positive Volume Index", ["pvi", "positivevolumeindex", "posvolindex"], gocharting="POSVOLINDEX"),
		Parameter("pvt", "Price Volume Trend", ["pvt"], tradingview="PriceVolumeTrend@tv-basicstudies"),
		Parameter("qstickindicator", "Qstick Indicator", ["qstickindicator", "qi", "qsticks"], gocharting="QSTICKS", dynamic={"GoCharting": [20]}),
		Parameter("randomwalk", "Random Walk", ["randomwalk", "ra"], gocharting="RANDOMWALK", dynamic={"GoCharting": [20]}),
		Parameter("ravi", "Ravi Oscillator", ["ravi"], gocharting="RAVI"),
		Parameter("rvi", "Relative Volatility", ["rvi"], gocharting="RELATIVEVOLATILITY"),
		Parameter("roc", "Price ROC", ["roc", "priceroc", "proc"], tradingview="ROC@tv-basicstudies", gocharting="PRICEROC", dynamic={"GoCharting": [20]}),
		Parameter("rsi", "RSI", ["rsi"], tradingview="RSI@tv-basicstudies", gocharting="RSI", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("schaff", "Schaff", ["schaff"], gocharting="SCHAFF"),
		Parameter("shinohara", "Shinohara", ["shinohara", "shin"], gocharting="SHINOHARA", dynamic={"GoCharting": [20]}),
		Parameter("shootingstarpattern", "Shooting Star Pattern", ["shootingstar", "ss"], gocharting="SHOOTINGSTAR"),
		Parameter("smiei", "SMI Ergodic Indicator", ["smiei"], tradingview="SMIErgodicIndicator@tv-basicstudies"),
		Parameter("smieo", "SMI Ergodic Oscillator", ["smieo"], tradingview="SMIErgodicOscillator@tv-basicstudies"),
		Parameter("stdev", "Standard Deviation", ["stdev", "stddev", "standarddeviation"], gocharting="SD"),
		Parameter("stochastic", "Stochastic", ["stochastic", "stoch"], tradingview="Stochastic@tv-basicstudies"),
		Parameter("stolleraveragerangechannelbands", "Stoller Average Range Channel Bands", ["stolleraveragerange", "sarc", "sarcb"], gocharting="STARCBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("srsi", "Stochastic RSI", ["srsi", "stochrsi", "stochasticrsi"], tradingview="StochasticRSI@tv-basicstudies"),
		Parameter("supertrend", "Supertrend", ["supertrend"], gocharting="SUPERTREND", dynamic={"GoCharting": [14, 2]}),
		Parameter("swing", "Swing Index", ["swing", "swingindex", "si"], gocharting="SWINGINDEX"),
		Parameter("tema", "Triple EMA", ["tema", "3ema"], tradingview="TripleEMA@tv-basicstudies", gocharting="TEMA", dynamic={"GoCharting": [20]}),
		Parameter("tpo", "Market Profile", ["tpo", "marketprofile"], gocharting="MARKETPROFILE"),
		Parameter("trix", "Triple Exponential Average", ["trix", "txa", "texa"], tradingview="Trix@tv-basicstudies", gocharting="TRIX", dynamic={"GoCharting": [20]}),
		Parameter("ts", "Time Series Moving Average", ["timeseriesmovingaverage", "ts"], gocharting="TS", dynamic={"GoCharting": [20]}),
		Parameter("threeblackcrowspattern", "Three Black Crows Pattern", ["threeblackcrows", "tbc"], gocharting="THREEBLACKCROWS"),
		Parameter("threewhitesoldierspattern", "Three White Soldiers Pattern", ["threewhitesoldiers", "tws"], gocharting="THREEWHITESOLDIERS"),
		Parameter("tradevolumeindex", "Trade Volume Index", ["tradevolumeindex", "tvi"], gocharting="TRADEVOLUMEINDEX", dynamic={"GoCharting": [20]}),
		Parameter("trendintensity", "Trend Intensity", ["trendintensity", "ti"], gocharting="TRENDINTENSITY"),
		Parameter("triangularmovingaverage", "Triangular Moving Average", ["tringularmovingaverage", "trma"], gocharting="TRIANGULAR", dynamic={"GoCharting": [20]}),
		Parameter("tweezerbottompattern", "Tweezer Bottom Pattern", ["tweezerbottom", "tbp"], gocharting="TWEEZERBOTTOM"),
		Parameter("tweezertoppattern", "Tweezer Top Pattern", ["tweezertop", "ttp"], gocharting="TWEEZERTOP"),
		Parameter("tmfi", "Twiggs Money Flow Index", ["tmfi", "twiggsmfi"], gocharting="TWIGGSMONEYFLOWINDEX", dynamic={"GoCharting": [20]}),
		Parameter("typicalprice", "Typical Price", ["typicalprice", "tp"], gocharting="TP", dynamic={"GoCharting": [20]}),
		Parameter("ulcer", "Ulcer Index", ["ulcer", "ulcerindex", "ui"], gocharting="ULCERINDEX", dynamic={"GoCharting": [14, 2]}),
		Parameter("ultimate", "Ultimate Oscillator", ["ultimate", "uo"], tradingview="UltimateOsc@tv-basicstudies"),
		Parameter("vidya", "VIDYA Moving Average", ["vidya"], gocharting="VIDYA", dynamic={"GoCharting": [20]}),
		Parameter("vigor", "Vigor Index", ["vigor", "rvi"], tradingview="VigorIndex@tv-basicstudies"),
		Parameter("vma", "Variable Moving Average", ["vma", "variablema", "varma"], gocharting="VMA", dynamic={"GoCharting": [20]}),
		Parameter("volatility", "Volatility Index", ["volatility", "vi"], tradingview="VolatilityIndex@tv-basicstudies"),
		Parameter("volumeoscillator", "Volume Oscillator", ["volosc", "volumeoscillator"], gocharting="VOLUMEOSCILLATOR"),
		Parameter("volumeprofile", "Volume Profile", ["volumeprofile"], gocharting="VOLUMEPROFILE"),
		Parameter("volumeroc", "Volume ROC", ["vroc", "volumeroc"], gocharting="VOLUMEROC", dynamic={"GoCharting": [20]}),
		Parameter("volumeunderlay", "Volume Underlay", ["volund", "volumeunderlay"], gocharting="VOLUMEUNDERLAY", dynamic={"GoCharting": [20]}),
		Parameter("vortex", "Vortex", ["vortex"], gocharting="VORTEX", dynamic={"GoCharting": [20]}),
		Parameter("vstop", "VSTOP", ["vstop"], tradingview="VSTOP@tv-basicstudies"),
		Parameter("vwap", "VWAP", ["vwap"], tradingview="VWAP@tv-basicstudies", gocharting="VWAP"),
		Parameter("vwma", "VWMA", ["mavw", "vw", "vwma"], tradingview="MAVolumeWeighted@tv-basicstudies", dynamic={"GoCharting": [20]}),
		Parameter("weightedclose", "Weighted Close", ["weightedclose"], gocharting="WC", dynamic={"GoCharting": [20]}),
		Parameter("williamsr", "Williams %R", ["williamsr", "wr"], tradingview="WilliamR@tv-basicstudies", gocharting="WILLIAMSR", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("williamsa", "Williams Alligator", ["williamsa", "williamsalligator", "wa"], tradingview="WilliamsAlligator@tv-basicstudies"),
		Parameter("williamsf", "Williams Fractal", ["williamsf", "williamsfractal", "wf"], tradingview="WilliamsFractal@tv-basicstudies"),
		Parameter("wma", "Weighted Moving Average", ["wma"], tradingview="MAWeighted@tv-basicstudies", gocharting="WMA"),
		Parameter("zz", "Zig Zag", ["zz", "zigzag"], tradingview="ZigZag@tv-basicstudies", gocharting="ZIGZAG")
	],
	"type": [
		Parameter("ta", "advanced TA", ["ta", "advanced"], finviz="&ta=1"),
		Parameter("nv", "no volume", ["hv", "nv", "novol"], tradingview="&hidevolume=1"),
		Parameter("np", "no price", ["hp", "np", "nopri"], gocharting="&showmainchart=false"),
		Parameter("theme", "light theme", ["light", "white"], tradingview="&theme=light", gocharting="&theme=light"),
		Parameter("theme", "dark theme", ["dark", "black"], tradingview="&theme=dark", gocharting="&theme=dark"),
		Parameter("candleStyle", "bars", ["bars", "bar"], tradingview="&style=0"),
		Parameter("candleStyle", "candles", ["candles", "candle"], tradingview="&style=1", gocharting="&charttype=CANDLESTICK", finviz="&ty=c"),
		Parameter("candleStyle", "hollow candles", ["hollow"], gocharting="&charttype=HOLLOW_CANDLESTICK"),
		Parameter("candleStyle", "heikin ashi", ["heikin", "heiken", "heikinashi", "heikenashi", "ashi", "ha"], tradingview="&style=8", gocharting="&charttype=HEIKIN_ASHI"),
		Parameter("candleStyle", "line break", ["break", "linebreak", "lb"], tradingview="&style=7", gocharting="&charttype=LINEBREAK"),
		Parameter("candleStyle", "line", ["line"], tradingview="&style=2", gocharting="&charttype=LINE", finviz="&ty=l"),
		Parameter("candleStyle", "area", ["area"], tradingview="&style=3", gocharting="&charttype=AREA"),
		Parameter("candleStyle", "renko", ["renko"], tradingview="&style=4", gocharting="&charttype=RENKO"),
		Parameter("candleStyle", "kagi", ["kagi"], tradingview="&style=5", gocharting="&charttype=KAGI"),
		Parameter("candleStyle", "point&figure", ["point", "figure", "pf", "paf"], tradingview="&style=6", gocharting="&charttype=POINT_FIGURE")
	],
	"style": [
		Parameter("theme", "light theme", ["light", "white"], tradinglite="light", finviz="light"),
		Parameter("theme", "dark theme", ["dark", "black"], tradinglite="dark", finviz="dark"),
		Parameter("log", "log", ["log", "logarithmic"], tradingview="log"),
		Parameter("wide", "wide", ["wide"], tradinglite="wide", tradingview="wide", bookmap="wide", gocharting="wide"),
		Parameter("flowlist", "list", ["list", "old", "legacy"], alphaflow="flowlist")
	],
	"preferences": [
		Parameter("heatmapIntensity", "whales heatmap intensity", ["whale", "whales"], tradinglite=(50,100)),
		Parameter("heatmapIntensity", "low heatmap intensity", ["low"], tradinglite=(10,100)),
		Parameter("heatmapIntensity", "normal heatmap intensity", ["normal"], tradinglite=(0,85)),
		Parameter("heatmapIntensity", "medium heatmap intensity", ["medium", "med"], tradinglite=(0,62)),
		Parameter("heatmapIntensity", "high heatmap intensity", ["high"], tradinglite=(0,39)),
		Parameter("heatmapIntensity", "crazy heatmap intensity", ["crazy"], tradinglite=(0,16)),
		Parameter("autoDeleteOverride", "autodelete", ["del", "delete", "autodelete"], tradinglite="autodelete", tradingview="autodelete", bookmap="autodelete", gocharting="autodelete", finviz="autodelete", alternativeme="autodelete", alphaflow="autodelete"),
		Parameter("hideRequest", "hide request", ["hide"], tradinglite="hide", tradingview="hide", bookmap="hide", gocharting="hide", finviz="hide", alternativeme="hide", alphaflow="hide"),
		Parameter("forcePlatform", "force chart on TradingLite", ["tl", "tradinglite"], tradinglite=True),
		Parameter("forcePlatform", "force chart on TradingView", ["tv", "tradingview"], tradingview=True),
		Parameter("forcePlatform", "force chart on Bookmap", ["bm", "bookmap"], bookmap=True),
		Parameter("forcePlatform", "force chart on GoCharting", ["gc", "gocharting"], gocharting=True),
		Parameter("forcePlatform", "force chart on Finviz", ["fv", "finviz"], finviz=True),
		Parameter("forcePlatform", "force chart on Alternative.me", ["am", "alternativeme"], alternativeme=True),
		Parameter("link", "link", ["link"], tradinglite="link", tradingview="link", bookmap="link", gocharting="link", finviz="link"),
		Parameter("force", "force", ["--force"], tradinglite="force", tradingview="force", bookmap="force", gocharting="force", finviz="force", alternativeme="force", alphaflow="force"),
		Parameter("upload", "upload", ["--upload"], tradinglite="upload", tradingview="upload", bookmap="upload", gocharting="upload", finviz="upload", alternativeme="upload", alphaflow="upload")
	]
}
DEFAULTS = {
	"Alternative.me": {
		"timeframes": [Parameter(None, None, None)],
		"indicators": [],
		"type": [],
		"style": [],
		"preferences": []
	},
	"TradingLite": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"type": [],
		"style": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="style", params=PARAMETERS)],
		"preferences": [AbstractRequest.find_parameter_with_id("heatmapIntensity", name="normal heatmap intensity", type="preferences", params=PARAMETERS)]
	},
	"TradingView": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"type": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="type", params=PARAMETERS), AbstractRequest.find_parameter_with_id("candleStyle", name="candles", type="type", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Bookmap": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"type": [],
		"style": [],
		"preferences": []
	},
	"GoCharting": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"type": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="type", params=PARAMETERS), AbstractRequest.find_parameter_with_id("candleStyle", name="candles", type="type", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Finviz": {
		"timeframes": [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"type": [AbstractRequest.find_parameter_with_id("candleStyle", name="candles", type="type", params=PARAMETERS)],
		"style": [AbstractRequest.find_parameter_with_id("theme", name="light theme", type="style", params=PARAMETERS)],
		"preferences": []
	},
	"Alpha Flow": {
		"timeframes": [],
		"indicators": [],
		"type": [],
		"style": [],
		"preferences": []
	}
}


class ChartRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional", **kwargs):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = ChartRequest(tickerId, platform, bias)

	async def parse_argument(self, argument):
		for platform, request in self.requests.items():
			if request.errorIsFatal: continue

			# None None - No successeful parse
			# None True - Successful parse and add
			# "" False - Successful parse and error
			# None False - Successful parse and breaking error

			finalOutput = None

			outputMessage, success = await request.add_timeframe(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_indicator(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_type(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_style(argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

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
			elif finalOutput.startswith("`Force Chart"):
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

			types = "".join([e.parsed[platform] for e in request.types])
			styles = [e.parsed[platform] for e in request.styles]
			preferences = [{"id": e.id, "value": e.parsed[platform]} for e in request.preferences]

			if platform == "Alternative.me":
				if request.ticker.get("id") not in ["FGI"]: request.set_error(None, isFatal=True)
			
			elif platform == "TradingLite":
				if not bool(request.exchange):
					request.set_error("TradingLite currently only supports cryptocurrency markets on supported exchanges.", isFatal=True)
				elif request.ticker.get("symbol") is None:
					request.set_error("Requested chart for `{}` is not available.".format(request.ticker.get("id")), isFatal=True)
				elif request.exchange.get("id") in ["binanceusdm", "binancecoinm", "ftx", "okex5"]:
					request.set_error("{} exchange is not available. ||Yet.||".format(request.exchange.get("name")), isFatal=True)
			
			elif platform == "TradingView":
				if "&style=6" in types and "log" in styles:
					request.set_error("Point & Figure chart can't be viewed in log scale.", isFatal=True)
			
			elif platform == "Bookmap":
				if not bool(request.exchange):
					request.set_error("Bookmap currently only supports cryptocurrency markets on supported exchanges.", isFatal=True)
			
			elif platform == "GoCharting":
				indicators = request.indicators
				parameters = request.numericalParameters
				lengths = {i: [] for i in range(len(indicators))}
				cursor = len(parameters) - 1
				for i in reversed(range(len(indicators))):
					while parameters[cursor] != -1:
						lengths[i].insert(0, parameters[cursor])
						cursor -= 1
					cursor -= 1

					if indicators[i].dynamic is not None and lengths[i] != 0 and len(lengths[i]) > len(indicators[i].dynamic[platform]):
						request.set_error("{} indicator takes in `{}` {}, but `{}` were given.".format(indicators[i].name, len(indicators[i].dynamic[platform]), "parameters" if len(indicators[i].dynamic[platform]) > 1 else "parameter", len(lengths[i])), isFatal=True)
						break

				if len(indicators) == 0 and len(parameters) != 0:
					request.set_error("`{}` is not a valid argument.".format(parameters[0]), isFatal=True)
			
			elif platform == "Finviz":
				pass
			
			elif platform == "Alpha Flow":
				if request.ticker.get("id") != "OPTIONS":
					if len(request.timeframes) != 0 and "flowlist" not in styles:
						request.styles.append(AbstractRequest.find_parameter_with_id("flowlist", name="list", type="style", params=PARAMETERS))
					elif len(request.timeframes) == 0:
						request.timeframes.append(AbstractRequest.find_parameter_with_id(10080, type="timeframes", params=PARAMETERS))
				else:
					if len(request.timeframes) != 0:
						request.set_error("Timeframes are not available for options flow overview on Alpha Flow.", isFatal=True)
					request.timeframes.append(Parameter(None, None, None, alphaflow=None))


	def to_dict(self):
		d = {
			"platforms": self.platforms,
			"currentPlatform": self.currentPlatform
		}

		timeframes = []

		for platform in self.platforms:
			request = self.requests[platform].to_dict()
			timeframes.append(request.pop("timeframes"))
			d[platform] = request

		d["timeframes"] = {p: t for p, t in zip(self.platforms, timeframes)}
		d["requestCount"] = len(d["timeframes"][d.get("currentPlatform")])

		return d


class ChartRequest(AbstractRequest):
	def __init__(self, tickerId, platform, bias):
		super().__init__(platform, bias)
		self.tickerId = tickerId
		self.ticker = {}
		self.exchange = {}

		self.timeframes = []
		self.indicators = []
		self.types = []
		self.styles = []
		self.preferences = []
		self.numericalParameters = []

		self.currentTimeframe = None
		self.hasExchange = False

	async def process_ticker(self):
		updatedTicker, error = None, None
		try: updatedTicker, error = await TickerParser.match_ticker(self.tickerId, self.exchange, self.platform, self.parserBias)
		except: print(format_exc())

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

	# async def add_timeframe(self, argument) -- inherited

	# async def add_exchange(self, argument) -- inherited

	async def add_indicator(self, argument):
		if argument in ["oscillator", "bands", "band", "ta"]: return None, False
		length = search("(\d+)$", argument)
		if length is not None and int(length.group()) > 0: argument = argument[:-len(length.group())]
		indicatorSupported, parsedIndicator = self.add_parameter(argument, "indicators")
		if parsedIndicator is not None and not self.has_parameter(parsedIndicator.id, self.indicators):
			if not indicatorSupported:
				outputMessage = "`{}` indicator is not supported on {}.".format(parsedIndicator.name, self.platform)
				return outputMessage, False
			self.indicators.append(parsedIndicator)
			self.numericalParameters.append(-1)
			if length is not None:
				if self.platform not in ["GoCharting"]:
					outputMessage = "Indicator lengths can only be changed on GoCharting."
					return outputMessage, False
				else:
					self.numericalParameters.append(int(length.group()))
			return None, True
		return None, None

	async def add_type(self, argument):
		typeSupported, parsedType = self.add_parameter(argument, "type")
		if parsedType is not None and not self.has_parameter(parsedType.id, self.types):
			if not typeSupported:
				outputMessage = "`{}` chart style is not supported on {}.".format(parsedType.name.title(), self.platform)
				return outputMessage, False
			self.types.append(parsedType)
			return None, True
		return None, None

	# async def add_style(self, argument) -- inherited

	# async def add_preferences(self, argument) -- inherited

	async def add_numerical_parameters(self, argument):
		try:
			numericalParameter = float(argument)
			if numericalParameter <= 0:
				outputMessage = "Only parameters greater than `0` are accepted."
				return outputMessage, False
			if self.platform not in ["GoCharting"]:
				outputMessage = "Indicator lengths can only be changed on GoCharting."
				return outputMessage, False
			self.numericalParameters.append(numericalParameter)
			return None, True
		except: return None, None

	def set_default_for(self, t):
		if t == "timeframes" and len(self.timeframes) == 0:
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.timeframes): self.timeframes.append(parameter)
		elif t == "indicators":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.indicators): self.indicators.append(parameter)
		elif t == "type":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.types): self.types.append(parameter)
		elif t == "style":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.styles): self.styles.append(parameter)
		elif t == "preferences":
			for parameter in DEFAULTS.get(self.platform, {}).get(t, []):
				if not self.has_parameter(parameter.id, self.preferences): self.preferences.append(parameter)

	def prepare_indicators(self):
		indicators = []

		if self.platform == "TradingView":
			if len(self.indicators) == 0:
				indicators = ""
			else:
				indicators = "&studies=" + "%1F".join([e.parsed[self.platform] for e in self.indicators])

		elif self.platform == "GoCharting":
			if len(self.indicators) == 0:
				indicators = ""
			else:
				lengths = {i: [] for i in range(len(self.indicators))}
				cursor = len(self.numericalParameters) - 1
				for i in reversed(range(len(self.indicators))):
					while self.numericalParameters[cursor] != -1:
						lengths[i].insert(0, self.numericalParameters[cursor])
						cursor -= 1
					cursor -= 1

					if self.indicators[i].dynamic is not None and lengths[i] != 0 and len(lengths[i]) < len(self.indicators[i].dynamic[self.platform]):
						for j in range(len(lengths[i]), len(self.indicators[i].dynamic[self.platform])):
							lengths[i].append(self.indicators[i].dynamic[self.platform][j])

					indicators.insert(0, "{}_{}".format(self.indicators[i].parsed[self.platform], "_".join([str(l) for l in lengths[i]])))

				indicators = "&studies=" + "-".join(indicators)

		return indicators


	def to_dict(self):
		d = {
			"ticker": self.ticker,
			"exchange": self.exchange,
			"parserBias": self.parserBias,
			"timeframes": [e.parsed[self.platform] for e in self.timeframes],
			"indicators": self.prepare_indicators(),
			"types": "".join([e.parsed[self.platform] for e in self.types]),
			"styles": [e.parsed[self.platform] for e in self.styles],
			"preferences": [{"id": e.id, "value": e.parsed[self.platform]} for e in self.preferences],
			"numericalParameters": self.numericalParameters,
			"currentTimeframe": self.currentTimeframe
		}
		return d