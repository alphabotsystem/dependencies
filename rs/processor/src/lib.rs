mod commands;

use async_recursion::async_recursion;
use google_cloud_auth::project::{create_token_source, Config};
use reqwest::{Client, Error};
use serde_json::{json, Value};
use std::env;
use tokio::time::{sleep, Duration};

pub use crate::commands::*;

#[async_recursion]
pub async fn process_task(
    mut request: Value,
    service: &str,
    endpoint: Option<&'async_recursion str>,
    origin: Option<String>,
    retries: Option<u8>,
	max_retries: Option<u8>,
) -> Result<Value, Error> {
    let retries = retries.unwrap_or(1);
	let max_retries = max_retries.unwrap_or(5);

    let endpoint = endpoint.unwrap_or("");
    let origin = origin.unwrap_or("default".to_string());

    let data = request.as_object_mut().unwrap();
    data.insert("origin".to_string(), Value::String(origin.clone()));

    let scopes = ["https://www.googleapis.com/auth/cloud-platform"];
    let config = Config {
        audience: None,
        scopes: Some(&scopes),
        sub: None,
    };
    let ts = match create_token_source(config).await {
        Ok(ts) => ts,
        Err(e) => {
            return Ok(json!({
                "message": format!("Error: {}", e),
                "response": Value::Null
            }));
        }
    };
    let token = ts.token().await.unwrap();

    let client = Client::new();
    let base_url = match service {
        "parser" => {
            if env::var("PRODUCTION").is_ok() {
                "http://parser:6900/"
            } else {
                "http://parser:6900/"
            }
        }
        "candle" => {
            if env::var("PRODUCTION").is_ok() {
                "http://candle-server:6900/"
            } else {
                "http://candle-server:6900/"
            }
        }
        "chart" => {
            if env::var("PRODUCTION").is_ok() {
                "https://image-server-yzrdox65bq-uc.a.run.app/"
            } else {
                "http://image-server:6900/"
            }
        }
        "depth" => {
            if env::var("PRODUCTION").is_ok() {
                "http://quote-server:6900/"
            } else {
                "http://quote-server:6900/"
            }
        }
        "detail" => {
            if env::var("PRODUCTION").is_ok() {
                "http://quote-server:6900/"
            } else {
                "http://quote-server:6900/"
            }
        }
        "heatmap" => {
            if env::var("PRODUCTION").is_ok() {
                "https://image-server-yzrdox65bq-uc.a.run.app/"
            } else {
                "http://image-server:6900/"
            }
        }
        "quote" => {
            if env::var("PRODUCTION").is_ok() {
                "http://quote-server:6900/"
            } else {
                "http://quote-server:6900/"
            }
        }
        _ => panic!("Invalid service name"),
    };

    let response = client
        .post(base_url.to_owned() + service + endpoint)
        .header("Authorization", token.access_token)
        .json(&data)
        .send()
        .await?
        .json::<Value>()
        .await;

    if let Ok(data) = response {
        Ok(data)
    } else {
        if retries < max_retries {
            println!("Retrying {}{} request ({}/2)", service, endpoint, retries);
            sleep(Duration::from_secs(retries as u64)).await;
            process_task(
                request,
                service,
                Some(endpoint),
                Some(origin),
                Some(retries + 1),
				Some(max_retries),
            )
            .await
        } else {
            response
        }
    }
}
