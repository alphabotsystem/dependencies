use serde::Deserialize;
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct ApiKeyData {
    pub key: String,
    pub secret: String,
    pub passphrase: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct ApiKeys {
    pub binance: Option<ApiKeyData>,
    pub binancefutures: Option<ApiKeyData>,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct FeatureData {
    pub enabled: Option<bool>,
    pub added: Option<Vec<String>>,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct CustomerData {
    pub slots: HashMap<String, HashMap<String, FeatureData>>,
    pub subscriptions: HashMap<String, u32>,
    pub stripeId: String,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct OAuthToken {
    pub accessToken: Option<String>,
    pub expiry: Option<u64>,
    pub userId: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct OAuthData {
    pub discord: OAuthToken,
    pub telegram: OAuthToken,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct PaperTraderBalance {
    pub Twelvedata: Option<HashMap<String, f64>>,
    pub CCXT: Option<HashMap<String, f64>>,
    pub USD: f64,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct PaperTraderData {
    pub globalLastReset: u64,
    pub globalResetCount: u64,
    pub balance: Option<PaperTraderBalance>,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct AccountProperties {
    pub apiKeys: ApiKeys,
    pub customer: CustomerData,
    pub oauth: OAuthData,
    pub paperTrader: Option<PaperTraderData>,
}
