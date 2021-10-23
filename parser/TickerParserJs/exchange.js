const ccxt = require('ccxt');
const supported = require("./supported.js");


class Exchange {
	constructor(id, marketType, name, region) {
		this.id = id
		this.name = null
		this.region = region
		this.properties = null
		this.type = marketType

		if (supported.ccxtExchanges.includes(id) && ccxt.exchanges.includes(id)) {
			this.properties = new ccxt[id];
			if (id == "binanceusdm") this.name = "Binance Futures" // USDⓈ-M
			else if (id == "binancecoinm") this.name = "Binance Futures COIN-M"
			else this.name = this.properties.name
			this.type = "crypto"
		} else {
			this.properties = new StocksExchange(id)
			this.name = !name ? id.charAt(0).toUpperCase() + id.substring(1) : name
		}
	}

	to_dict() {
		return {
			id: this.id,
			name: this.name,
			region: this.region,
			type: this.type
		}
	}

	static from_dict(d) {
		if (!d || Object.keys(d).length == 0) return null
		return new Exchange(d.id, d.type, d.name, d.region)
	}
}

class StocksExchange {
	constructor(id) {
		this.id = id
		this.symbols = []
		this.markets = {}
		this.timeframes = ["1m"]
	}

	milliseconds() {
		return Date.now();
	}
}

module.exports = { Exchange };