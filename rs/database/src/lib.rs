pub mod structs;

use std::{collections::HashMap, fmt::Debug, marker::PhantomData};
use reqwest::Client;
use serde::de::DeserializeOwned;
use serde::Deserialize;
use serde_json::{Value, json};
use structs::DatabaseObject;
use async_recursion::async_recursion;
pub use structs::{account::AccountProperties, guild::GuildProperties};

const BASE_URL: &str = "http://database:6900/";

pub struct DatabaseConnector<M: DatabaseObject> {
	_marker: PhantomData<M>,
	mode: String,
	client: Client,
}

#[derive(Debug, Deserialize)]
struct Response<T> {
	response: Option<T>,
}

impl<M> DatabaseConnector<M> where M: Debug, M: DatabaseObject, M: DeserializeOwned, M: Sync, M: Send {
	pub fn new() -> DatabaseConnector<M> {
		DatabaseConnector {
			_marker: PhantomData,
			mode: M::mode(),
			client: Client::new(),
		}
	}

	#[async_recursion]
	async fn process_task<T>(&self, endpoint: &str, request: Option<Value>, retries: Option<u8>) -> Result<Option<T>, reqwest::Error> where T: Debug, T: DeserializeOwned, T: Send {
		let retries = retries.unwrap_or(3);

		let response = self.client.post(BASE_URL.to_owned() + &self.mode + endpoint)
			.json(&request)
			.send()
			.await?
			.json::<Response<T>>()
			.await;

		if let Ok(data) = response {
			Ok(data.response)
		} else {
			if retries > 1 {
				self.process_task::<T>(endpoint, request, Some(retries - 1)).await
			} else {
				Err(response.unwrap_err())
			}
		}
	}

	pub async fn check_status(&self) -> Option<String> {
		let response = self.process_task::<String>("/status", None, None).await;

		if let Ok(data) = response {
			data
		} else {
			eprintln!("Error: {:?}", response.unwrap_err());
			None
		}
	}

	pub async fn keys(&self, default: Option<HashMap<String, String>>) -> Option<HashMap<String, String>> {
		let response = self.process_task::<HashMap<String, String>>("/keys", None, None).await;

		if let Ok(data) = response {
			data
		} else {
			eprintln!("Error: {:?}", response.unwrap_err());
			default
		}
	}

	pub async fn get(&self, value: &str, default: Option<M>) -> Option<M> {
		let request = json!({
			"key": value,
		});

		let response = self.process_task::<M>("/fetch", Some(request), None).await;

		if let Ok(data) = response {
			data
		} else {
			eprintln!("Error: {:?}", response.unwrap_err());
			default
		}
	}

	pub async fn match_id(&self, value: &str, default: Option<String>) -> Option<String> {
		if self.mode != "account" {
			panic!("match is only available for account mode");
		}

		let request = json!({
			"key": value,
		});

		let response = self.process_task::<String>("/match", Some(request), None).await;

		if let Ok(data) = response {
			data
		} else {
			eprintln!("Error: {:?}", response.unwrap_err());
			default
		}
	}
}

#[cfg(test)]
mod tests {
    use super::*;
	use structs::{guild::GuildInfo, account::AccountInfo};

    #[test]
    fn initialization() {
        let _ = DatabaseConnector::<AccountInfo>::new();
		let _ = DatabaseConnector::<GuildInfo>::new();
    }
}
