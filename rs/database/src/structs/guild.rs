use serde::Deserialize;

use crate::AccountProperties;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct ChartingSettings {
    pub theme: String,
    pub timeframe: String,
    pub indicators: Vec<String>,
    pub chartType: String,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct MessageProcessingData {
    pub autodelete: Option<u32>,
    pub bias: String,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct SetupData {
    pub completed: bool,
    pub connection: Option<String>,
    pub tos: u8,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct SettingsData {
    pub messageProcessing: MessageProcessingData,
    pub setup: SetupData,
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct GuildProperties {
    pub charting: ChartingSettings,
    pub settings: SettingsData,
    pub connection: Option<AccountProperties>,
}
