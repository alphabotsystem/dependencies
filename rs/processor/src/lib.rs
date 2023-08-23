use std::env;
use google_cloud_auth::project::{create_token_source, Config};
use reqwest::Client;
use serde_json::{Map, Value};
use async_recursion::async_recursion;

#[async_recursion(?Send)]
pub async fn process_task(mut request: Map<String, Value>, service: &str, endpoint: Option<&'async_recursion str>, origin: Option<String>, retries: Option<u8>) -> Result<Map<String, Value>, reqwest::Error> {
	let retries = retries.unwrap_or(3);

	let endpoint = endpoint.unwrap_or("");
	let origin = origin.unwrap_or("default".to_string());
	request.insert("origin".to_string(), Value::String(origin.clone()));

    let scopes = ["https://www.googleapis.com/auth/cloud-platform"];
    let config = Config {
        audience: None,
        scopes: Some(&scopes),
        sub: None
    };
    let ts = create_token_source(config).await.unwrap();
    let token = ts.token().await.unwrap();
    println!("token is {}",token.access_token);

	let client = Client::new();
	let base_url = match service {
		"parser" => if env::var("PRODUCTION").is_ok() { "http://parser:6900/" } else { "http://parser:6900/" },
		"candle" => if env::var("PRODUCTION").is_ok() { "http://candle-server:6900/" } else { "http://candle-server:6900/" },
		"chart" => if env::var("PRODUCTION").is_ok() { "https://image-server-yzrdox65bq-uc.a.run.app/" } else { "http://image-server:6900/" },
		"depth" => if env::var("PRODUCTION").is_ok() { "http://quote-server:6900/" } else { "http://quote-server:6900/" },
		"detail" => if env::var("PRODUCTION").is_ok() { "http://quote-server:6900/" } else { "http://quote-server:6900/" },
		"heatmap" => if env::var("PRODUCTION").is_ok() { "https://image-server-yzrdox65bq-uc.a.run.app/" } else { "http://image-server:6900/" },
		"quote" => if env::var("PRODUCTION").is_ok() { "http://quote-server:6900/" } else { "http://quote-server:6900/" },
		_ => panic!("Invalid service name")
	};

	let response = client.post(base_url.to_owned() + service + endpoint)
		.header("Authorization", token.access_token)
		.json(&request)
		.send()
		.await?
		.json::<Map<String, Value>>()
		.await;

	if let Ok(data) = response {
		Ok(data)
	} else {
		if retries > 0 {
			process_task(request, service, Some(endpoint), Some(origin), Some(retries - 1)).await
		} else {
			response
		}
	}
}