use self::{account::AccountInfo, guild::GuildInfo};

pub mod account;
pub mod guild;

pub trait DatabaseObject {
	fn mode() -> String;
}

impl DatabaseObject for AccountInfo {
	fn mode() -> String {
		"account".to_owned()
	}
}

impl DatabaseObject for GuildInfo {
	fn mode() -> String {
		"guild".to_owned()
	}
}