pub mod structs;

use std::{collections::HashMap, fmt::Debug, marker::PhantomData};
use reqwest::Client;
use serde::de::DeserializeOwned;
use structs::DatabaseObject;
use async_recursion::async_recursion;

const BASE_URL: &str = "http://database:6900/";

pub struct DatabaseConnector<M: DatabaseObject> {
	_marker: PhantomData<M>,
	mode: String,
	client: Client,
}

impl<M> DatabaseConnector<M> where M: Debug, M: DatabaseObject, M: DeserializeOwned {
	pub fn new() -> DatabaseConnector<M> {
		DatabaseConnector {
			_marker: PhantomData,
			mode: M::mode(),
			client: Client::new(),
		}
	}

	#[async_recursion(?Send)]
	async fn process_task<T: DeserializeOwned>(&self, endpoint: &str, request: Option<HashMap<&'async_recursion str, &'async_recursion str>>, retries: Option<u8>) -> Result<T, reqwest::Error> {
		let retries = retries.unwrap_or(3);

		let response = self.client.post(BASE_URL.to_owned() + &self.mode + endpoint)
			.json(&request)
			.send()
			.await?
			.json::<T>()
			.await;

		if let Ok(data) = response {
			Ok(data)
		} else {
			if retries > 0 {
				self.process_task::<T>(endpoint, request, Some(retries - 1)).await
			} else {
				response
			}
		}
	}

	pub async fn check_status(&self) -> Option<String> {
		let response = self.process_task::<String>("/status", None, None).await;

		if let Ok(data) = response {
			Some(data)
		} else {
			eprintln!("Error: {:?}", response.unwrap_err());
			None
		}
	}

	pub async fn keys(&self, default: Option<HashMap<String, String>>) -> Option<HashMap<String, String>> {
		let response = self.process_task::<HashMap<String, String>>("/keys", None, None).await;

		if let Ok(data) = response {
			Some(data)
		} else {
			eprintln!("Error: {:?}", response.unwrap_err());
			default
		}
	}

	pub async fn get(&self, value: &str, default: Option<M>) -> Option<M> {
		let mut request = HashMap::new();
		request.insert("value", value);

		let response = self.process_task::<M>("/get", Some(request), None).await;

		if let Ok(data) = response {
			Some(data)
		} else {
			eprintln!("Error: {:?}", response.unwrap_err());
			default
		}
	}

	pub async fn match_id(&self, value: &str, default: Option<String>) -> Option<String> {
		let mut request = HashMap::new();
		request.insert("value", value);

		let response = self.process_task::<String>("/match", Some(request), None).await;

		if let Ok(data) = response {
			Some(data)
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
