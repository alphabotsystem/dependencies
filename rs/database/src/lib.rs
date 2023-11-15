pub mod structs;

use async_recursion::async_recursion;
use reqwest::Client;
use serde::de::DeserializeOwned;
use serde::Deserialize;
use serde_json::{json, Value};
use std::{collections::HashMap, fmt::Debug, marker::PhantomData};
use structs::DatabaseObject;
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

impl<M> DatabaseConnector<M>
where
    M: Debug,
    M: DatabaseObject,
    M: DeserializeOwned,
    M: Sync,
    M: Send,
{
    pub fn new() -> DatabaseConnector<M> {
        DatabaseConnector {
            _marker: PhantomData,
            mode: M::mode(),
            client: Client::new(),
        }
    }

    #[async_recursion]
    async fn process_task<T>(
        &self,
        endpoint: &str,
        request: Option<Value>,
        retries: Option<u8>,
        max_retries: Option<u8>,
    ) -> Result<Option<T>, reqwest::Error>
    where
        T: Debug,
        T: DeserializeOwned,
        T: Send,
    {
        let retries = retries.unwrap_or(1);
        let max_retries = max_retries.unwrap_or(5);

        let response = self
            .client
            .post(BASE_URL.to_owned() + &self.mode + endpoint)
            .json(&request)
            .send()
            .await?
            .json::<Response<T>>()
            .await;

        if let Ok(data) = response {
            Ok(data.response)
        } else {
            if retries < max_retries {
                self.process_task::<T>(endpoint, request, Some(retries + 1), Some(max_retries))
                    .await
            } else {
                Err(response.unwrap_err())
            }
        }
    }

    pub async fn check_status(&self) -> Option<String> {
        let response = self
            .process_task::<String>("/status", None, None, None)
            .await;

        if let Ok(data) = response {
            data
        } else {
            eprintln!(
                "Failed to fetch {} status: {:?}",
                self.mode,
                response.unwrap_err()
            );
            None
        }
    }

    pub async fn keys(
        &self,
        default: Option<HashMap<String, String>>,
    ) -> Option<HashMap<String, String>> {
        let response = self
            .process_task::<HashMap<String, String>>("/keys", None, None, None)
            .await;

        if let Ok(data) = response {
            data
        } else {
            eprintln!(
                "Failed to fetch {} keys: {:?}",
                self.mode,
                response.unwrap_err()
            );
            default
        }
    }

    pub async fn get(&self, value: &str, default: Option<M>) -> Option<M> {
        let request = json!({
            "key": value,
        });

        let response = self
            .process_task::<M>("/fetch", Some(request), None, None)
            .await;

        if let Ok(data) = response {
            data
        } else {
            eprintln!(
                "Failed to get {} properties: {:?}",
                self.mode,
                response.unwrap_err()
            );
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

        let response = self
            .process_task::<String>("/match", Some(request), None, None)
            .await;

        if let Ok(data) = response {
            data
        } else {
            eprintln!(
                "Failed to match {} id: {:?}",
                self.mode,
                response.unwrap_err()
            );
            default
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use structs::{account::AccountProperties, guild::GuildProperties};

    #[test]
    fn initialization() {
        let _ = DatabaseConnector::<AccountProperties>::new();
        let _ = DatabaseConnector::<GuildProperties>::new();
    }
}
