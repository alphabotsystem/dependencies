from sys import maxsize as MAXSIZE
from time import time
from re import search
from traceback import format_exc

from TickerParser import TickerParser, Exchange
from .parameter import ChartParameter as Parameter
from .abstract import AbstractRequestHandler, AbstractRequest


PARAMETERS = {
	"timeframes": [
		Parameter(1, "1-minute", ["1", "1m", "1min", "1mins", "1minute", "1-minute", "1minutes", "min", "m"], tradinglite="1", tradingview="1", gocharting="1m"),
		Parameter(2, "2-minute", ["2", "2m", "2min", "2mins", "2minute", "2-minute", "2minutes"]),
		Parameter(3, "3-minute", ["3", "3m", "3min", "3mins", "3minute", "3-minute", "3minutes"], tradinglite="3", tradingview="3", gocharting="3m"),
		Parameter(4, "4-minute", ["4", "4m", "4min", "4mins", "4minute", "4-minute", "4minutes"]),
		Parameter(5, "5-minute", ["5", "5m", "5min", "5mins", "5minute", "5-minute", "5minutes"], tradinglite="5", tradingview="5", gocharting="5m"),
		Parameter(6, "6-minute", ["6", "6m", "6min", "6mins", "6minute", "6-minute", "6minutes"]),
		Parameter(10, "10-minute", ["10", "10m", "10min", "10mins", "10minute", "10-minute", "10minutes"], bookmap="bm-btn-time-frame-10m"),
		Parameter(15, "15-minute", ["15", "15m", "15min", "15mins", "15minute", "15-minute", "15minutes"], tradinglite="15", tradingview="15", gocharting="15m"),
		Parameter(20, "20-minute", ["20", "20m", "20min", "20mins", "20minute", "20-minute", "20minutes"]),
		Parameter(30, "30-minute", ["30", "30m", "30min", "30mins", "30minute", "30-minute", "30minutes"], tradinglite="30", tradingview="30", gocharting="30m"),
		Parameter(45, "45-minute", ["45", "45m", "45min", "45mins", "45minute", "45-minute", "45minutes"], tradingview="45"),
		Parameter(60, "1-hour", ["60", "60m", "60min", "60mins", "60minute", "60-minute", "60minutes", "1", "1h", "1hr", "1hour", "1-hour", "1hours", "hourly", "hour", "hr", "h"], tradinglite="60", tradingview="60", bookmap="bm-btn-time-frame-1h", gocharting="1h"),
		Parameter(120, "2-hour", ["120", "120m", "120min", "120mins", "120minute", "120-minute", "120minutes", "2", "2h", "2hr", "2hrs", "2hour", "2-hour", "2hours"], tradinglite="120", tradingview="120", gocharting="2h"),
		Parameter(180, "3-hour", ["180", "180m", "180min", "180mins", "180minute", "180-minute", "180minutes", "3", "3h", "3hr", "3hrs", "3hour", "3-hour", "3hours"], tradingview="180"),
		Parameter(240, "4-hour", ["240", "240m", "240min", "240mins", "240minute", "240-minute", "240minutes", "4", "4h", "4hr", "4hrs", "4hour", "4-hour", "4hours"], tradinglite="240", tradingview="240", gocharting="4h"),
		Parameter(360, "6-hour", ["360", "360m", "360min", "360mins", "360minute", "360-minute", "360minutes", "6", "6h", "6hr", "6hrs", "6hour", "6-hour", "6hours"], tradinglite="360"),
		Parameter(480, "8-hour", ["480", "480m", "480min", "480mins", "480minute", "480-minute", "480minutes", "8", "8h", "8hr", "8hrs", "8hour", "8-hour", "8hours"], tradinglite="480"),
		Parameter(720, "12-hour", ["720", "720m", "720min", "720mins", "720minute", "720-minute", "720minutes", "12", "12h", "12hr", "12hrs", "12hour", "12-hour", "12hours"], tradinglite="720", gocharting="12h"),
		Parameter(1440, "1-day", ["24", "24h", "24hr", "24hrs", "24hour", "24-hour", "24hours", "d", "day", "1", "1d", "1day", "1-day", "daily", "1440", "1440m", "1440min", "1440mins", "1440minute", "1440-minute", "1440minutes"], tradinglite="1440", tradingview="D", bookmap="bm-btn-time-frame-1d", gocharting="1D", finviz="d", alphaflow="yesterday"),
		Parameter(2880, "2-day", ["48", "48h", "48hr", "48hrs", "48hour", "48-hour", "48hours", "2", "2d", "2day", "2-day", "2880", "2880m", "2880min", "2880mins", "2880minute", "2880-minute", "2880minutes"]),
		Parameter(3420, "3-day", ["72", "72h", "72hr", "72hrs", "72hour", "72-hour", "72hours", "3", "3d", "3day", "3-day", "3420", "3420m", "3420min", "3420mins", "3420minute", "3420-minute", "3420minutes"]),
		Parameter(5760, "4-day", ["96", "96h", "96hr", "96hrs", "96hour", "96-hour", "96hours", "4", "4d", "4day", "4-day", "5760", "5760m", "5760min", "5760mins", "5760minute", "5760-minute", "5760minutes"]),
		Parameter(7200, "5-day", ["120", "120h", "120hr", "120hrs", "120hour", "120-hour", "120hours", "5", "5d", "5day", "5-day", "7200", "7200m", "7200min", "7200mins", "7200minute", "7200-minute", "7200minutes"]),
		Parameter(8640, "6-day", ["144", "144h", "144hr", "144hrs", "144hour", "144-hour", "144hours", "6", "6d", "6day", "6-day", "8640", "8640m", "8640min", "8640mins", "8640minute", "8640-minute", "8640minutes"]),
		Parameter(10080, "1-week", ["7", "7d", "7day", "7-day", "7days", "w", "week", "1w", "1-week", "1week", "weekly"], tradingview="W", bookmap="bm-btn-time-frame-1W", gocharting="1W", finviz="w", alphaflow="lastweek"),
		Parameter(20160, "2-week", ["14", "14d", "14day", "14-day", "14days", "2w", "2-week", "2week"]),
		Parameter(30240, "3-week", ["21", "21d", "21day", "21-day", "21days", "3w", "3-week", "3week"]),
		Parameter(43829, "1-month", ["30d", "30day", "30-day", "30days", "1", "1m", "m", "mo", "month", "1mo", "1month", "1-month", "monthly"], tradingview="M", bookmap="bm-btn-time-frame-1Mo", gocharting="1M", finviz="m"),
		Parameter(87658, "2-month", ["2", "2m", "2m", "2mo", "2month", "2-month", "2months"]),
		Parameter(131487, "3-month", ["3", "3m", "3m", "3mo", "3month", "3-month", "3months"]),
		Parameter(175316, "4-month", ["4", "4m", "4m", "4mo", "4month", "4-month", "4months"]),
		Parameter(262974, "6-month", ["6", "6m", "5m", "6mo", "6month", "6-month", "6months"]),
		Parameter(525949, "1-year", ["12", "12m", "12mo", "12month", "12months", "year", "yearly", "1year", "1-year", "1y", "y", "annual", "annually"]),
		Parameter(1051898, "2-year", ["24", "24m", "24mo", "24month", "24months", "2year", "2-year", "2y"]),
		Parameter(1577847, "3-year", ["36", "36m", "36mo", "36month", "36months", "3year", "3-year", "3y"]),
		Parameter(2103796, "4-year", ["48", "48m", "48mo", "48month", "48months", "4year", "4-year", "4y"]),
		Parameter(2628000, "5-year", ["60", "60m", "60mo", "60month", "60months", "5year", "5-year", "5y"])
	],
	"indicators": [
		Parameter("ab", "Abandoned Baby", ["ab", "abandonedbaby"], gocharting="ABANDONEDBABY"),
		Parameter("accd", "Accumulation/Distribution", ["accd", "ad", "acc", "accumulationdistribution", "accumulation/distribution"], tradingview="ACCD@tv-basicstudies", gocharting="ACC", dynamic={"GoCharting": [20]}),
		Parameter("accumulationswingindex", "Accumulation Swing Index", ["accumulationswingindex", "accsi", "asi"], gocharting="ACCSWINGINDEX"),
		Parameter("admi", "Average Directional Movement Index", ["admi", "adx", "averagedirectionalmovementindex"], gocharting="ADX", dynamic={"GoCharting": [20]}),
		Parameter("adr", "ADR", ["adr"], tradingview="studyADR@tv-basicstudies"),
		Parameter("alligator", "Alligator", ["alligator"], gocharting="ALLIGATOR"),
		Parameter("aroon", "Aroon", ["aroon"], tradingview="AROON@tv-basicstudies", gocharting="AROON", dynamic={"GoCharting": [20]}),
		Parameter("aroonoscillator", "Aroon Oscillator", ["aroonoscillator"], gocharting="AROONOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("atr", "ATR", ["atr"], tradingview="ATR@tv-basicstudies", gocharting="ATR", dynamic={"GoCharting": [20]}),
		Parameter("atrb", "ATR Bands", ["atrb", "atrbands"], gocharting="ATRBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("atrts", "ATR Trailing Stop", ["trailingstop", "atrts", "atrstop", "atrs", "atrtrailingstop"], gocharting="ATRTRAILINGSTOP", dynamic={"GoCharting": [14, 2]}),
		Parameter("awesome", "Awesome Oscillator", ["awesome", "ao", "awesomeoscillator"], tradingview="AwesomeOscillator@tv-basicstudies", gocharting="AWESOMEOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("balanceofpower", "Balance of Power", ["balanceofpower", "bop"], gocharting="BOP", dynamic={"GoCharting": [20]}),
		Parameter("bearish", "All Bearish Candlestick Patterns", ["bear", "bearish", "bearishpatterns", "allbearishcandlestickpatterns"], gocharting="BEARISH"),
		Parameter("bearishengulfing", "Bearish Engulfing Pattern", ["bearishengulfing", "bearishengulfingpattern"], gocharting="BEARISHENGULFINGPATTERN"),
		Parameter("bearishhammer", "Bearish Hammer Pattern", ["bearishhammer", "bearishhammerpattern"], gocharting="BEARISHHAMMER"),
		Parameter("bearishharami", "Bearish Harami Pattern", ["bearishharami", "bearishharamipattern"], gocharting="BEARISHHARAMI"),
		Parameter("bearishharamicross", "Bearish Harami Cross Pattern", ["bearishharamicross", "bearishharamicrosspattern"], gocharting="BEARISHHARAMICROSS"),
		Parameter("bearishinvertedhammer", "Bearish Inverted Hammer Pattern", ["bearishinvertedhammer", "bearishinvertedhammerpattern"], gocharting="BEARISHINVERTEDHAMMER"),
		Parameter("bearishmarubozu", "Bearish Marubozu Pattern", ["bearishmarubozu", "bearishmarubozupattern"], gocharting="BEARISHMARUBOZU"),
		Parameter("bearishspinningtop", "Bearish Spinning Top Pattern", ["bearishspinningtop", "bearishspinningtoppattern"], gocharting="BEARISHSPINNINGTOP"),
		Parameter("width", "Bollinger Bands Width", ["width", "bbw", "bollingerbandswidth"], tradingview="BollingerBandsWidth@tv-basicstudies"),
		Parameter("bullish", "All Bullish Candlestick Patterns", ["bull", "bullish", "bullishpatterns", "allbullishcandlestickpatterns"], gocharting="BULLISH"),
		Parameter("bullishengulfing", "Bullish Engulfing Pattern", ["bullishengulfing", "bullishengulfingpattern"], gocharting="BULLISHENGULFINGPATTERN"),
		Parameter("bullishhammer", "Bullish Hammer Pattern", ["bullishhammer", "bullishhammerpattern"], gocharting="BULLISHHAMMER"),
		Parameter("bullishharami", "Bullish Harami Pattern", ["bullishharami", "bullishharamipattern"], gocharting="BULLISHHARAMI"),
		Parameter("bullishharamicross", "Bullish Harami Cross Pattern", ["bullishharamicross", "bullishharamicrosspattern"], gocharting="BULLISHHARAMICROSS"),
		Parameter("bullishinvertedhammer", "Bullish Inverted Hammer Pattern", ["bullishinvertedhammer", "bullishinvertedhammerpattern"], gocharting="BULLISHINVERTEDHAMMER"),
		Parameter("bullishmarubozu", "Bullish Marubozu Pattern", ["bullishmarubozu", "bullishmarubozupattern"], gocharting="BULLISHMARUBOZU"),
		Parameter("bullishspinningtop", "Bullish Spinning Top Pattern", ["bullishspinningtop", "bullishspinningtoppattern"], gocharting="BULLISHSPINNINGTOP"),
		Parameter("bollinger", "Bollinger Bands", ["bollinger", "bbands", "bb", "bollingerbands"], tradingview="BB@tv-basicstudies", gocharting="BOLLINGERBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("cmf", "Chaikin Money Flow Index", ["cmf", "chaikinmoneyflow", "chaikinmoneyflowindex"], tradingview="CMF@tv-basicstudies", gocharting="CHAIKINMFI", dynamic={"GoCharting": [20]}),
		Parameter("chaikin", "Chaikin Oscillator", ["chaikin", "co", "chaikinoscillator"], tradingview="ChaikinOscillator@tv-basicstudies"),
		Parameter("cv", "Chaikin Volatility", ["cv", "chaikinvolatility"], gocharting="CHAIKINVOLATILITY"),
		Parameter("cf", "Chande Forecast", ["cf", "chandeforecast"], gocharting="CHANDEFORECAST", dynamic={"GoCharting": [20]}),
		Parameter("chande", "Chande MO", ["chande", "cmo", "chandemo"], tradingview="chandeMO@tv-basicstudies", gocharting="CMO", dynamic={"GoCharting": [20]}),
		Parameter("choppiness", "Choppiness Index", ["choppiness", "ci", "choppinessindex"], tradingview="ChoppinessIndex@tv-basicstudies", gocharting="CHOPPINESS"),
		Parameter("cci", "CCI", ["cci"], tradingview="CCI@tv-basicstudies", gocharting="CCI", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("crsi", "CRSI", ["crsi"], tradingview="CRSI@tv-basicstudies"),
		Parameter("cog", "Center of Gravity", ["cog", "centerofgravity"], gocharting="COG", dynamic={"GoCharting": [20]}),
		Parameter("coppock", "Coppock", ["coppock"], gocharting="COPPOCK"),
		Parameter("cumtick", "Cumulative Tick", ["cumtick", "cumulativetick"], gocharting="CUMTICK", dynamic={"GoCharting": [20]}),
		Parameter("correlation", "Correlation Coefficient", ["correlation", "cc", "correlationcoefficient"], tradingview="CorrelationCoefficient@tv-basicstudies"),
		Parameter("darkcloudcoverpattern", "Dark Cloud Cover Pattern", ["darkcloudcover", "dccp", "darkcloudcoverpattern"], gocharting="DARKCLOUDCOVER"),
		Parameter("detrended", "Detrended Price Oscillator", ["detrended", "dpo", "detrendedpriceoscillator"], tradingview="DetrendedPriceOscillator@tv-basicstudies", gocharting="DPO", dynamic={"GoCharting": [20]}),
		Parameter("disparityoscillator", "Disparity Oscillator", ["disparityoscillator"], gocharting="DISPARITY", dynamic={"GoCharting": [20]}),
		Parameter("donchainwidth", "Donchain Width", ["donchainwidth"], gocharting="DONCHIANWIDTH", dynamic={"GoCharting": [20]}),
		Parameter("dm", "DM", ["dm", "directional"], tradingview="DM@tv-basicstudies"),
		Parameter("dojipattern", "Doji Pattern", ["doji", "dojipattern"], gocharting="DOJI"),
		Parameter("donch", "DONCH", ["donch", "donchainchannel"], tradingview="DONCH@tv-basicstudies", gocharting="DONCHIANCHANNEL", dynamic={"GoCharting": [14, 2]}),
		Parameter("downsidetasukigappattern", "Downside Tasuki Gap Pattern", ["downsidetasukigap", "dtgp", "downsidetasukigappattern"], gocharting="DOWNSIDETASUKIGAP"),
		Parameter("dema", "Double EMA", ["dema", "doubleema"], tradingview="DoubleEMA@tv-basicstudies", gocharting="DEMA", dynamic={"GoCharting": [20]}),
		Parameter("dragonflydojipattern", "Dragonfly Doji Pattern", ["dragonflydoji", "ddp", "dragonflydojipattern"], gocharting="DRAGONFLYDOJI"),
		Parameter("efi", "EFI", ["efi"], tradingview="EFI@tv-basicstudies"),
		Parameter("ema", "EMA", ["ema"], tradingview="MAExp@tv-basicstudies", gocharting="EMA", dynamic={"GoCharting": [20]}),
		Parameter("elderray", "Elder Ray", ["elderray"], gocharting="ELDERRAY"),
		Parameter("elliott", "Elliott Wave", ["elliott", "ew", "elliottwave"], tradingview="ElliottWave@tv-basicstudies"),
		Parameter("env", "ENV", ["env"], tradingview="ENV@tv-basicstudies"),
		Parameter("eom", "Ease of Movement", ["eom", "easeofmovement"], tradingview="EaseOfMovement@tv-basicstudies", gocharting="EOM", dynamic={"GoCharting": [20]}),
		Parameter("eveningdojistarpattern", "Evening Doji Star Pattern", ["eveningdojistar", "edsp", "eveningdojistarpattern"], gocharting="EVENINGDOJISTAR"),
		Parameter("eveningstarpattern", "Evening Star Pattern", ["eveningstar", "esp", "eveningstarpattern"], gocharting="EVENINGSTAR"),
		Parameter("fisher", "Fisher Transform", ["fisher", "ft", "fishertransform"], tradingview="FisherTransform@tv-basicstudies", gocharting="EHLERFISHERTRANSFORM", dynamic={"GoCharting": [20]}),
		Parameter("forceindex", "Force Index", ["forceindex"], gocharting="FORCEINDEX"),
		Parameter("fullstochasticoscillator", "Full Stochastic Oscillator", ["fso", "fullstochasticoscillator"], gocharting="FULLSTOCHASTICOSCILLATOR"),
		Parameter("gravestonedojipattern", "Gravestone Doji Pattern", ["gravestonedoji", "gd", "gravestonedojipattern"], gocharting="GRAVESTONEDOJI"),
		Parameter("gatoroscillator", "Gator Oscillator", ["gatoroscillator", "gatoro"], gocharting="GATOROSCILLATOR"),
		Parameter("gopalakrishnanrangeindex", "Gopalakrishnan Range Index", ["gopalakrishnanrangeindex", "gri", "gapo"], gocharting="GAPO", dynamic={"GoCharting": [20]}),
		Parameter("guppy", "Guppy Moving Average", ["guppy", "gma", "rainbow", "rma", "guppymovingaverage"], gocharting="GUPPY", dynamic={"GoCharting": [20]}),
		Parameter("guppyoscillator", "Guppy Oscillator", ["guppyoscillator", "guppyo", "rainbowoscillator", "rainbowo"], gocharting="GUPPYOSCILLATOR"),
		Parameter("hangmanpattern", "Hangman Pattern", ["hangman", "hangingman", "hangmanpattern"], gocharting="HANGINGMAN"),
		Parameter("hhv", "Highest High Volume", ["highesthighvolume", "hhv"], gocharting="HHV", dynamic={"GoCharting": [20]}),
		Parameter("hml", "High Minus Low", ["highminuslow", "hml"], gocharting="HIGHMINUSLOW"),
		Parameter("hv", "Historical Volatility", ["historicalvolatility", "hv"], tradingview="HV@tv-basicstudies", gocharting="HISTVOLATILITY"),
		Parameter("hull", "Hull MA", ["hull", "hma", "hullma"], tradingview="hullMA@tv-basicstudies", gocharting="HULL"),
		Parameter("ichimoku", "Ichimoku Cloud", ["ichimoku", "cloud", "ichi", "ic", "ichimokucloud"], tradingview="IchimokuCloud@tv-basicstudies", gocharting="ICHIMOKU"),
		Parameter("imi", "Intraday Momentum Index", ["intradaymomentumindex", "imi", "intradaymi"], gocharting="INTRADAYMI", dynamic={"GoCharting": [20]}),
		Parameter("keltner", "Keltner Channel", ["keltner", "kltnr", "keltnerchannel"], tradingview="KLTNR@tv-basicstudies", gocharting="KELTNERCHANNEL", dynamic={"GoCharting": [14, 2]}),
		Parameter("klinger", "Klinger", ["klinger"], gocharting="KLINGER"),
		Parameter("kst", "Know Sure Thing", ["knowsurething", "kst"], tradingview="KST@tv-basicstudies", gocharting="KST"),
		Parameter("llv", "Lowest Low Volume", ["llv", "lowestlowvolume"], gocharting="LLV", dynamic={"GoCharting": [20]}),
		Parameter("regression", "Linear Regression", ["regression", "lr", "linreg", "linearregression"], tradingview="LinearRegression@tv-basicstudies"),
		Parameter("macd", "MACD", ["macd"], tradingview="MACD@tv-basicstudies", gocharting="MACD"),
		Parameter("massindex", "Mass Index", ["massindex", "mi"], gocharting="MASSINDEX"),
		Parameter("medianprice", "Median Price", ["medianprice", "mp"], gocharting="MP", dynamic={"GoCharting": [20]}),
		Parameter("mom", "Momentum", ["mom", "momentum"], tradingview="MOM@tv-basicstudies", gocharting="MOMENTUMINDICATOR", dynamic={"GoCharting": [20]}),
		Parameter("morningdojistarpattern", "Morning Doji Star Pattern", ["morningdojistar", "mds", "morningdojistarpattern"], gocharting="MORNINGDOJISTAR"),
		Parameter("morningstarpattern", "Morning Star Pattern", ["morningstar", "ms", "morningstarpattern"], gocharting="MORNINGSTAR"),
		Parameter("mf", "Money Flow", ["mf", "mfi", "moneyflow"], tradingview="MF@tv-basicstudies", gocharting="MONEYFLOWINDEX", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("moon", "Moon Phases", ["moon", "moonphases"], tradingview="MoonPhases@tv-basicstudies", gocharting="MOONPHASE"),
		Parameter("ma", "Moving Average", ["ma", "sma", "movingaverage"], tradingview="MASimple@tv-basicstudies", gocharting="SMA", dynamic={"GoCharting": [20]}),
		Parameter("maenvelope", "Moving Average Envelope", ["maenvelope", "mae", "movingaverageenvelope"], gocharting="MAENVELOPE", dynamic={"GoCharting": [14, 2]}),
		Parameter("nvi", "Negative Volume Index", ["nvi", "negvolindex", "negativevolumeindex"], gocharting="NEGVOLINDEX"),
		Parameter("obv", "On Balance Volume", ["obv", "onbalancevolume"], tradingview="OBV@tv-basicstudies", gocharting="ONBALANCEVOLUME", dynamic={"GoCharting": [20]}),
		Parameter("parabolic", "PSAR", ["parabolic", "sar", "psar"], tradingview="PSAR@tv-basicstudies", gocharting="SAR"),
		Parameter("performanceindex", "Performance Index", ["performanceindex", "pi"], gocharting="PERFORMANCEINDEX"),
		Parameter("pgo", "Pretty Good Oscillator", ["prettygoodoscillator", "pgo"], gocharting="PRETTYGOODOSCILLATOR", dynamic={"GoCharting": [20]}),
		Parameter("piercinglinepattern", "Piercing Line Pattern", ["piercingline", "pl", "piercinglinepattern"], gocharting="PIERCINGLINE"),
		Parameter("pmo", "Price Momentum Oscillator", ["pmo", "pricemomentum", "pricemomentumoscillator"], gocharting="PMO"),
		Parameter("po", "Price Oscillator", ["po", "priceoscillator"], tradingview="PriceOsc@tv-basicstudies", gocharting="PRICEOSCILLATOR"),
		Parameter("pphl", "Pivot Points High Low", ["pphl", "pivotpointshighlow"], tradingview="PivotPointsHighLow@tv-basicstudies"),
		Parameter("pps", "Pivot Points Standard", ["pps", "pivot", "pivotpointsstandard"], tradingview="PivotPointsStandard@tv-basicstudies", gocharting="PIVOTPOINTS"),
		Parameter("primenumberbands", "Prime Number Bands", ["primenumberbands", "pnb"], gocharting="PRIMENUMBERBANDS", dynamic={"GoCharting": [14, 2]}),
		Parameter("primenumberoscillator", "Prime Number Oscillator", ["primenumberoscillator", "pno"], gocharting="PRIMENUMBEROSCILLATOR"),
		Parameter("psychologicalline", "Psychological Line", ["psychologicalline", "psy", "psychological"], gocharting="PSY", dynamic={"GoCharting": [20]}),
		Parameter("pvi", "Positive Volume Index", ["pvi", "positivevolumeindex", "posvolindex"], gocharting="POSVOLINDEX"),
		Parameter("pvt", "Price Volume Trend", ["pvt", "pricevolumetrend"], tradingview="PriceVolumeTrend@tv-basicstudies"),
		Parameter("qstickindicator", "Qstick Indicator", ["qstickindicator", "qi", "qsticks"], gocharting="QSTICKS", dynamic={"GoCharting": [20]}),
		Parameter("randomwalk", "Random Walk", ["randomwalk", "ra"], gocharting="RANDOMWALK", dynamic={"GoCharting": [20]}),
		Parameter("ravi", "Ravi Oscillator", ["ravi", "ravioscillator"], gocharting="RAVI"),
		Parameter("rvi", "Relative Volatility", ["rvi", "relativevolatility"], gocharting="RELATIVEVOLATILITY"),
		Parameter("roc", "Price ROC", ["roc", "priceroc", "proc"], tradingview="ROC@tv-basicstudies", gocharting="PRICEROC", dynamic={"GoCharting": [20]}),
		Parameter("rsi", "RSI", ["rsi"], tradingview="RSI@tv-basicstudies", gocharting="RSI", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("schaff", "Schaff", ["schaff"], gocharting="SCHAFF"),
		Parameter("shinohara", "Shinohara", ["shinohara", "shin"], gocharting="SHINOHARA", dynamic={"GoCharting": [20]}),
		Parameter("shootingstarpattern", "Shooting Star Pattern", ["shootingstar", "ss", "shootingstarpattern"], gocharting="SHOOTINGSTAR"),
		Parameter("smiei", "SMI Ergodic Indicator", ["smiei", "smiergodicindicator"], tradingview="SMIErgodicIndicator@tv-basicstudies"),
		Parameter("smieo", "SMI Ergodic Oscillator", ["smieo", "smiergodicoscillator"], tradingview="SMIErgodicOscillator@tv-basicstudies"),
		Parameter("stdev", "Standard Deviation", ["stdev", "stddev", "standarddeviation"], gocharting="SD"),
		Parameter("stochastic", "Stochastic", ["stochastic", "stoch"], tradingview="Stochastic@tv-basicstudies"),
		Parameter("stolleraveragerangechannelbands", "Stoller Average Range Channel Bands", ["stolleraveragerange", "sarc", "sarcb", "stolleraveragerangechannelbands"], gocharting="STARCBAND", dynamic={"GoCharting": [14, 2]}),
		Parameter("srsi", "Stochastic RSI", ["srsi", "stochrsi", "stochasticrsi"], tradingview="StochasticRSI@tv-basicstudies"),
		Parameter("supertrend", "Supertrend", ["supertrend"], gocharting="SUPERTREND", dynamic={"GoCharting": [14, 2]}),
		Parameter("swing", "Swing Index", ["swing", "swingindex", "si"], gocharting="SWINGINDEX"),
		Parameter("tema", "Triple EMA", ["tema", "tripleema"], tradingview="TripleEMA@tv-basicstudies", gocharting="TEMA", dynamic={"GoCharting": [20]}),
		Parameter("tpo", "Market Profile", ["tpo", "marketprofile"], gocharting="MARKETPROFILE"),
		Parameter("trix", "Triple Exponential Average", ["trix", "txa", "texa", "tripleexponentialaverage"], tradingview="Trix@tv-basicstudies", gocharting="TRIX", dynamic={"GoCharting": [20]}),
		Parameter("ts", "Time Series Moving Average", ["timeseriesmovingaverage", "ts"], gocharting="TS", dynamic={"GoCharting": [20]}),
		Parameter("threeblackcrowspattern", "Three Black Crows Pattern", ["threeblackcrows", "tbc", "threeblackcrowspattern"], gocharting="THREEBLACKCROWS"),
		Parameter("threewhitesoldierspattern", "Three White Soldiers Pattern", ["threewhitesoldiers", "tws", "threewhitesoldierspattern"], gocharting="THREEWHITESOLDIERS"),
		Parameter("tradevolumeindex", "Trade Volume Index", ["tradevolumeindex", "tvi"], gocharting="TRADEVOLUMEINDEX", dynamic={"GoCharting": [20]}),
		Parameter("trendintensity", "Trend Intensity", ["trendintensity", "ti"], gocharting="TRENDINTENSITY"),
		Parameter("triangularmovingaverage", "Triangular Moving Average", ["triangularmovingaverage", "trma"], gocharting="TRIANGULAR", dynamic={"GoCharting": [20]}),
		Parameter("tweezerbottompattern", "Tweezer Bottom Pattern", ["tweezerbottom", "tbp", "tweezerbottompattern"], gocharting="TWEEZERBOTTOM"),
		Parameter("tweezertoppattern", "Tweezer Top Pattern", ["tweezertop", "ttp", "tweezertoppattern"], gocharting="TWEEZERTOP"),
		Parameter("tmfi", "Twiggs Money Flow Index", ["tmfi", "twiggsmfi", "twiggsmoneyflowindex"], gocharting="TWIGGSMONEYFLOWINDEX", dynamic={"GoCharting": [20]}),
		Parameter("typicalprice", "Typical Price", ["typicalprice", "tp"], gocharting="TP", dynamic={"GoCharting": [20]}),
		Parameter("ulcer", "Ulcer Index", ["ulcer", "ulcerindex", "ui"], gocharting="ULCERINDEX", dynamic={"GoCharting": [14, 2]}),
		Parameter("ultimate", "Ultimate Oscillator", ["ultimate", "uo", "ultimateoscillator"], tradingview="UltimateOsc@tv-basicstudies"),
		Parameter("vidya", "VIDYA Moving Average", ["vidya", "vidyamovingaverage"], gocharting="VIDYA", dynamic={"GoCharting": [20]}),
		Parameter("vigor", "Vigor Index", ["vigor", "vigorindex"], tradingview="VigorIndex@tv-basicstudies"),
		Parameter("vma", "Variable Moving Average", ["vma", "variablema", "varma", "variablemovingaverage"], gocharting="VMA", dynamic={"GoCharting": [20]}),
		Parameter("volatility", "Volatility Index", ["volatility", "vi", "volatilityindex"], tradingview="VolatilityIndex@tv-basicstudies"),
		Parameter("volumeoscillator", "Volume Oscillator", ["volosc", "volumeoscillator"], gocharting="VOLUMEOSCILLATOR"),
		Parameter("volumeprofile", "Volume Profile", ["volumeprofile"], gocharting="VOLUMEPROFILE"),
		Parameter("volumeroc", "Volume ROC", ["vroc", "volumeroc"], gocharting="VOLUMEROC", dynamic={"GoCharting": [20]}),
		Parameter("volumeunderlay", "Volume Underlay", ["volund", "volumeunderlay"], gocharting="VOLUMEUNDERLAY", dynamic={"GoCharting": [20]}),
		Parameter("vortex", "Vortex", ["vortex"], gocharting="VORTEX", dynamic={"GoCharting": [20]}),
		Parameter("vstop", "VSTOP", ["vstop"], tradingview="VSTOP@tv-basicstudies"),
		Parameter("vwap", "VWAP", ["vwap"], tradingview="VWAP@tv-basicstudies", gocharting="VWAP"),
		Parameter("vwma", "VWMA", ["mavw", "vw", "vwma"], tradingview="MAVolumeWeighted@tv-basicstudies", dynamic={"GoCharting": [20]}),
		Parameter("weightedclose", "Weighted Close", ["weightedclose"], gocharting="WC", dynamic={"GoCharting": [20]}),
		Parameter("williamsr", "Williams %R", ["williamsr", "wr", "williams%r"], tradingview="WilliamR@tv-basicstudies", gocharting="WILLIAMSR", dynamic={"GoCharting": [14, 20, 80]}),
		Parameter("williamsa", "Williams Alligator", ["williamsa", "williamsalligator", "wa"], tradingview="WilliamsAlligator@tv-basicstudies"),
		Parameter("williamsf", "Williams Fractal", ["williamsf", "williamsfractal", "wf"], tradingview="WilliamsFractal@tv-basicstudies"),
		Parameter("wma", "Weighted Moving Average", ["wma", "weightedmovingaverage"], tradingview="MAWeighted@tv-basicstudies", gocharting="WMA"),
		Parameter("zz", "Zig Zag", ["zz", "zigzag"], tradingview="ZigZag@tv-basicstudies", gocharting="ZIGZAG")
	],
	"types": [
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
		Parameter("forcePlatform", "force chart on TradingLite", ["tl", "tradinglite"], tradinglite=True),
		Parameter("forcePlatform", "force chart on TradingView", ["tv", "tradingview"], tradingview=True),
		Parameter("forcePlatform", "force chart on Bookmap", ["bm", "bookmap"], bookmap=True),
		Parameter("forcePlatform", "force chart on GoCharting", ["gc", "gocharting"], gocharting=True),
		Parameter("forcePlatform", "force chart on Finviz", ["fv", "finviz"], finviz=True),
		Parameter("forcePlatform", "force chart on Alternative.me", ["am", "alternativeme"], alternativeme=True),
		Parameter("force", "force", ["--force"], tradinglite="force", tradingview="force", bookmap="force", gocharting="force", finviz="force", alternativeme="force", alphaflow="force"),
		Parameter("upload", "upload", ["--upload"], tradinglite="upload", tradingview="upload", bookmap="upload", gocharting="upload", finviz="upload", alternativeme="upload", alphaflow="upload")
	]
}
DEFAULTS = {
	"Alternative.me": {
		"timeframes": [Parameter(None, None, None)],
		"indicators": [],
		"types": [],
		"style": [],
		"preferences": []
	},
	"TradingLite": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [],
		"style": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="style", params=PARAMETERS)],
		"preferences": [AbstractRequest.find_parameter_with_id("heatmapIntensity", name="normal heatmap intensity", type="preferences", params=PARAMETERS)]
	},
	"TradingView": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("candleStyle", name="candles", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Bookmap": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [],
		"style": [],
		"preferences": []
	},
	"GoCharting": {
		"timeframes": [AbstractRequest.find_parameter_with_id(60, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [AbstractRequest.find_parameter_with_id("theme", name="dark theme", type="types", params=PARAMETERS), AbstractRequest.find_parameter_with_id("candleStyle", name="candles", type="types", params=PARAMETERS)],
		"style": [],
		"preferences": []
	},
	"Finviz": {
		"timeframes": [AbstractRequest.find_parameter_with_id(1440, type="timeframes", params=PARAMETERS)],
		"indicators": [],
		"types": [AbstractRequest.find_parameter_with_id("candleStyle", name="candles", type="types", params=PARAMETERS)],
		"style": [AbstractRequest.find_parameter_with_id("theme", name="light theme", type="style", params=PARAMETERS)],
		"preferences": []
	},
	"Alpha Flow": {
		"timeframes": [],
		"indicators": [],
		"types": [],
		"style": [],
		"preferences": []
	}
}


class ChartRequestHandler(AbstractRequestHandler):
	def __init__(self, tickerId, platforms, bias="traditional"):
		super().__init__(platforms)
		for platform in platforms:
			self.requests[platform] = ChartRequest(tickerId, platform, bias)

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

			outputMessage, success = await request.add_indicator(_argument)
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

			outputMessage, success = await request.add_exchange(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			outputMessage, success = await request.add_numerical_parameters(_argument)
			if outputMessage is not None: finalOutput = outputMessage
			elif success: continue

			if finalOutput is None:
				request.set_error(f"`{argument[:229]}` is not a valid argument.", isFatal=True)
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
					request.set_error(f"Requested chart for `{request.ticker.get('id')}` is not available.", isFatal=True)
				elif request.exchange.get("id") in ["binanceusdm", "binancecoinm", "ftx", "okex5"]:
					request.set_error(f"{request.exchange.get('name')} exchange is not available. ||Yet.||", isFatal=True)
			
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
						request.set_error(f"{indicators[i].name} indicator takes in `{len(indicators[i].dynamic[platform])}` {'parameters' if len(indicators[i].dynamic[platform]) > 1 else 'parameter'}, but `{len(lengths[i])}` were given.", isFatal=True)
						break

				if len(indicators) == 0 and len(parameters) != 0:
					request.set_error(f"`{str(parameters[0])[:229]}` is not a valid argument.", isFatal=True)
			
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
				outputMessage = f"`{parsedIndicator.name}` indicator is not supported on {self.platform}."
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
		typeSupported, parsedType = self.add_parameter(argument, "types")
		if parsedType is not None and not self.has_parameter(parsedType.id, self.types):
			if not typeSupported:
				outputMessage = f"`{parsedType.name.title()}` chart style is not supported on {self.platform}."
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
				outputMessage = "Only parameters greater than `0` are valid."
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
		elif t == "types":
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

					indicators.insert(0, f"{self.indicators[i].parsed[self.platform]}_{'_'.join([str(l) for l in lengths[i]])}")

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