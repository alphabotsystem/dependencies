use serde_json::{Value, json};

use crate::process_task;

pub async fn process_chart_arguments(arguments: Vec<&str>, platforms: Vec<&str>, ticker_id: Option<&str>, defaults: Value) -> (Value, Value) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": ticker_id,
			"defaults": defaults
		}),
		"parser",
		Some("/chart"),
		None,
		None,
		None
	).await;

	if let Err(e) = payload {
		(Value::String(e.to_string()), Value::Null)
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(payload.get("message").unwrap().clone(), payload.get("response").unwrap().clone())
	}
}

pub async fn process_heatmap_arguments(arguments: Vec<&str>, platforms: Vec<&str>) -> (Value, Value) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms
		}),
		"parser",
		Some("/heatmap"),
		None,
		None,
		None
	).await;

	if let Err(e) = payload {
		(Value::String(e.to_string()), Value::Null)
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(payload.get("message").unwrap().clone(), payload.get("response").unwrap().clone())
	}
}

pub async fn process_quote_arguments(arguments: Vec<&str>, platforms: Vec<&str>, ticker_id: Option<&str>) -> (Value, Value) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": ticker_id
		}),
		"parser",
		Some("/quote"),
		None,
		None,
		None
	).await;

	if let Err(e) = payload {
		(Value::String(e.to_string()), Value::Null)
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(payload.get("message").unwrap().clone(), payload.get("response").unwrap().clone())
	}
}

pub async fn process_detail_arguments(arguments: Vec<&str>, platforms: Vec<&str>, ticker_id: Option<&str>) -> (Value, Value) {
	let payload = process_task(
		json!({
			"arguments": arguments,
			"platforms": platforms,
			"tickerId": ticker_id
		}),
		"parser",
		Some("/detail"),
		None,
		None,
		None
	).await;

	if let Err(e) = payload {
		(Value::String(e.to_string()), Value::Null)
	} else {
		let payload = unsafe { payload.unwrap_unchecked() };
		(payload.get("message").unwrap().clone(), payload.get("response").unwrap().clone())
	}
}