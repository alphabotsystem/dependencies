use self::{account::AccountProperties, guild::GuildProperties};

pub mod account;
pub mod guild;

pub trait DatabaseObject {
	fn mode() -> String;
}

impl DatabaseObject for AccountProperties {
	fn mode() -> String {
		"account".to_owned()
	}
}

impl DatabaseObject for GuildProperties {
	fn mode() -> String {
		"guild".to_owned()
	}
}