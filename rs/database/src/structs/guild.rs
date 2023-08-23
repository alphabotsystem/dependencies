use serde::Deserialize;

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct ChartingSettings {
	pub theme: String,
	pub timeframe: String,
	pub indicators: Vec<String>,
	pub chartType: String
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct AssistantData {
	pub enabled: bool
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct MessageProcessingData {
	pub autodelete: Option<u32>,
	pub bias: String
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct SetupData {
	pub completed: bool,
	pub connection: AccountInfo,
	pub tos: u8
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct SettingsData {
	pub assistant: AssistantData,
	pub messageProcessing: MessageProcessingData,
	pub setup: SetupData
}

#[derive(Debug, Clone, PartialEq, Deserialize)]
pub struct GuildInfo {
	pub charting: ChartingSettings,
	pub settings: SettingsData
}